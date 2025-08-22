from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from django.db.models import Prefetch, Count, Avg, Sum
from django.core.cache import cache
from django.conf import settings
from django.db import transaction
from .models import (
    User,
    ClientProfile,
    Service,
    Cart,
    CartItem,
    Order,
    OrderItem,
    Review,
)
from .serializers import (
    UserSerializer,
    ClientProfileSerializer,
    ServiceSerializer,
    CartSerializer,
    OrderSerializer,
    ReviewSerializer,
)
from .forms import ClientProfileForm


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().select_related("clientprofile")
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        cache_key = f"user_queryset_{self.request.user.id}"
        cached_queryset = cache.get(cache_key)

        if cached_queryset is not None:
            return cached_queryset

        if self.request.user.role == "admin":
            queryset = User.objects.select_related("clientprofile").all()
        else:
            queryset = User.objects.select_related("clientprofile").filter(
                id=self.request.user.id
            )

        # Cache for 15 minutes
        cache.set(cache_key, queryset, settings.CACHE_TTL)
        return queryset

    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAdminUser])
    def promote(self, request, pk=None):
        user = get_object_or_404(User, pk=pk)
        user.role = "admin"
        user.save()

        # Invalidate user cache
        cache.delete(f"user_queryset_{request.user.id}")

        return Response({"status": "user promoted"})


class ClientProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ClientProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        cache_key = f"client_profiles_{self.request.user.id}"
        cached_queryset = cache.get(cache_key)

        if cached_queryset is not None:
            return cached_queryset

        if self.request.user.role == "admin":
            queryset = ClientProfile.objects.select_related("user").all()
        else:
            queryset = ClientProfile.objects.select_related("user").filter(
                user=self.request.user
            )

        # Cache for 15 minutes
        cache.set(cache_key, queryset, settings.CACHE_TTL)
        return queryset


class ServiceViewSet(viewsets.ModelViewSet):
    serializer_class = ServiceSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        search = self.request.query_params.get("search", None)
        sort = self.request.query_params.get("sort", None)

        # Create cache key
        cache_key = f"services_{search}_{sort}_{self.request.user.id if self.request.user.is_authenticated else 'anonymous'}"
        cached_queryset = cache.get(cache_key)

        if cached_queryset is not None:
            return cached_queryset

        queryset = Service.objects.all()

        if search:
            queryset = queryset.filter(name__icontains=search)

        if sort == "rating":
            queryset = queryset.order_by("-average_rating")

        # Cache for 15 minutes
        cache.set(cache_key, queryset, settings.CACHE_TTL)
        return queryset


class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        cache_key = f"cart_{self.request.user.id}"
        cached_queryset = cache.get(cache_key)

        if cached_queryset is not None:
            return cached_queryset

        # Optimize by prefetching related cart items and services
        queryset = Cart.objects.filter(user=self.request.user).prefetch_related(
            Prefetch(
                "cartitem_set", queryset=CartItem.objects.select_related("service")
            )
        )

        # Annotate with total price for efficiency
        queryset = queryset.annotate(
            annotated_total_price=Sum(
                models.F("cartitem_set__service__price")
                * models.F("cartitem_set__quantity")
            )
        )

        # Cache for 5 minutes (shorter cache time for cart)
        cache.set(cache_key, queryset, settings.CACHE_TTL // 3)
        return queryset

    @action(detail=False, methods=["post"])
    def add_service(self, request):
        # Use select_related to reduce database queries
        cart, created = Cart.objects.select_related("user").get_or_create(
            user=request.user
        )
        service_id = request.data.get("service_id")
        service = get_object_or_404(Service, id=service_id)

        with transaction.atomic():
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart, service=service
            )
            if not created:
                cart_item.quantity += 1
                cart_item.save()

        # Invalidate cache for this user's cart
        cache.delete(f"cart_{request.user.id}")

        return Response({"status": "service added to cart"})

    @action(detail=False, methods=["post"])
    def remove_service(self, request):
        # Use select_related to reduce database queries
        cart = get_object_or_404(Cart.objects.select_related("user"), user=request.user)
        service_id = request.data.get("service_id")
        service = get_object_or_404(Service, id=service_id)

        try:
            cart_item = CartItem.objects.get(cart=cart, service=service)
            cart_item.delete()

            # Invalidate cache for this user's cart
            cache.delete(f"cart_{request.user.id}")

            return Response({"status": "service removed from cart"})
        except CartItem.DoesNotExist:
            return Response(
                {"status": "service not in cart"}, status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=["post"])
    def checkout(self, request):
        # Optimize with select_related and prefetch_related
        cart = get_object_or_404(
            Cart.objects.prefetch_related(
                Prefetch(
                    "cartitem_set", queryset=CartItem.objects.select_related("service")
                )
            ),
            user=request.user,
        )

        if not cart.cartitem_set.exists():
            return Response(
                {"status": "cart is empty"}, status=status.HTTP_400_BAD_REQUEST
            )

        # Create order with all items in a single transaction
        with transaction.atomic():
            order = Order.objects.create(user=request.user)

            # Use bulk_create for order items to reduce database queries
            order_items = [
                OrderItem(order=order, service=item.service, quantity=item.quantity)
                for item in cart.cartitem_set.all()
            ]
            OrderItem.objects.bulk_create(order_items)

            # Clear cart items
            cart.cartitem_set.all().delete()

        # Invalidate cache for this user's cart and orders
        cache.delete(f"cart_{request.user.id}")
        cache.delete(f"orders_{request.user.id}")

        return Response({"status": "order created", "order_id": order.id})


class OrderViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Check cache first
        cache_key = f"orders_{self.request.user.id}"
        cached_queryset = cache.get(cache_key)

        if cached_queryset is not None:
            return cached_queryset

        # Optimize with prefetch_related for order items and services
        queryset = Order.objects.prefetch_related(
            Prefetch(
                "orderitem_set", queryset=OrderItem.objects.select_related("service")
            )
        ).select_related("user")

        if self.request.user.role == "admin":
            result = queryset
        else:
            result = queryset.filter(user=self.request.user)

        # Cache the result for 15 minutes
        cache.set(cache_key, result, settings.CACHE_TTL)
        return result


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        cache_key = f"reviews_{self.request.user.id}"
        cached_queryset = cache.get(cache_key)

        if cached_queryset is not None:
            return cached_queryset

        # Optimize with select_related for user and service
        queryset = Review.objects.select_related("user", "service")

        if self.request.user.role == "admin":
            result = queryset
        else:
            result = queryset.filter(user=self.request.user)

        # Cache for 15 minutes
        cache.set(cache_key, result, settings.CACHE_TTL)
        return result

    def perform_create(self, serializer):
        # Check if the user has a completed order for the service
        service = serializer.validated_data["service"]
        user = self.request.user

        # Optimize the query with exists() instead of filtering all orders
        if not Order.objects.filter(
            user=user, services=service, status="completed"
        ).exists():
            raise serializers.ValidationError(
                "You can only review services you have completed orders for."
            )

        serializer.save(user=user)

        # Invalidate cache for this service's reviews
        cache.delete(f"reviews_{service.id}")


def home(request):
    return render(request, "home.html")


def services(request):
    # Check cache first
    cache_key = f"web_services_{request.GET.get('search', '')}_{request.GET.get('sort', '')}_{request.user.id if request.user.is_authenticated else 'anonymous'}"
    cached_services = cache.get(cache_key)

    if cached_services is not None:
        return render(request, "services.html", {"services": cached_services})

    # Optimize the query with select_related if needed
    services = Service.objects.all()
    search = request.GET.get("search")
    sort = request.GET.get("sort")

    if search:
        services = services.filter(name__icontains=search)

    if sort == "rating":
        services = services.order_by("-average_rating")

    # Cache the result for 15 minutes
    cache.set(cache_key, services, settings.CACHE_TTL)

    return render(request, "services.html", {"services": services})


def service_detail(request, service_id):
    # Check cache first
    cache_key = f"service_detail_{service_id}_{request.user.id if request.user.is_authenticated else 'anonymous'}"
    cached_data = cache.get(cache_key)

    if cached_data is not None:
        return render(request, "service_detail.html", cached_data)

    # Optimize with select_related
    service = get_object_or_404(Service, id=service_id)

    # Check cache for reviews
    reviews_cache_key = f"reviews_{service_id}_{request.user.id if request.user.is_authenticated else 'anonymous'}"
    reviews = cache.get(reviews_cache_key)

    if reviews is None:
        reviews = (
            Review.objects.filter(service=service)
            .select_related("user")
            .order_by("-created_at")
        )
        # Cache reviews for 15 minutes
        cache.set(reviews_cache_key, reviews, settings.CACHE_TTL)

    context = {"service": service, "reviews": reviews}

    # Cache the service detail page for 15 minutes
    cache.set(cache_key, context, settings.CACHE_TTL)

    return render(request, "service_detail.html", context)


@login_required
def cart(request):
    # Check cache first
    cache_key = f"cart_{request.user.id}_web"
    cached_cart = cache.get(cache_key)

    if cached_cart is not None:
        return render(request, "cart.html", {"cart": cached_cart})

    # Optimize with prefetch_related to reduce database queries
    cart, created = Cart.objects.prefetch_related(
        Prefetch("cartitem_set", queryset=CartItem.objects.select_related("service"))
    ).get_or_create(user=request.user)

    # Cache the cart for 5 minutes (shorter cache time for cart)
    cache.set(cache_key, cart, settings.CACHE_TTL // 3)

    return render(request, "cart.html", {"cart": cart})


@login_required
def add_to_cart(request):
    if request.method == "POST":
        service_id = request.POST.get("service_id")
        service = get_object_or_404(Service, id=service_id)

        # Optimize with select_related
        with transaction.atomic():
            cart, created = Cart.objects.select_related("user").get_or_create(
                user=request.user
            )

            cart_item, created = CartItem.objects.get_or_create(
                cart=cart, service=service
            )
            if not created:
                cart_item.quantity += 1
                cart_item.save()

        messages.success(request, "Service added to cart!")

        # Invalidate cache for this user's cart
        cache.delete(f"cart_{request.user.id}_web")

    return redirect("service_detail", service_id=service_id)


@login_required
def remove_from_cart(request):
    if request.method == "POST":
        service_id = request.POST.get("service_id")
        service = get_object_or_404(Service, id=service_id)

        # Optimize with select_related
        cart = get_object_or_404(Cart.objects.select_related("user"), user=request.user)

        try:
            cart_item = CartItem.objects.get(cart=cart, service=service)
            cart_item.delete()
            messages.success(request, "Service removed from cart!")

            # Invalidate cache for this user's cart
            cache.delete(f"cart_{request.user.id}_web")
        except CartItem.DoesNotExist:
            messages.error(request, "Service not in cart.")
    return redirect("cart")


@login_required
def checkout(request):
    # Optimize with prefetch_related
    cart = get_object_or_404(
        Cart.objects.prefetch_related(
            Prefetch(
                "cartitem_set", queryset=CartItem.objects.select_related("service")
            )
        ),
        user=request.user,
    )

    if not cart.cartitem_set.exists():
        messages.error(request, "Your cart is empty.")
        return redirect("cart")

    # Create order with all items in a single transaction
    with transaction.atomic():
        order = Order.objects.create(user=request.user)

        # Use bulk_create for order items to reduce database queries
        order_items = [
            OrderItem(order=order, service=item.service, quantity=item.quantity)
            for item in cart.cartitem_set.all()
        ]
        OrderItem.objects.bulk_create(order_items)

        # Clear cart items
        cart.cartitem_set.all().delete()

    messages.success(request, "Order created successfully!")

    # Invalidate cache for this user's cart and orders
    cache.delete(f"cart_{request.user.id}_web")
    cache.delete(f"orders_{request.user.id}_web")

    return redirect("orders")


@login_required
def orders(request):
    # Check cache first
    cache_key = f"web_orders_{request.user.id}"
    cached_orders = cache.get(cache_key)

    if cached_orders is not None:
        return render(request, "orders.html", {"orders": cached_orders})

    # Optimize with prefetch_related for order items and services
    orders = (
        Order.objects.filter(user=request.user)
        .prefetch_related(
            Prefetch(
                "orderitem_set", queryset=OrderItem.objects.select_related("service")
            )
        )
        .order_by("-created_at")
    )

    # Cache the orders for 15 minutes
    cache.set(cache_key, orders, settings.CACHE_TTL)

    return render(request, "orders.html", {"orders": orders})


@login_required
def profile(request):
    # Optimize with select_related
    profile, created = ClientProfile.objects.select_related("user").get_or_create(
        user=request.user
    )
    return render(request, "profile.html", {"profile": profile})


@login_required
def edit_profile(request):
    # Optimize with select_related
    profile, created = ClientProfile.objects.select_related("user").get_or_create(
        user=request.user
    )

    if request.method == "POST":
        form = ClientProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect("profile")
    else:
        form = ClientProfileForm(instance=profile)
    return render(request, "edit_profile.html", {"form": form})


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect("home")
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {username}!")
                return redirect("home")
    else:
        form = AuthenticationForm()
    return render(request, "registration/login.html", {"form": form})


def logout_view(request):
    logout()

    # Clear all user-related cache
    if request.user.is_authenticated:
        cache.delete(f"cart_{request.user.id}_web")
        cache.delete(f"cart_{request.user.id}")
        cache.delete(f"orders_{request.user.id}_web")
        cache.delete(f"orders_{request.user.id}")

    messages.success(request, "You have been logged out successfully!")
    return redirect("home")

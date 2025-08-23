from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.postgres.search import SearchQuery, SearchVector
from django.contrib.sites.shortcuts import get_current_site
from django.core.cache import cache
from django.core.mail import send_mail
from django.db import transaction
from django.db.models import F, Prefetch, Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from drf_spectacular.utils import (
    OpenApiParameter,
    OpenApiTypes,
    extend_schema,
    extend_schema_view,
)
from rest_framework import permissions, serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.token_blacklist.models import (
    BlacklistedToken,
    OutstandingToken,
)

from .decorators import jwt_login_required
from .forms import ClientProfileForm
from .models import (
    Cart,
    CartItem,
    ClientProfile,
    Order,
    OrderItem,
    Review,
    Service,
    User,
)
from .permissions import IsOwnerOrAdmin
from .serializers import (
    CartSerializer,
    ClientProfileSerializer,
    OrderSerializer,
    ReviewSerializer,
    ServiceSerializer,
    UserSerializer,
)
from .tokens import account_activation_token


@extend_schema_view(
    list=extend_schema(
        summary="List all users",
        description="Retrieve a list of all user accounts. Admins can see all users, regular users can only see their own account.",
    ),
    create=extend_schema(
        summary="Create a new user account",
        description="Register a new user account. This endpoint is typically used for user registration.",
    ),
    retrieve=extend_schema(
        summary="Get user details",
        description="Retrieve detailed information about a specific user account by ID. Admins can view any user's details, while regular users can only view their own.",
    ),
    update=extend_schema(
        summary="Update user account",
        description="Update all fields of a specific user account. Users can update their own account, and admins can update any user's account.",
    ),
    partial_update=extend_schema(
        summary="Partially update user account",
        description="Update specific fields of a user account without affecting others. Users can partially update their own account, and admins can update any user's account.",
    ),
    destroy=extend_schema(
        summary="Delete a user account",
        description="Remove a user account from the system. Only administrators can delete user accounts.",
    ),
)
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

    @extend_schema(
        summary="Promote a user to administrator role",
        description=(
            "This endpoint allows an existing administrator to elevate another user's role to 'admin'. "
            "Only users with 'admin' privileges can access this endpoint. "
            "Upon successful promotion, the user will gain full administrative access to the system, "
            "including the ability to manage other users, services, and orders."
        ),
        request=None,
        responses={200: {"status": "user promoted"}},
    )
    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAdminUser])
    def promote(self, request, pk=None):
        if int(pk) == request.user.id:
            return Response(
                {"status": "You cannot promote yourself."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = get_object_or_404(User, pk=pk)
        if user.role == "admin":
            return Response(
                {"status": "User is already an admin."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.role = "admin"
        user.save()

        # Invalidate user cache
        cache.delete(f"user_queryset_{request.user.id}")

        return Response({"status": "user promoted"})


@extend_schema_view(
    list=extend_schema(
        summary="List all client profiles",
        description="Retrieve a list of all client profiles. Admins can see all profiles, regular users can only see their own profile.",
    ),
    create=extend_schema(
        summary="Create a client profile",
        description="Create a new client profile. This is typically done automatically when a user registers.",
    ),
    retrieve=extend_schema(
        summary="Get client profile details",
        description="Retrieve detailed information about a specific client profile by ID.",
        parameters=[
            OpenApiParameter(
                name="id",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.PATH,
                description="ID of the client profile to retrieve.",
            )
        ],
    ),
    update=extend_schema(
        summary="Update client profile",
        description="Update all fields of a specific client profile.",
        parameters=[
            OpenApiParameter(
                name="id",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.PATH,
                description="ID of the client profile to update.",
            )
        ],
    ),
    partial_update=extend_schema(
        summary="Partially update client profile",
        description="Update specific fields of a client profile without affecting others.",
        parameters=[
            OpenApiParameter(
                name="id",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.PATH,
                description="ID of the client profile to partially update.",
            )
        ],
    ),
    destroy=extend_schema(
        summary="Delete a client profile",
        description="Remove a client profile from the system.",
        parameters=[
            OpenApiParameter(
                name="id",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.PATH,
                description="ID of the client profile to delete.",
            )
        ],
    ),
)
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


@extend_schema_view(
    list=extend_schema(
        summary="List all services",
        description="Retrieve a list of all available household services. Supports search and sorting.",
    ),
    create=extend_schema(
        summary="Create a new service",
        description="Add a new household service to the platform. Admin access required.",
    ),
    retrieve=extend_schema(
        summary="Get service details",
        description="Retrieve detailed information about a specific service by ID.",
        parameters=[
            OpenApiParameter(
                name="id",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.PATH,
                description="ID of the service to retrieve.",
            )
        ],
    ),
    update=extend_schema(
        summary="Update service information",
        description="Update all fields of a specific service. Admin access required.",
        parameters=[
            OpenApiParameter(
                name="id",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.PATH,
                description="ID of the service to update.",
            )
        ],
    ),
    partial_update=extend_schema(
        summary="Partially update service information",
        description="Update specific fields of a service without affecting others. Admin access required.",
        parameters=[
            OpenApiParameter(
                name="id",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.PATH,
                description="ID of the service to partially update.",
            )
        ],
    ),
    destroy=extend_schema(
        summary="Delete a service",
        description="Remove a service from the platform. Admin access required.",
        parameters=[
            OpenApiParameter(
                name="id",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.PATH,
                description="ID of the service to delete.",
            )
        ],
    ),
)
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
            if "postgres" in settings.DATABASES["default"]["ENGINE"]:
                query = SearchQuery(search)
                queryset = queryset.annotate(
                    search=SearchVector("name", "description")
                ).filter(search=query)
            else:
                queryset = queryset.filter(name__icontains=search)

        if sort == "rating":
            queryset = queryset.order_by("-average_rating")

        # Cache for 15 minutes
        cache.set(cache_key, queryset, settings.CACHE_TTL)
        return queryset


@extend_schema_view(
    list=extend_schema(
        summary="List user's carts",
        description="Retrieve the current user's shopping cart. Each user typically has one cart.",
    ),
    create=extend_schema(
        summary="Create a new cart",
        description="Create a new shopping cart for the current user.",
    ),
    retrieve=extend_schema(
        summary="Get cart details",
        description="Retrieve detailed information about a specific cart by ID.",
        parameters=[
            OpenApiParameter(
                name="id",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.PATH,
                description="ID of the cart to retrieve.",
            )
        ],
    ),
    update=extend_schema(
        summary="Update cart",
        description="Update all fields of a specific cart.",
        parameters=[
            OpenApiParameter(
                name="id",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.PATH,
                description="ID of the cart to update.",
            )
        ],
    ),
    partial_update=extend_schema(
        summary="Partially update cart",
        description="Update specific fields of a cart without affecting others.",
        parameters=[
            OpenApiParameter(
                name="id",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.PATH,
                description="ID of the cart to partially update.",
            )
        ],
    ),
    destroy=extend_schema(
        summary="Delete a cart",
        description="Remove a cart from the system.",
        parameters=[
            OpenApiParameter(
                name="id",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.PATH,
                description="ID of the cart to delete.",
            )
        ],
    ),
)
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
                F("cartitem_set__service__price") * F("cartitem_set__quantity")
            ),
            annotated_item_count=Sum("cartitem_set__quantity"),
        )

        # Cache for 5 minutes (shorter cache time for cart)
        cache.set(cache_key, queryset, settings.CACHE_TTL // 3)
        return queryset

    @extend_schema(
        summary="Add service to cart",
        description=(
            "Add a service to the current user's shopping cart. "
            "If the service is already in the cart, its quantity will be increased by 1. "
            'Expected request body: `{"service_id": <integer>}`'
        ),
        request={
            "application/json": {
                "examples": {
                    "Add Service Example": {
                        "value": {"service_id": 123},
                        "summary": "Example of adding a service to the cart.",
                    }
                }
            }
        },
        responses={
            200: {
                "description": "Service added to cart successfully.",
                "content": {
                    "application/json": {
                        "examples": {
                            "Success Response": {
                                "value": {"status": "service added to cart"},
                                "summary": "Successful response",
                            }
                        }
                    }
                },
            }
        },
    )
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

    @extend_schema(
        summary="Remove service from cart",
        description=(
            "Remove a service from the current user's shopping cart. "
            'Expected request body: `{"service_id": <integer>}`'
        ),
        request={
            "application/json": {
                "examples": {
                    "Remove Service Example": {
                        "value": {"service_id": 123},
                        "summary": "Example of removing a service from the cart.",
                    }
                }
            }
        },
        responses={
            200: {
                "description": "Service removed from cart successfully.",
                "content": {
                    "application/json": {
                        "examples": {
                            "Success Response": {
                                "value": {"status": "service removed from cart"},
                                "summary": "Successful response",
                            }
                        }
                    }
                },
            },
            400: {
                "description": "Service not in cart.",
                "content": {
                    "application/json": {
                        "examples": {
                            "Error Response": {
                                "value": {"status": "service not in cart"},
                                "summary": "Error response",
                            }
                        }
                    }
                },
            },
        },
    )
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

    @extend_schema(
        summary="Checkout cart",
        description="Convert all items in the current user's cart to a new order. This action clears the cart.",
        request=None,
        responses={
            200: {"status": "order created", "order_id": "integer"},
            400: {"status": "cart is empty"},
        },
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


@extend_schema_view(
    list=extend_schema(
        summary="List user's orders",
        description="Retrieve a list of all orders for the current user. Admins can see all orders.",
    ),
    retrieve=extend_schema(
        summary="Get order details",
        description="Retrieve detailed information about a specific order by ID.",
        parameters=[
            OpenApiParameter(
                name="id",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.PATH,
                description="ID of the order to retrieve.",
            )
        ],
    ),
)
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
        queryset = (
            Order.objects.prefetch_related(
                Prefetch(
                    "orderitem_set",
                    queryset=OrderItem.objects.select_related("service"),
                )
            )
            .select_related("user")
            .annotate(
                annotated_total_price=Sum(
                    F("orderitem_set__service__price") * F("orderitem_set__quantity")
                ),
                annotated_item_count=Sum("orderitem_set__quantity"),
            )
        )

        if self.request.user.role == "admin":
            result = queryset
        else:
            result = queryset.filter(user=self.request.user)

        # Cache the result for 15 minutes
        cache.set(cache_key, result, settings.CACHE_TTL)
        return result


@extend_schema_view(
    list=extend_schema(
        summary="List all reviews",
        description="Retrieve a list of all service reviews. Admins can see all reviews, regular users can only see their own reviews.",
    ),
    create=extend_schema(
        summary="Create a new review",
        description="Leave a review for a service you've ordered. You can only review services you've completed orders for.",
    ),
    retrieve=extend_schema(
        summary="Get review details",
        description="Retrieve detailed information about a specific review by ID.",
        parameters=[
            OpenApiParameter(
                name="id",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.PATH,
                description="ID of the review to retrieve.",
            )
        ],
    ),
    update=extend_schema(
        summary="Update a review",
        description="Update your review for a service.",
        parameters=[
            OpenApiParameter(
                name="id",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.PATH,
                description="ID of the review to update.",
            )
        ],
    ),
    partial_update=extend_schema(
        summary="Partially update a review",
        description="Update specific fields of your review without affecting others.",
        parameters=[
            OpenApiParameter(
                name="id",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.PATH,
                description="ID of the review to partially update.",
            )
        ],
    ),
    destroy=extend_schema(
        summary="Delete a review",
        description="Remove your review from the system.",
        parameters=[
            OpenApiParameter(
                name="id",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.PATH,
                description="ID of the review to delete.",
            )
        ],
    ),
)
class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsOwnerOrAdmin]

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
            user=user, services=service, status="COMPLETED"
        ).exists():
            raise serializers.ValidationError(
                "You can only review services you have completed orders for."
            )

        serializer.save(user=user)

        # Invalidate cache for this service's reviews and service detail
        cache.delete(f"reviews_{service.id}")
        cache.delete(
            f"service_detail_{service.id}_{user.id if user.is_authenticated else 'anonymous'}"
        )
        cache.delete(
            f"web_services__{user.id if user.is_authenticated else 'anonymous'}"
        )


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


@jwt_login_required
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


@jwt_login_required
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


@jwt_login_required
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


@jwt_login_required
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


@jwt_login_required
@login_required
def profile(request):
    # Optimize with select_related
    profile, created = ClientProfile.objects.select_related("user").get_or_create(
        user=request.user
    )
    return render(request, "profile.html", {"profile": profile})


@jwt_login_required
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
            user = form.save(commit=False)
            user.is_active = False  # User is inactive until email confirmation
            user.save()

            # Send activation email
            current_site = get_current_site(request)
            subject = "Activate your HomeSer account"

            # Render email content
            message = render_to_string(
                "registration/activation_email.txt",
                {
                    "user": user,
                    "domain": current_site.domain,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": account_activation_token.make_token(user),
                },
            )

            html_message = render_to_string(
                "registration/activation_email.html",
                {
                    "user": user,
                    "domain": current_site.domain,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": account_activation_token.make_token(user),
                },
            )

            # Send email
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
                html_message=html_message,
            )

            messages.success(
                request,
                "Registration successful! Please check your email to activate your account.",
            )
            return redirect("home")
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html", {"form": form})


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Your account has been activated successfully!")
        login(request, user)

        # Create JWT tokens for the newly activated user
        from .jwt_utils import create_jwt_tokens_for_user, set_jwt_cookies

        tokens = create_jwt_tokens_for_user(user)

        # Redirect to home and set JWT cookies
        response = redirect("home")
        response = set_jwt_cookies(response, tokens["access"], tokens["refresh"])
        return response
    else:
        messages.error(request, "Activation link is invalid!")
        return redirect("home")


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

                # Create JWT tokens
                from .jwt_utils import create_jwt_tokens_for_user, set_jwt_cookies

                tokens = create_jwt_tokens_for_user(user)

                # Redirect to home and set JWT cookies
                response = redirect("home")
                response = set_jwt_cookies(
                    response, tokens["access"], tokens["refresh"]
                )
                return response
    else:
        form = AuthenticationForm()
    return render(request, "registration/login.html", {"form": form})


def logout_view(request):
    user = request.user
    if user.is_authenticated:
        # Blacklist JWT tokens
        for token in OutstandingToken.objects.filter(user=user):
            BlacklistedToken.objects.get_or_create(token=token)

        logout(request)

        # Clear all user-related cache
        cache.delete(f"cart_{user.id}_web")
        cache.delete(f"cart_{user.id}")
        cache.delete(f"orders_{user.id}_web")
        cache.delete(f"orders_{user.id}")

    # Remove JWT cookies
    from .jwt_utils import unset_jwt_cookies

    response = redirect("home")
    response = unset_jwt_cookies(response)
    messages.success(request, "You have been logged out successfully!")
    return response

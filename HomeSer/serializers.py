from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

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


class UserSerializer(serializers.ModelSerializer):
    """User account information.

    This serializer handles user account data including authentication
    details.
    """

    id = serializers.IntegerField(
        read_only=True, help_text="Unique identifier for the user account."
    )
    username = serializers.CharField(help_text="Unique username for the user account.")
    email = serializers.EmailField(help_text="Email address of the user.")
    role = serializers.CharField(
        help_text="Role of the user (e.g., 'admin', 'client')."
    )

    class Meta:
        model = User
        fields = ("id", "username", "email", "role")
        read_only_fields = ("id",)


class ClientProfileSerializer(serializers.ModelSerializer):
    """Extended profile information for clients.

    Contains additional details about users with the 'client' role.
    """

    bio = serializers.CharField(
        help_text="A short biography or description of the client."
    )
    profile_picture = serializers.ImageField(
        help_text="URL or path to the client's profile picture."
    )
    social_links = serializers.JSONField(
        help_text="JSON object containing links to the client's social media profiles."
    )
    user_username = serializers.CharField(
        source="user.username",
        read_only=True,
        help_text="The username of the associated user account",
    )
    user_email = serializers.CharField(
        source="user.email",
        read_only=True,
        help_text="The email address of the associated user account",
    )

    class Meta:
        model = ClientProfile
        fields = (
            "bio",
            "profile_picture",
            "social_links",
            "user_username",
            "user_email",
        )
        read_only_fields = ("user",)


class ServiceSerializer(serializers.ModelSerializer):
    """Household service information.

    Represents a service that can be ordered through the platform.
    """

    id = serializers.IntegerField(
        read_only=True, help_text="Unique identifier for the service."
    )
    name = serializers.CharField(help_text="Name of the service.")
    description = serializers.CharField(
        help_text="Detailed description of the service."
    )
    price = serializers.DecimalField(
        max_digits=10, decimal_places=2, help_text="Price of the service."
    )
    average_rating = serializers.FloatField(
        read_only=True, help_text="Average rating of the service based on reviews."
    )

    class Meta:
        model = Service
        fields = ("id", "name", "description", "price", "average_rating")
        read_only_fields = ("id", "average_rating")


class CartItemSerializer(serializers.ModelSerializer):
    """Individual item in a shopping cart.

    Represents a service that has been added to a user's cart.
    """

    id = serializers.IntegerField(
        read_only=True, help_text="Unique identifier for the cart item."
    )
    service = serializers.PrimaryKeyRelatedField(
        queryset=Service.objects.all(), help_text="ID of the service in the cart."
    )
    service_name = serializers.CharField(
        source="service.name", read_only=True, help_text="Name of the service"
    )
    service_price = serializers.DecimalField(
        source="service.price",
        max_digits=10,
        decimal_places=2,
        read_only=True,
        help_text="Price of the service",
    )
    quantity = serializers.IntegerField(
        help_text="Number of units of the service in the cart."
    )

    class Meta:
        model = CartItem
        fields = ("id", "service", "service_name", "service_price", "quantity")
        read_only_fields = ("id",)


class CartSerializer(serializers.ModelSerializer):
    """User's shopping cart.

    Contains all services a user has selected but not yet ordered.
    """

    id = serializers.IntegerField(
        read_only=True, help_text="Unique identifier for the cart."
    )
    user = serializers.PrimaryKeyRelatedField(
        read_only=True, help_text="ID of the user who owns this cart."
    )
    services = serializers.PrimaryKeyRelatedField(
        many=True, read_only=True, help_text="List of service IDs in the cart."
    )
    items = CartItemSerializer(
        many=True, read_only=True, help_text="List of services in the cart"
    )
    total_price = serializers.SerializerMethodField(
        help_text="Total cost of all items in the cart"
    )
    item_count = serializers.SerializerMethodField(
        help_text="Total number of items in the cart"
    )

    class Meta:
        model = Cart
        fields = ("id", "user", "services", "items", "total_price", "item_count")
        read_only_fields = ("id", "user")

    @extend_schema_field(serializers.FloatField)
    def get_total_price(self, obj) -> float:
        # Optimize calculation using annotation if available
        if (
            hasattr(obj, "annotated_total_price")
            and obj.annotated_total_price is not None
        ):
            return obj.annotated_total_price
        # Fallback calculation
        return sum(
            item.service.price * item.quantity for item in obj.cartitem_set.all()
        )

    @extend_schema_field(serializers.IntegerField)
    def get_item_count(self, obj) -> int:
        # Optimize count using annotation if available
        if (
            hasattr(obj, "annotated_item_count")
            and obj.annotated_item_count is not None
        ):
            return obj.annotated_item_count
        # Fallback count
        return obj.cartitem_set.count()


class OrderItemSerializer(serializers.ModelSerializer):
    """Individual item in an order.

    Represents a service that has been ordered by a user.
    """

    id = serializers.IntegerField(
        read_only=True, help_text="Unique identifier for the order item."
    )
    service = serializers.PrimaryKeyRelatedField(
        queryset=Service.objects.all(), help_text="ID of the service in the order."
    )
    service_name = serializers.CharField(
        source="service.name", read_only=True, help_text="Name of the service"
    )
    service_price = serializers.DecimalField(
        source="service.price",
        max_digits=10,
        decimal_places=2,
        read_only=True,
        help_text="Price of the service at the time of order",
    )
    quantity = serializers.IntegerField(
        help_text="Number of units of the service in the order."
    )

    class Meta:
        model = OrderItem
        fields = ("id", "service", "service_name", "service_price", "quantity")
        read_only_fields = ("id",)


class OrderSerializer(serializers.ModelSerializer):
    """Service order information.

    Represents a confirmed order of services by a user.
    """

    id = serializers.IntegerField(
        read_only=True, help_text="Unique identifier for the order."
    )
    user = serializers.PrimaryKeyRelatedField(
        read_only=True, help_text="ID of the user who placed the order."
    )
    services = serializers.PrimaryKeyRelatedField(
        many=True, read_only=True, help_text="List of service IDs in the order."
    )
    created_at = serializers.DateTimeField(
        read_only=True, help_text="Timestamp when the order was created."
    )
    status = serializers.CharField(
        help_text="Current status of the order (e.g., 'pending', 'completed', 'cancelled')."
    )
    items = OrderItemSerializer(
        many=True,
        read_only=True,
        source="orderitem_set",
        help_text="List of services included in this order",
    )
    total_price = serializers.SerializerMethodField(
        help_text="Total cost of all items in the order"
    )
    item_count = serializers.SerializerMethodField(
        help_text="Total number of items in the order"
    )

    class Meta:
        model = Order
        fields = (
            "id",
            "user",
            "services",
            "created_at",
            "status",
            "items",
            "total_price",
            "item_count",
        )
        read_only_fields = ("id", "user", "created_at")

    @extend_schema_field(serializers.FloatField)
    def get_total_price(self, obj) -> float:
        # Optimize calculation using annotation if available
        if (
            hasattr(obj, "annotated_total_price")
            and obj.annotated_total_price is not None
        ):
            return obj.annotated_total_price
        # Fallback calculation
        return sum(
            item.service.price * item.quantity for item in obj.orderitem_set.all()
        )

    @extend_schema_field(serializers.IntegerField)
    def get_item_count(self, obj) -> int:
        # Optimize count using annotation if available
        if (
            hasattr(obj, "annotated_item_count")
            and obj.annotated_item_count is not None
        ):
            return obj.annotated_item_count
        # Fallback count
        return obj.orderitem_set.count()


class ReviewSerializer(serializers.ModelSerializer):
    """Service review and rating.

    Allows users to provide feedback on completed services.
    """

    id = serializers.IntegerField(
        read_only=True, help_text="Unique identifier for the review."
    )
    user = serializers.PrimaryKeyRelatedField(
        read_only=True, help_text="ID of the user who wrote the review."
    )
    user_username = serializers.CharField(
        source="user.username", read_only=True, help_text="Username of the reviewer"
    )
    service = serializers.PrimaryKeyRelatedField(
        queryset=Service.objects.all(), help_text="ID of the service being reviewed."
    )
    service_name = serializers.CharField(
        source="service.name",
        read_only=True,
        help_text="Name of the service being reviewed",
    )
    rating = serializers.IntegerField(
        help_text="Rating given to the service (e.g., 1 to 5 stars)."
    )
    text = serializers.CharField(help_text="Detailed text of the review.")
    created_at = serializers.DateTimeField(
        read_only=True, help_text="Timestamp when the review was created."
    )

    class Meta:
        model = Review
        fields = (
            "id",
            "user",
            "user_username",
            "service",
            "service_name",
            "rating",
            "text",
            "created_at",
        )
        read_only_fields = ("id", "user", "created_at")

from rest_framework import serializers
from .models import User, ClientProfile, Service, Cart, CartItem, Order, OrderItem, Review


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'role')
        read_only_fields = ('id',)


class ClientProfileSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True)
    user_email = serializers.CharField(source='user.email', read_only=True)
    
    class Meta:
        model = ClientProfile
        fields = ('bio', 'profile_picture', 'social_links', 'user_username', 'user_email')
        read_only_fields = ('user',)


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ('id', 'name', 'description', 'price', 'average_rating')
        read_only_fields = ('id', 'average_rating')


class CartItemSerializer(serializers.ModelSerializer):
    service_name = serializers.CharField(source='service.name', read_only=True)
    service_price = serializers.DecimalField(source='service.price', max_digits=10, decimal_places=2, read_only=True)
    
    class Meta:
        model = CartItem
        fields = ('id', 'service', 'service_name', 'service_price', 'quantity')
        read_only_fields = ('id',)


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()
    item_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Cart
        fields = ('id', 'user', 'services', 'items', 'total_price', 'item_count')
        read_only_fields = ('id', 'user')
    
    def get_total_price(self, obj):
        # Optimize calculation using annotation if available
        if hasattr(obj, 'annotated_total_price') and obj.annotated_total_price is not None:
            return obj.annotated_total_price
        # Fallback calculation
        return sum(item.service.price * item.quantity for item in obj.cartitem_set.all())
    
    def get_item_count(self, obj):
        # Optimize count using annotation if available
        if hasattr(obj, 'annotated_item_count') and obj.annotated_item_count is not None:
            return obj.annotated_item_count
        # Fallback count
        return obj.cartitem_set.count()


class OrderItemSerializer(serializers.ModelSerializer):
    service_name = serializers.CharField(source='service.name', read_only=True)
    service_price = serializers.DecimalField(source='service.price', max_digits=10, decimal_places=2, read_only=True)
    
    class Meta:
        model = OrderItem
        fields = ('id', 'service', 'service_name', 'service_price', 'quantity')
        read_only_fields = ('id',)


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()
    item_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Order
        fields = ('id', 'user', 'services', 'created_at', 'status', 'items', 'total_price', 'item_count')
        read_only_fields = ('id', 'user', 'created_at')
    
    def get_total_price(self, obj):
        # Optimize calculation using annotation if available
        if hasattr(obj, 'annotated_total_price') and obj.annotated_total_price is not None:
            return obj.annotated_total_price
        # Fallback calculation
        return sum(item.service.price * item.quantity for item in obj.orderitem_set.all())
    
    def get_item_count(self, obj):
        # Optimize count using annotation if available
        if hasattr(obj, 'annotated_item_count') and obj.annotated_item_count is not None:
            return obj.annotated_item_count
        # Fallback count
        return obj.orderitem_set.count()


class ReviewSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True)
    service_name = serializers.CharField(source='service.name', read_only=True)
    
    class Meta:
        model = Review
        fields = ('id', 'user', 'user_username', 'service', 'service_name', 'rating', 'text', 'created_at')
        read_only_fields = ('id', 'user', 'created_at')
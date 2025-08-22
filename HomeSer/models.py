from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.db.models import Index


class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('client', 'Client'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='client')

    def __str__(self):
        return self.username

    class Meta:
        indexes = [
            models.Index(fields=['role']),
            models.Index(fields=['is_active']),
        ]


class ClientProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True)
    social_links = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    class Meta:
        indexes = [
            models.Index(fields=['user']),
        ]


class Service(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    average_rating = models.FloatField(default=0.0)

    def __str__(self):
        return self.name

    class Meta:
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['average_rating']),
            models.Index(fields=['price']),
        ]


class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    services = models.ManyToManyField(Service, through='CartItem')

    def __str__(self):
        return f"Cart for {self.user.username}"

    class Meta:
        indexes = [
            models.Index(fields=['user']),
        ]


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.service.name} in cart for {self.cart.user.username}"

    class Meta:
        indexes = [
            models.Index(fields=['cart']),
            models.Index(fields=['service']),
        ]
        unique_together = ['cart', 'service']


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    services = models.ManyToManyField(Service, through='OrderItem')
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default='PENDING_PAYMENT')

    def __str__(self):
        return f"Order {self.id} for {self.user.username}"

    class Meta:
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['created_at']),
            models.Index(fields=['status']),
        ]


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.service.name} in order {self.order.id}"

    class Meta:
        indexes = [
            models.Index(fields=['order']),
            models.Index(fields=['service']),
        ]


class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} for {self.service.name}"

    class Meta:
        unique_together = ('user', 'service')
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['service']),
            models.Index(fields=['rating']),
            models.Index(fields=['created_at']),
        ]
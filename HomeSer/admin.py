from django.contrib import admin

from .models import (Cart, CartItem, ClientProfile, Order, OrderItem, Review,
                     Service, User)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "role")
    list_filter = ("role",)


@admin.register(ClientProfile)
class ClientProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "bio")
    search_fields = ("user__username", "bio")


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "average_rating")
    search_fields = ("name", "description")


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("user",)
    search_fields = ("user__username",)


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ("cart", "service", "quantity")
    search_fields = ("cart__user__username", "service__name")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("user", "created_at", "status")
    list_filter = ("status", "created_at")
    search_fields = ("user__username",)


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("order", "service", "quantity")
    search_fields = ("order__user__username", "service__name")


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("user", "service", "rating", "created_at")
    list_filter = ("rating", "created_at")
    search_fields = ("user__username", "service__name")

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r"users", views.UserViewSet)
router.register(r"profiles", views.ClientProfileViewSet, basename="clientprofile")
router.register(r"services", views.ServiceViewSet, basename="service")
router.register(r"cart", views.CartViewSet, basename="cart")
router.register(r"orders", views.OrderViewSet, basename="order")
router.register(r"reviews", views.ReviewViewSet, basename="review")

urlpatterns = [
    path("", include(router.urls)),
    path("auth/", include("rest_framework.urls")),
]

from django.urls import include, path
from drf_spectacular.views import (SpectacularAPIView, SpectacularRedocView,
                                   SpectacularSwaggerView)
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
    path("", views.api_root, name="api-root"),
    path("", include(router.urls)),
    path("auth/", include("rest_framework.urls")),
    # API documentation
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "docs/swagger/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path("docs/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    path("health/", views.health_check, name="health_check"),
]

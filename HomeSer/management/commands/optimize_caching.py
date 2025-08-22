from django.core.management.base import BaseCommand
from django.core.cache import cache
from django.conf import settings
from HomeSer.models import Service, Review, Order


class Command(BaseCommand):
    help = "Optimize caching by pre-populating cache with frequently accessed data"

    def handle(self, *args, **options):
        self.stdout.write("Optimizing caching...")

        # Clear existing cache
        cache.clear()
        self.stdout.write("Cache cleared")

        # Pre-populate cache with frequently accessed data
        self.populate_service_cache()
        self.populate_review_cache()
        self.populate_order_cache()

        self.stdout.write(self.style.SUCCESS("Caching optimization completed"))

    def populate_service_cache(self):
        """Pre-populate cache with service data"""
        self.stdout.write("Populating service cache...")

        # Cache all services
        services = Service.objects.all()
        cache.set("all_services", services, settings.CACHE_TTL)

        # Cache services by rating
        top_rated_services = Service.objects.order_by("-average_rating")[:10]
        cache.set("top_rated_services", top_rated_services, settings.CACHE_TTL)

        # Cache individual services
        for service in services:
            cache_key = f"service_{service.id}"
            cache.set(cache_key, service, settings.CACHE_TTL)

        self.stdout.write(self.style.SUCCESS(f"Cached {services.count()} services"))

    def populate_review_cache(self):
        """Pre-populate cache with review data"""
        self.stdout.write("Populating review cache...")

        # Cache recent reviews
        recent_reviews = Review.objects.select_related("user", "service").order_by(
            "-created_at"
        )[:50]
        cache.set("recent_reviews", recent_reviews, settings.CACHE_TTL)

        # Cache reviews by service
        services = Service.objects.all()
        for service in services:
            service_reviews = (
                Review.objects.filter(service=service)
                .select_related("user")
                .order_by("-created_at")
            )
            cache_key = f"reviews_for_service_{service.id}"
            cache.set(cache_key, service_reviews, settings.CACHE_TTL)

        self.stdout.write(
            self.style.SUCCESS(f"Cached reviews for {services.count()} services")
        )

    def populate_order_cache(self):
        """Pre-populate cache with order data"""
        self.stdout.write("Populating order cache...")

        # Cache recent orders (for admin users)
        recent_orders = (
            Order.objects.select_related("user")
            .prefetch_related("orderitem_set__service")
            .order_by("-created_at")[:50]
        )
        cache.set("recent_orders", recent_orders, settings.CACHE_TTL)

        self.stdout.write(
            self.style.SUCCESS(f"Cached {recent_orders.count()} recent orders")
        )

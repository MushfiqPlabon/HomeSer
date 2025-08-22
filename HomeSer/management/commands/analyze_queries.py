from django.core.management.base import BaseCommand
from django.db import connection
from HomeSer.models import (
    User,
    ClientProfile,
    Service,
    Cart,
    CartItem,
    Order,
    OrderItem,
    Review,
)


class Command(BaseCommand):
    help = "Analyze database queries and suggest optimizations"

    def handle(self, *args, **options):
        self.stdout.write("Analyzing database queries...")

        # Analyze common queries and suggest optimizations
        self.analyze_user_queries()
        self.analyze_service_queries()
        self.analyze_cart_queries()
        self.analyze_order_queries()
        self.analyze_review_queries()

        self.stdout.write(self.style.SUCCESS("Query analysis completed"))

    def analyze_user_queries(self):
        """Analyze user-related queries"""
        self.stdout.write("\nUser Query Analysis:")
        self.stdout.write('  - Use select_related("user") when accessing user profiles')
        self.stdout.write(
            '  - Use prefetch_related("user") when accessing multiple user profiles'
        )
        self.stdout.write(
            "  - Index on role, username, and email fields for faster lookups"
        )
        self.stdout.write(
            "  - Use only() or defer() to limit fields when full objects are not needed"
        )

    def analyze_service_queries(self):
        """Analyze service-related queries"""
        self.stdout.write("\nService Query Analysis:")
        self.stdout.write(
            '  - Use select_related("service") when accessing services through foreign keys'
        )
        self.stdout.write(
            '  - Use prefetch_related("service") when accessing multiple services'
        )
        self.stdout.write(
            "  - Index on name, average_rating, and price fields for faster searches and sorting"
        )
        self.stdout.write(
            "  - Use only() or defer() to limit fields when full objects are not needed"
        )
        self.stdout.write("  - Consider caching for frequently accessed service data")

    def analyze_cart_queries(self):
        """Analyze cart-related queries"""
        self.stdout.write("\nCart Query Analysis:")
        self.stdout.write(
            '  - Use prefetch_related("items__service") to reduce queries when accessing cart items'
        )
        self.stdout.write(
            '  - Use select_related("user") when accessing carts for specific users'
        )
        self.stdout.write("  - Use bulk_create() for adding multiple items to cart")
        self.stdout.write(
            "  - Use delete() on QuerySet for removing all cart items at once"
        )
        self.stdout.write("  - Consider caching cart data for authenticated users")

    def analyze_order_queries(self):
        """Analyze order-related queries"""
        self.stdout.write("\nOrder Query Analysis:")
        self.stdout.write(
            '  - Use prefetch_related("orderitem_set__service") to reduce queries when accessing order items'
        )
        self.stdout.write(
            '  - Use select_related("user") when accessing orders for specific users'
        )
        self.stdout.write("  - Use bulk_create() for creating multiple order items")
        self.stdout.write(
            "  - Index on user, created_at, and status fields for faster lookups"
        )
        self.stdout.write("  - Consider caching order data for authenticated users")

    def analyze_review_queries(self):
        """Analyze review-related queries"""
        self.stdout.write("\nReview Query Analysis:")
        self.stdout.write(
            '  - Use select_related("user", "service") when accessing reviews'
        )
        self.stdout.write(
            '  - Use prefetch_related("user", "service") when accessing multiple reviews'
        )
        self.stdout.write(
            "  - Index on service, user, rating, and created_at fields for faster lookups"
        )
        self.stdout.write(
            "  - Use only() or defer() to limit fields when full objects are not needed"
        )
        self.stdout.write("  - Consider caching review data for services")

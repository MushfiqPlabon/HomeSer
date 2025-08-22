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
    help = "Optimize database queries for better performance"

    def handle(self, *args, **options):
        self.stdout.write("Optimizing database queries...")

        # Analyze and optimize common queries
        self.optimize_user_queries()
        self.optimize_service_queries()
        self.optimize_cart_queries()
        self.optimize_order_queries()
        self.optimize_review_queries()

        self.stdout.write(self.style.SUCCESS("Database query optimization completed"))

    def optimize_user_queries(self):
        """Optimize user-related queries"""
        self.stdout.write("\nOptimizing User Queries:")

        # Example: Optimize user profile retrieval
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

        # Show example optimization
        self.stdout.write("\n  Example Optimization:")
        self.stdout.write("    # Before (causes N+1 queries):")
        self.stdout.write("    users = User.objects.all()")
        self.stdout.write("    for user in users:")
        self.stdout.write("        print(user.clientprofile.bio)")
        self.stdout.write("")
        self.stdout.write("    # After (single query with join):")
        self.stdout.write(
            '    users = User.objects.select_related("clientprofile").all()'
        )
        self.stdout.write("    for user in users:")
        self.stdout.write("        print(user.clientprofile.bio)")

    def optimize_service_queries(self):
        """Optimize service-related queries"""
        self.stdout.write("\nOptimizing Service Queries:")

        # Example: Optimize service retrieval with ratings
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

        # Show example optimization
        self.stdout.write("\n  Example Optimization:")
        self.stdout.write("    # Before (causes N+1 queries):")
        self.stdout.write("    services = Service.objects.all()")
        self.stdout.write("    for service in services:")
        self.stdout.write("        print(service.name, service.average_rating)")
        self.stdout.write("")
        self.stdout.write("    # After (single query with optimized fields):")
        self.stdout.write(
            '    services = Service.objects.only("name", "average_rating").order_by("-average_rating")'
        )
        self.stdout.write("    for service in services:")
        self.stdout.write("        print(service.name, service.average_rating)")

    def optimize_cart_queries(self):
        """Optimize cart-related queries"""
        self.stdout.write("\nOptimizing Cart Queries:")

        # Example: Optimize cart retrieval with items
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

        # Show example optimization
        self.stdout.write("\n  Example Optimization:")
        self.stdout.write("    # Before (multiple queries):")
        self.stdout.write("    cart = Cart.objects.get(user=request.user)")
        self.stdout.write("    items = cart.items.all()")
        self.stdout.write("    for item in items:")
        self.stdout.write("        print(item.service.name, item.quantity)")
        self.stdout.write("")
        self.stdout.write("    # After (single query with prefetching):")
        self.stdout.write("    cart = Cart.objects.prefetch_related(")
        self.stdout.write(
            '        Prefetch("items", queryset=CartItem.objects.select_related("service"))'
        )
        self.stdout.write("    ).get(user=request.user)")
        self.stdout.write("    for item in cart.items.all():")
        self.stdout.write("        print(item.service.name, item.quantity)")

    def optimize_order_queries(self):
        """Optimize order-related queries"""
        self.stdout.write("\nOptimizing Order Queries:")

        # Example: Optimize order retrieval with items
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

        # Show example optimization
        self.stdout.write("\n  Example Optimization:")
        self.stdout.write("    # Before (multiple queries):")
        self.stdout.write("    orders = Order.objects.filter(user=request.user)")
        self.stdout.write("    for order in orders:")
        self.stdout.write("        items = order.orderitem_set.all()")
        self.stdout.write("        for item in items:")
        self.stdout.write("            print(item.service.name, item.quantity)")
        self.stdout.write("")
        self.stdout.write("    # After (single query with prefetching):")
        self.stdout.write(
            "    orders = Order.objects.filter(user=request.user).prefetch_related("
        )
        self.stdout.write(
            '        Prefetch("orderitem_set", queryset=OrderItem.objects.select_related("service"))'
        )
        self.stdout.write("    )")
        self.stdout.write("    for order in orders:")
        self.stdout.write("        for item in order.orderitem_set.all():")
        self.stdout.write("            print(item.service.name, item.quantity)")

    def optimize_review_queries(self):
        """Optimize review-related queries"""
        self.stdout.write("\nOptimizing Review Queries:")

        # Example: Optimize review retrieval
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

        # Show example optimization
        self.stdout.write("\n  Example Optimization:")
        self.stdout.write("    # Before (multiple queries):")
        self.stdout.write("    reviews = Review.objects.filter(service=service)")
        self.stdout.write("    for review in reviews:")
        self.stdout.write("        print(review.user.username, review.rating)")
        self.stdout.write("")
        self.stdout.write("    # After (single query with joins):")
        self.stdout.write(
            '    reviews = Review.objects.filter(service=service).select_related("user", "service")'
        )
        self.stdout.write("    for review in reviews:")
        self.stdout.write("        print(review.user.username, review.rating)")

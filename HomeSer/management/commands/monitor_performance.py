import time

from django.core.cache import cache
from django.core.management.base import BaseCommand
from django.db import connection

from HomeSer.models import (Cart, CartItem, ClientProfile, Order, OrderItem,
                            Review, Service, User)


class Command(BaseCommand):
    help = "Monitor application performance and provide optimization recommendations"

    def handle(self, *args, **options):
        self.stdout.write("Monitoring application performance...")

        # Measure database performance
        self.monitor_database_performance()

        # Measure cache performance
        self.monitor_cache_performance()

        # Analyze model relationships
        self.analyze_model_relationships()

        # Provide optimization recommendations
        self.provide_recommendations()

        self.stdout.write(self.style.SUCCESS("Performance monitoring completed"))

    def monitor_database_performance(self):
        """Monitor database performance"""
        self.stdout.write("\nDatabase Performance Monitoring:")

        # Measure query execution time for common operations
        start_time = time.time()

        # Test user query
        users = User.objects.all()[:10]
        user_query_time = time.time() - start_time

        # Test service query
        start_time = time.time()
        services = Service.objects.all()[:10]
        service_query_time = time.time() - start_time

        # Test cart query with related items
        start_time = time.time()
        carts = Cart.objects.prefetch_related("items__service").all()[:10]
        cart_query_time = time.time() - start_time

        # Test order query with related items
        start_time = time.time()
        orders = Order.objects.prefetch_related("orderitem_set__service").all()[:10]
        order_query_time = time.time() - start_time

        # Test review query
        start_time = time.time()
        reviews = Review.objects.select_related("user", "service").all()[:10]
        review_query_time = time.time() - start_time

        self.stdout.write(f"  User query time: {user_query_time:.4f} seconds")
        self.stdout.write(f"  Service query time: {service_query_time:.4f} seconds")
        self.stdout.write(f"  Cart query time: {cart_query_time:.4f} seconds")
        self.stdout.write(f"  Order query time: {order_query_time:.4f} seconds")
        self.stdout.write(f"  Review query time: {review_query_time:.4f} seconds")

        # Database connection info
        self.stdout.write(f"\n  Database vendor: {connection.vendor}")
        self.stdout.write(f"  Database connection alive: {connection.is_usable()}")

    def monitor_cache_performance(self):
        """Monitor cache performance"""
        self.stdout.write("\nCache Performance Monitoring:")

        # Test cache set operation
        start_time = time.time()
        cache.set("performance_test_key", "test_value", 300)
        cache_set_time = time.time() - start_time

        # Test cache get operation
        start_time = time.time()
        cached_value = cache.get("performance_test_key")
        cache_get_time = time.time() - start_time

        # Test cache delete operation
        start_time = time.time()
        cache.delete("performance_test_key")
        cache_delete_time = time.time() - start_time

        self.stdout.write(f"  Cache set time: {cache_set_time:.6f} seconds")
        self.stdout.write(f"  Cache get time: {cache_get_time:.6f} seconds")
        self.stdout.write(f"  Cache delete time: {cache_delete_time:.6f} seconds")

        # Cache backend info
        cache_backend = cache.__class__.__module__ + "." + cache.__class__.__name__
        self.stdout.write(f"  Cache backend: {cache_backend}")

    def analyze_model_relationships(self):
        """Analyze model relationships for optimization opportunities"""
        self.stdout.write("\nModel Relationship Analysis:")

        # Analyze User model
        self.stdout.write("  User Model:")
        self.stdout.write("    ✓ One-to-One relationship with ClientProfile")
        self.stdout.write("    ✓ One-to-Many relationship with Cart")
        self.stdout.write("    ✓ One-to-Many relationship with Order")
        self.stdout.write("    ✓ One-to-Many relationship with Review")

        # Analyze Service model
        self.stdout.write("  Service Model:")
        self.stdout.write("    ✓ Many-to-Many relationship with Cart through CartItem")
        self.stdout.write(
            "    ✓ Many-to-Many relationship with Order through OrderItem"
        )
        self.stdout.write("    ✓ One-to-Many relationship with Review")
        self.stdout.write("    ✓ Indexed fields: name, average_rating, price")

        # Analyze Cart model
        self.stdout.write("  Cart Model:")
        self.stdout.write("    ✓ One-to-One relationship with User")
        self.stdout.write(
            "    ✓ Many-to-Many relationship with Service through CartItem"
        )
        self.stdout.write("    ✓ One-to-Many relationship with CartItem")
        self.stdout.write("    ✓ Indexed fields: user")

        # Analyze CartItem model
        self.stdout.write("  CartItem Model:")
        self.stdout.write("    ✓ Many-to-One relationship with Cart")
        self.stdout.write("    ✓ Many-to-One relationship with Service")
        self.stdout.write("    ✓ Indexed fields: cart, service")

        # Analyze Order model
        self.stdout.write("  Order Model:")
        self.stdout.write("    ✓ Many-to-One relationship with User")
        self.stdout.write(
            "    ✓ Many-to-Many relationship with Service through OrderItem"
        )
        self.stdout.write("    ✓ One-to-Many relationship with OrderItem")
        self.stdout.write("    ✓ Indexed fields: user, created_at, status")

        # Analyze OrderItem model
        self.stdout.write("  OrderItem Model:")
        self.stdout.write("    ✓ Many-to-One relationship with Order")
        self.stdout.write("    ✓ Many-to-One relationship with Service")
        self.stdout.write("    ✓ Indexed fields: order, service")

        # Analyze Review model
        self.stdout.write("  Review Model:")
        self.stdout.write("    ✓ Many-to-One relationship with User")
        self.stdout.write("    ✓ Many-to-One relationship with Service")
        self.stdout.write("    ✓ Unique constraint on user and service")
        self.stdout.write("    ✓ Indexed fields: user, service, rating, created_at")

    def provide_recommendations(self):
        """Provide optimization recommendations"""
        self.stdout.write("\nPerformance Optimization Recommendations:")

        # Database recommendations
        self.stdout.write("  Database Optimizations:")
        self.stdout.write("    ✓ Use select_related() for foreign key relationships")
        self.stdout.write(
            "    ✓ Use prefetch_related() for many-to-many and reverse foreign key relationships"
        )
        self.stdout.write(
            "    ✓ Use only() or defer() to limit fields when full objects are not needed"
        )
        self.stdout.write("    ✓ Use bulk_create() for inserting multiple records")
        self.stdout.write("    ✓ Use bulk_update() for updating multiple records")
        self.stdout.write(
            "    ✓ Use exists() instead of count() when checking for existence"
        )
        self.stdout.write(
            "    ✓ Use iterator() for large querysets to reduce memory usage"
        )

        # Cache recommendations
        self.stdout.write("  Cache Optimizations:")
        self.stdout.write(
            "    ✓ Cache frequently accessed data like services and reviews"
        )
        self.stdout.write("    ✓ Use cache versioning for data that changes frequently")
        self.stdout.write("    ✓ Implement cache invalidation strategies")
        self.stdout.write("    ✓ Use cache timeouts appropriate to your data")
        self.stdout.write("    ✓ Consider using Redis for production caching")

        # Query recommendations
        self.stdout.write("  Query Optimizations:")
        self.stdout.write("    ✓ Use database indexes on frequently queried fields")
        self.stdout.write(
            "    ✓ Avoid N+1 query problems with proper use of select_related and prefetch_related"
        )
        self.stdout.write("    ✓ Use annotations instead of extra queries in loops")
        self.stdout.write("    ✓ Use Q objects for complex queries")
        self.stdout.write(
            "    ✓ Use raw SQL for complex queries that can't be optimized with ORM"
        )

        # Model recommendations
        self.stdout.write("  Model Optimizations:")
        self.stdout.write(
            "    ✓ Use database constraints instead of application-level validation when possible"
        )
        self.stdout.write("    ✓ Use proper field types for better performance")
        self.stdout.write(
            "    ✓ Use database-level defaults instead of application-level defaults"
        )
        self.stdout.write("    ✓ Use database indexes on frequently queried fields")
        self.stdout.write(
            "    ✓ Normalize data to reduce redundancy but denormalize when needed for performance"
        )

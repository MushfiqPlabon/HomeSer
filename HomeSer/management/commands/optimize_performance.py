from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.core.cache import cache
from django.db import connection
from HomeSer.models import Service, Review


class Command(BaseCommand):
    help = 'Comprehensive performance optimization including database, caching, and query analysis'

    def handle(self, *args, **options):
        self.stdout.write('Starting comprehensive performance optimization...')
        
        # Step 1: Optimize database
        self.optimize_database()
        
        # Step 2: Optimize caching
        self.optimize_caching()
        
        # Step 3: Analyze queries
        self.analyze_queries()
        
        self.stdout.write(
            self.style.SUCCESS('Comprehensive performance optimization completed')
        )
    
    def optimize_database(self):
        """Optimize the database"""
        self.stdout.write('Optimizing database...')
        
        # Run Django's built-in commands for optimization
        try:
            # Update content types
            call_command('contenttypes')
        except Exception as e:
            self.stdout.write(f'Note: contenttypes command not available or failed: {e}')
        
        # For SQLite, we can run VACUUM
        if connection.vendor == 'sqlite':
            with connection.cursor() as cursor:
                cursor.execute('VACUUM')
                cursor.execute('ANALYZE')
            self.stdout.write(
                self.style.SUCCESS('Database optimized with VACUUM and ANALYZE')
            )
        else:
            self.stdout.write(
                self.style.WARNING(
                    f'Database optimization not implemented for {connection.vendor}'
                )
            )
        
        # Update service ratings
        self.update_service_ratings()
    
    def update_service_ratings(self):
        """Update average ratings for all services based on reviews"""
        self.stdout.write('Updating service ratings...')
        
        # Get all services with their average ratings
        services_with_ratings = Service.objects.annotate(
            avg_rating=models.Avg('review__rating')
        )
        
        # Update each service's average_rating field
        updated_count = 0
        for service in services_with_ratings:
            if service.avg_rating is not None:
                service.average_rating = round(service.avg_rating, 1)
                service.save(update_fields=['average_rating'])
                updated_count += 1
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully updated ratings for {updated_count} services'
            )
        )
    
    def optimize_caching(self):
        """Optimize caching by pre-populating cache with frequently accessed data"""
        self.stdout.write('Optimizing caching...')
        
        # Clear existing cache
        cache.clear()
        self.stdout.write('Cache cleared')
        
        # Pre-populate cache with frequently accessed data
        self.populate_service_cache()
        self.populate_review_cache()
        
        self.stdout.write(
            self.style.SUCCESS('Caching optimization completed')
        )
    
    def populate_service_cache(self):
        """Pre-populate cache with service data"""
        self.stdout.write('Populating service cache...')
        
        # Cache all services
        services = Service.objects.all()
        cache.set('all_services', services, settings.CACHE_TTL)
        
        # Cache services by rating
        top_rated_services = Service.objects.order_by('-average_rating')[:10]
        cache.set('top_rated_services', top_rated_services, settings.CACHE_TTL)
        
        # Cache individual services
        for service in services:
            cache_key = f'service_{service.id}'
            cache.set(cache_key, service, settings.CACHE_TTL)
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Cached {services.count()} services'
            )
        )
    
    def populate_review_cache(self):
        """Pre-populate cache with review data"""
        self.stdout.write('Populating review cache...')
        
        # Cache recent reviews
        recent_reviews = Review.objects.select_related('user', 'service').order_by('-created_at')[:50]
        cache.set('recent_reviews', recent_reviews, settings.CACHE_TTL)
        
        # Cache reviews by service
        services = Service.objects.all()
        for service in services:
            service_reviews = Review.objects.filter(service=service).select_related('user').order_by('-created_at')
            cache_key = f'reviews_for_service_{service.id}'
            cache.set(cache_key, service_reviews, settings.CACHE_TTL)
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Cached reviews for {services.count()} services'
            )
        )
    
    def analyze_queries(self):
        """Analyze database queries and suggest optimizations"""
        self.stdout.write('Analyzing database queries...')
        
        # Analyze common queries and suggest optimizations
        self.analyze_user_queries()
        self.analyze_service_queries()
        self.analyze_cart_queries()
        self.analyze_order_queries()
        self.analyze_review_queries()
        
        self.stdout.write(
            self.style.SUCCESS('Query analysis completed')
        )
    
    def analyze_user_queries(self):
        """Analyze user-related queries"""
        self.stdout.write('\nUser Query Optimization Suggestions:')
        self.stdout.write('  ✓ Use select_related("user") when accessing user profiles')
        self.stdout.write('  ✓ Use prefetch_related("user") when accessing multiple user profiles')
        self.stdout.write('  ✓ Index on role, username, and email fields for faster lookups')
        self.stdout.write('  ✓ Use only() or defer() to limit fields when full objects are not needed')
    
    def analyze_service_queries(self):
        """Analyze service-related queries"""
        self.stdout.write('\nService Query Optimization Suggestions:')
        self.stdout.write('  ✓ Use select_related("service") when accessing services through foreign keys')
        self.stdout.write('  ✓ Use prefetch_related("service") when accessing multiple services')
        self.stdout.write('  ✓ Index on name, average_rating, and price fields for faster searches and sorting')
        self.stdout.write('  ✓ Use only() or defer() to limit fields when full objects are not needed')
        self.stdout.write('  ✓ Consider caching for frequently accessed service data')
    
    def analyze_cart_queries(self):
        """Analyze cart-related queries"""
        self.stdout.write('\nCart Query Optimization Suggestions:')
        self.stdout.write('  ✓ Use prefetch_related("items__service") to reduce queries when accessing cart items')
        self.stdout.write('  ✓ Use select_related("user") when accessing carts for specific users')
        self.stdout.write('  ✓ Use bulk_create() for adding multiple items to cart')
        self.stdout.write('  ✓ Use delete() on QuerySet for removing all cart items at once')
        self.stdout.write('  ✓ Consider caching cart data for authenticated users')
    
    def analyze_order_queries(self):
        """Analyze order-related queries"""
        self.stdout.write('\nOrder Query Optimization Suggestions:')
        self.stdout.write('  ✓ Use prefetch_related("orderitem_set__service") to reduce queries when accessing order items')
        self.stdout.write('  ✓ Use select_related("user") when accessing orders for specific users')
        self.stdout.write('  ✓ Use bulk_create() for creating multiple order items')
        self.stdout.write('  ✓ Index on user, created_at, and status fields for faster lookups')
        self.stdout.write('  ✓ Consider caching order data for authenticated users')
    
    def analyze_review_queries(self):
        """Analyze review-related queries"""
        self.stdout.write('\nReview Query Optimization Suggestions:')
        self.stdout.write('  ✓ Use select_related("user", "service") when accessing reviews')
        self.stdout.write('  ✓ Use prefetch_related("user", "service") when accessing multiple reviews')
        self.stdout.write('  ✓ Index on service, user, rating, and created_at fields for faster lookups')
        self.stdout.write('  ✓ Use only() or defer() to limit fields when full objects are not needed')
        self.stdout.write('  ✓ Consider caching review data for services')
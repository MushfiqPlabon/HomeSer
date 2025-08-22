from django.core.management.base import BaseCommand
from django.core.cache import cache
from django.db.models import Avg
from HomeSer.models import Service, Review


class Command(BaseCommand):
    help = "Run all optimizations for the HomeSer platform"

    def handle(self, *args, **options):
        # Clear all caches
        self.clear_caches()

        # Update service ratings
        self.update_service_ratings()

        # Optimize database
        self.optimize_database()

        self.stdout.write(
            self.style.SUCCESS("All optimizations completed successfully!")
        )

    def clear_caches(self):
        """Clear all caches"""
        cache.clear()
        self.stdout.write("Cleared all caches")

    def update_service_ratings(self):
        """Update average ratings for all services"""
        services = Service.objects.all()
        updated_count = 0

        for service in services:
            # Get average rating for this service
            avg_rating = Review.objects.filter(service=service).aggregate(
                avg_rating=Avg("rating")
            )["avg_rating"]

            # Update the service rating
            if avg_rating is not None:
                service.average_rating = round(float(avg_rating), 1)
                service.save(update_fields=["average_rating"])
                updated_count += 1

        self.stdout.write(
            self.style.SUCCESS(f"Updated ratings for {updated_count} services")
        )

    def optimize_database(self):
        """Run database optimization"""
        from django.db import connection

        # Update table statistics
        tables = [
            "HomeSer_user",
            "HomeSer_clientprofile",
            "HomeSer_service",
            "HomeSer_cart",
            "HomeSer_cartitem",
            "HomeSer_order",
            "HomeSer_orderitem",
            "HomeSer_review",
        ]

        with connection.cursor() as cursor:
            for table in tables:
                try:
                    cursor.execute(f"ANALYZE {table};")
                    self.stdout.write(f"Analyzed table: {table}")
                except Exception as e:
                    self.stdout.write(
                        self.style.WARNING(f"Could not analyze {table}: {str(e)}")
                    )

        self.stdout.write("Database optimization completed")

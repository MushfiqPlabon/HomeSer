from django.core.cache import cache
from django.core.management.base import BaseCommand
from django.db.models import Avg

from HomeSer.models import Review, Service


class Command(BaseCommand):
    help = "Update service ratings and clear related caches"

    def handle(self, *args, **options):
        self.stdout.write("Updating service ratings...")

        # Get all services with their average ratings
        services_with_ratings = Service.objects.annotate(
            avg_rating=Avg("review__rating")
        )

        # Update each service's average_rating field
        updated_count = 0
        for service in services_with_ratings:
            if service.avg_rating is not None:
                service.average_rating = round(service.avg_rating, 1)
                service.save()
                updated_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully updated ratings for {updated_count} services"
            )
        )

        # Clear caches for services
        self.stdout.write("Clearing service-related caches...")
        # In a real application, you might want to be more selective about which caches to clear
        # For now, we'll clear the entire cache
        cache.clear()
        self.stdout.write(self.style.SUCCESS("All caches cleared"))

        self.stdout.write(
            self.style.SUCCESS(
                "Service ratings updated and caches cleared successfully"
            )
        )

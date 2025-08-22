from django.core.management.base import BaseCommand
from django.db.models import Avg
from HomeSer.models import Service, Review


class Command(BaseCommand):
    help = "Update average ratings for all services efficiently"

    def handle(self, *args, **options):
        # Update all service ratings in a single query
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
            self.style.SUCCESS(
                f"Successfully updated ratings for {updated_count} services"
            )
        )

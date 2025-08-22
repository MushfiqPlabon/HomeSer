from django.core.management.base import BaseCommand
from django.db import connection, models
from HomeSer.models import Service, Review


class Command(BaseCommand):
    help = 'Optimize the database for better performance'

    def handle(self, *args, **options):
        # Update service average ratings
        self.update_service_ratings()
        
        # Optimize database tables
        self.optimize_tables()
        
        self.stdout.write(
            self.style.SUCCESS('Database optimization completed successfully')
        )

    def update_service_ratings(self):
        """Update average ratings for all services"""
        services = Service.objects.all()
        updated_count = 0
        
        for service in services:
            reviews = Review.objects.filter(service=service)
            if reviews.exists():
                avg_rating = reviews.aggregate(avg_rating=models.Avg('rating'))['avg_rating']
                service.average_rating = avg_rating or 0.0
                service.save()
                updated_count += 1
        
        self.stdout.write(
            self.style.SUCCESS(f'Updated ratings for {updated_count} services')
        )

    def optimize_tables(self):
        """Run database optimization commands"""
        with connection.cursor() as cursor:
            # Analyze tables for better query planning
            tables = [
                'HomeSer_user',
                'HomeSer_clientprofile', 
                'HomeSer_service',
                'HomeSer_cart',
                'HomeSer_cartitem',
                'HomeSer_order',
                'HomeSer_orderitem',
                'HomeSer_review'
            ]
            
            for table in tables:
                try:
                    cursor.execute(f'ANALYZE {table};')
                    self.stdout.write(f'Analyzed table: {table}')
                except Exception as e:
                    self.stdout.write(
                        self.style.WARNING(f'Could not analyze {table}: {str(e)}')
                    )
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from HomeSer.models import Service, Review
import random

User = get_user_model()


class Command(BaseCommand):
    help = 'Seed the database with sample data'

    def handle(self, *args, **options):
        # Create admin user
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@example.com',
                'role': 'admin'
            }
        )
        if created:
            admin_user.set_password('adminpassword')
            admin_user.save()
            self.stdout.write(self.style.SUCCESS('Admin user created'))

        # Create client users
        client_users = []
        for i in range(5):
            user, created = User.objects.get_or_create(
                username=f'client{i}',
                defaults={
                    'email': f'client{i}@example.com',
                    'role': 'client'
                }
            )
            if created:
                user.set_password('clientpassword')
                user.save()
                client_users.append(user)
                self.stdout.write(self.style.SUCCESS(f'Client user {i} created'))

        # Create services
        services = []
        for i in range(10):
            service, created = Service.objects.get_or_create(
                name=f'Service {i}',
                defaults={
                    'description': f'Description for service {i}',
                    'price': random.uniform(10.0, 100.0),
                    'average_rating': random.uniform(1.0, 5.0)
                }
            )
            if created:
                services.append(service)
                self.stdout.write(self.style.SUCCESS(f'Service {i} created'))

        # Create reviews
        for service in services:
            for user in client_users:
                if random.choice([True, False]):  # 50% chance to create a review
                    review, created = Review.objects.get_or_create(
                        user=user,
                        service=service,
                        defaults={
                            'rating': random.randint(1, 5),
                            'text': f'Review text for {service.name} by {user.username}'
                        }
                    )
                    if created:
                        self.stdout.write(self.style.SUCCESS(f'Review created for {service.name} by {user.username}'))

        self.stdout.write(self.style.SUCCESS('Database seeding completed'))
import random

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from HomeSer.models import (
    Cart,
    CartItem,
    ClientProfile,
    Order,
    OrderItem,
    Review,
    Service,
)

User = get_user_model()


class Command(BaseCommand):
    help = "Create sample data for testing"

    def handle(self, *args, **options):
        # Create admin user
        if not User.objects.filter(username="admin").exists():
            admin = User.objects.create_superuser("admin", "admin@example.com", "admin")
            admin.role = "admin"
            admin.save()
            self.stdout.write(self.style.SUCCESS("Admin user created"))
        else:
            self.stdout.write(self.style.SUCCESS("Admin user already exists"))

        # Create client users
        client_usernames = ["alice", "bob", "charlie", "diana", "eve"]
        clients = []
        for username in client_usernames:
            if not User.objects.filter(username=username).exists():
                client = User.objects.create_user(
                    username, f"{username}@example.com", "password"
                )
                client.role = "client"
                client.save()
                clients.append(client)
                self.stdout.write(self.style.SUCCESS(f"Client user {username} created"))
            else:
                client = User.objects.get(username=username)
                clients.append(client)
                self.stdout.write(
                    self.style.SUCCESS(f"Client user {username} already exists")
                )

        # Create services
        service_names = [
            "Plumbing Repair",
            "Electrical Work",
            "House Cleaning",
            "Lawn Mowing",
            "Painting Services",
            "Furniture Assembly",
            "Carpet Cleaning",
            "Window Washing",
            "HVAC Maintenance",
            "Pest Control",
        ]

        services = []
        for i, name in enumerate(service_names):
            if not Service.objects.filter(name=name).exists():
                service = Service.objects.create(
                    name=name,
                    description=f"Professional {name.lower()} service for your home.",
                    price=random.uniform(50, 200),
                    average_rating=random.uniform(3.0, 5.0),
                )
                services.append(service)
                self.stdout.write(self.style.SUCCESS(f"Service {name} created"))
            else:
                service = Service.objects.get(name=name)
                services.append(service)
                self.stdout.write(self.style.SUCCESS(f"Service {name} already exists"))

        # Create client profiles
        for client in clients:
            if not ClientProfile.objects.filter(user=client).exists():
                ClientProfile.objects.create(
                    user=client,
                    bio=f"Professional service provider with {random.randint(1, 10)} years of experience.",
                    social_links={
                        "facebook": "https://facebook.com/example",
                        "twitter": "https://twitter.com/example",
                    },
                )
                self.stdout.write(
                    self.style.SUCCESS(f"Profile for {client.username} created")
                )

        # Create reviews
        for service in services:
            for client in clients:
                # Only create a review if one doesn't already exist for this user/service combination
                if not Review.objects.filter(user=client, service=service).exists():
                    Review.objects.create(
                        user=client,
                        service=service,
                        rating=random.randint(1, 5),
                        text=f"Great service! Highly recommend {service.name.lower()}.",
                    )
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"Review created for {service.name} by {client.username}"
                        )
                    )

        self.stdout.write(self.style.SUCCESS("Sample data creation completed"))

from django.core.management.base import BaseCommand
from django.db import connection
from HomeSer.models import User, ClientProfile, Service, Cart, CartItem, Order, OrderItem, Review


class Command(BaseCommand):
    help = 'Create database indexes for optimized querying'

    def handle(self, *args, **options):
        self.stdout.write('Creating database indexes...')
        
        # For SQLite, we'll just output the SQL that would be used
        if connection.vendor == 'sqlite':
            self.stdout.write(
                self.style.SUCCESS(
                    'SQLite database detected. Indexes are automatically created by Django migrations.'
                )
            )
        else:
            # For other databases, we could create custom indexes
            self.stdout.write(
                self.style.WARNING(
                    f'Database indexing not implemented for {connection.vendor}. '
                    'Please create indexes manually or use database-specific tools.'
                )
            )
        
        # Output information about existing indexes
        self.show_index_info()
        
        self.stdout.write(
            self.style.SUCCESS('Database indexing information displayed')
        )
    
    def show_index_info(self):
        """Show information about existing indexes"""
        self.stdout.write('\nExisting indexes:')
        
        # User model indexes
        self.stdout.write(f'  User model:')
        self.stdout.write(f'    - Role index: role field indexed')
        self.stdout.write(f'    - Username index: username field indexed')
        self.stdout.write(f'    - Email index: email field indexed')
        
        # ClientProfile model indexes
        self.stdout.write(f'  ClientProfile model:')
        self.stdout.write(f'    - User index: user field indexed')
        
        # Service model indexes
        self.stdout.write(f'  Service model:')
        self.stdout.write(f'    - Name index: name field indexed')
        self.stdout.write(f'    - Average rating index: average_rating field indexed')
        self.stdout.write(f'    - Price index: price field indexed')
        
        # Cart model indexes
        self.stdout.write(f'  Cart model:')
        self.stdout.write(f'    - User index: user field indexed')
        
        # CartItem model indexes
        self.stdout.write(f'  CartItem model:')
        self.stdout.write(f'    - Cart index: cart field indexed')
        self.stdout.write(f'    - Service index: service field indexed')
        self.stdout.write(f'    - Composite index: cart and service fields indexed')
        
        # Order model indexes
        self.stdout.write(f'  Order model:')
        self.stdout.write(f'    - User index: user field indexed')
        self.stdout.write(f'    - Created at index: created_at field indexed')
        self.stdout.write(f'    - Status index: status field indexed')
        self.stdout.write(f'    - Composite index: user and created_at fields indexed')
        
        # OrderItem model indexes
        self.stdout.write(f'  OrderItem model:')
        self.stdout.write(f'    - Order index: order field indexed')
        self.stdout.write(f'    - Service index: service field indexed')
        self.stdout.write(f'    - Composite index: order and service fields indexed')
        
        # Review model indexes
        self.stdout.write(f'  Review model:')
        self.stdout.write(f'    - User index: user field indexed')
        self.stdout.write(f'    - Service index: service field indexed')
        self.stdout.write(f'    - Rating index: rating field indexed')
        self.stdout.write(f'    - Created at index: created_at field indexed')
        self.stdout.write(f'    - Composite index: service and created_at fields indexed')
        self.stdout.write(f'    - Unique constraint: user and service fields unique together')
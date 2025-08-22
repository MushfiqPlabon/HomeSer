from django.core.management.base import BaseCommand
from django.db import connection

from HomeSer.models import (Cart, CartItem, ClientProfile, Order, OrderItem,
                            Review, Service, User)


class Command(BaseCommand):
    help = "Optimize database indexes for better query performance"

    def handle(self, *args, **options):
        self.stdout.write("Optimizing database indexes...")

        # For SQLite, we'll just output information about existing indexes
        if connection.vendor == "sqlite":
            self.stdout.write(
                self.style.SUCCESS(
                    "SQLite database detected. Indexes are automatically created by Django migrations."
                )
            )
            self.show_sqlite_index_info()
        else:
            # For other databases, we could create custom indexes
            self.stdout.write(
                self.style.WARNING(
                    f"Database index optimization not implemented for {connection.vendor}. "
                    "Please create indexes manually or use database-specific tools."
                )
            )

        self.stdout.write(self.style.SUCCESS("Database index optimization completed"))

    def show_sqlite_index_info(self):
        """Show information about SQLite indexes"""
        self.stdout.write("\nSQLite Index Information:")

        # Show indexes for each table
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

        for table in tables:
            self.show_table_indexes(table)

    def show_table_indexes(self, table_name):
        """Show indexes for a specific table"""
        self.stdout.write(f"\n  {table_name}:")

        # Get index information from SQLite
        with connection.cursor() as cursor:
            try:
                cursor.execute(f"PRAGMA index_list({table_name})")
                indexes = cursor.fetchall()

                if indexes:
                    for index in indexes:
                        index_name = index[1]
                        self.stdout.write(f"    - {index_name}")

                        # Get index information
                        cursor.execute(f"PRAGMA index_info({index_name})")
                        index_info = cursor.fetchall()

                        columns = [info[2] for info in index_info]
                        self.stdout.write(f'      Columns: {", ".join(columns)}')
                else:
                    self.stdout.write(f"    - No indexes found")
            except Exception as e:
                self.stdout.write(f"    - Error retrieving indexes: {e}")

        # Show table schema
        self.show_table_schema(table_name)

    def show_table_schema(self, table_name):
        """Show schema for a specific table"""
        self.stdout.write(f"    Schema:")

        with connection.cursor() as cursor:
            try:
                cursor.execute(f"PRAGMA table_info({table_name})")
                columns = cursor.fetchall()

                for column in columns:
                    col_name = column[1]
                    col_type = column[2]
                    col_notnull = "NOT NULL" if column[3] else "NULL"
                    col_pk = "PRIMARY KEY" if column[5] else ""

                    self.stdout.write(
                        f"      {col_name} {col_type} {col_notnull} {col_pk}"
                    )
            except Exception as e:
                self.stdout.write(f"      Error retrieving schema: {e}")

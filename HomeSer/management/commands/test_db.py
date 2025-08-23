from django.core.management.base import BaseCommand
from django.conf import settings
import environ

class Command(BaseCommand):
    help = 'Test database configuration'

    def handle(self, *args, **options):
        # Test environment variables directly
        env = environ.Env(
            DATABASE_URL=(str, ""),
            user=(str, ""),
            password=(str, ""),
            host=(str, ""),
            port=(str, ""),
            dbname=(str, ""),
        )
        
        db_user = env("user", default="").strip()
        db_password = env("password", default="").strip()
        db_host = env("host", default="").strip()
        db_port = env("port", default="").strip()
        db_name = env("dbname", default="").strip()
        database_url = env("DATABASE_URL")
        
        self.stdout.write(f"Direct env read - user: '{db_user}'")
        self.stdout.write(f"Direct env read - password: '{db_password}'")
        self.stdout.write(f"Direct env read - host: '{db_host}'")
        self.stdout.write(f"Direct env read - port: '{db_port}'")
        self.stdout.write(f"Direct env read - name: '{db_name}'")
        self.stdout.write(f"Direct env read - DATABASE_URL: '{database_url}'")
        
        # Check Django settings
        db_config = settings.DATABASES['default']
        self.stdout.write(f"Settings DB Engine: {db_config['ENGINE']}")
        self.stdout.write(f"Settings DB Name: {db_config.get('NAME', 'N/A')}")
        self.stdout.write(f"Settings DB User: {db_config.get('USER', 'N/A')}")
        self.stdout.write(f"Settings DB Host: {db_config.get('HOST', 'N/A')}")
        self.stdout.write(f"Settings DB Port: {db_config.get('PORT', 'N/A')}")
        
        # Check if using PostgreSQL
        if 'postgresql' in db_config['ENGINE']:
            self.stdout.write(self.style.SUCCESS('Using PostgreSQL database'))
        elif 'sqlite3' in db_config['ENGINE']:
            self.stdout.write(self.style.WARNING('Using SQLite database'))
        else:
            self.stdout.write(self.style.NOTICE(f'Using {db_config["ENGINE"]} database'))
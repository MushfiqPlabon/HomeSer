from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site
from django.conf import settings


class Command(BaseCommand):
    help = 'Set up the site domain for email verification'

    def add_arguments(self, parser):
        parser.add_argument('--domain', type=str, help='The domain for the site')
        parser.add_argument('--name', type=str, help='The name for the site')

    def handle(self, *args, **options):
        domain = options['domain'] or ('localhost:8000' if settings.DEBUG else 'yourdomain.com')
        name = options['name'] or ('HomeSer Development' if settings.DEBUG else 'HomeSer')
        
        site = Site.objects.get_current()
        site.domain = domain
        site.name = name
        site.save()
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully set site domain to "{domain}" and name to "{name}"'
            )
        )
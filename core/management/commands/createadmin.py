from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Creates a superuser if none exists'

    def handle(self, *args, **options):
        if not User.objects.filter(username='ricky').exists():
            User.objects.create_superuser('ricky', 'ricky@example.com', 'ricky123')
            self.stdout.write(self.style.SUCCESS('Superuser created: username=ricky, password=ricky123'))
        else:
            self.stdout.write(self.style.WARNING('Superuser already exists'))

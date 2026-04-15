from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import transaction

User = get_user_model()


class Command(BaseCommand):
    help = "Populate initial sample data (safe, idempotent)"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.NOTICE("Starting sample data population..."))

        with transaction.atomic():

            # Example 1: Create admin user if none exists
            if not User.objects.filter(is_superuser=True).exists():
                User.objects.create_superuser(
                    username="admin",
                    email="admin@example.com",
                    password="admin12345"
                )
                self.stdout.write(self.style.SUCCESS("Created default admin user"))
            else:
                self.stdout.write("Admin user already exists")

            # Example 2: Create a demo user
            if not User.objects.filter(username="demo").exists():
                User.objects.create_user(
                    username="demo",
                    email="demo@example.com",
                    password="demo12345"
                )
                self.stdout.write(self.style.SUCCESS("Created demo user"))
            else:
                self.stdout.write("Demo user already exists")

        self.stdout.write(self.style.SUCCESS("Sample data population complete."))
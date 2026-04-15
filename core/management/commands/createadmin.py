from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = 'Creates default users if they do not exist'

    def handle(self, *args, **options):

        users = [
            {
                "username": "admin",
                "email": "admin@example.com",
                "password": "admin12345",
                "is_superuser": True,
                "is_staff": True,
            },
            {
                "username": "demouser",
                "email": "demo@example.com",
                "password": "demo12345",
                "is_superuser": False,
                "is_staff": False,
            },
        ]

        for u in users:
            if not User.objects.filter(username=u["username"]).exists():
                if u["is_superuser"]:
                    User.objects.create_superuser(
                        username=u["username"],
                        email=u["email"],
                        password=u["password"]
                    )
                else:
                    User.objects.create_user(
                        username=u["username"],
                        email=u["email"],
                        password=u["password"]
                    )

                self.stdout.write(
                    self.style.SUCCESS(f"Created user: {u['username']}")
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f"User already exists: {u['username']}")
                )

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_system.settings')
django.setup()

from django.contrib.auth.models import User

# Create an approver user
username = 'approver'
email = 'approver@example.com'
password = 'approver123'
first_name = 'John'
last_name = 'Approver'

# Check if user already exists
if User.objects.filter(username=username).exists():
    user = User.objects.get(username=username)
    print(f"User '{username}' already exists")
else:
    user = User.objects.create_user(
        username=username,
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name
    )
    print(f"Created user: {username}")
    print(f"Password: {password}")
    print(f"Full name: {first_name} {last_name}")
    print(f"\nYou can use this user to approve requests.")

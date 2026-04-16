from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os
import sys

class Command(BaseCommand):
    help = 'Create a superuser if one does not exist'

    def handle(self, *args, **options):
        User = get_user_model()
        
        # Get credentials from environment variables
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'admin123')
        
        self.stdout.write(self.style.WARNING(f'Attempting to create superuser with username: {username}'))
        
        try:
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_superuser(username=username, email=email, password=password)
                self.stdout.write(self.style.SUCCESS(f'Superuser "{username}" created successfully!'))
                self.stdout.write(self.style.WARNING(f'Username: {username}'))
                self.stdout.write(self.style.WARNING(f'Password: {password}'))
                self.stdout.write(self.style.WARNING(f'Email: {email}'))
                self.stdout.write(self.style.WARNING(f'Is staff: {user.is_staff}'))
                self.stdout.write(self.style.WARNING(f'Is superuser: {user.is_superuser}'))
            else:
                self.stdout.write(self.style.SUCCESS(f'Superuser "{username}" already exists.'))
                existing_user = User.objects.get(username=username)
                self.stdout.write(self.style.WARNING(f'Existing user is_staff: {existing_user.is_staff}'))
                self.stdout.write(self.style.WARNING(f'Existing user is_superuser: {existing_user.is_superuser}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error creating superuser: {str(e)}'))
            sys.exit(1)

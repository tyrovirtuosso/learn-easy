from django.utils import timezone
from usersApp.models import OneTimeToken
import os
import django
from pprint import pprint

# Set the DJANGO_SETTINGS_MODULE environment variable to your project's settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "learn_easy.settings")

# Initialize Django
django.setup()


def run():
    expired_tokens = OneTimeToken.objects.filter(expiration_date__lt=timezone.now())
    count = expired_tokens.count()
    expired_tokens.delete()
    print(f'Deleted {count} expired tokens.')
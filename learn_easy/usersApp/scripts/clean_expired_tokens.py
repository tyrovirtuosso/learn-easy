# Standard Library Imports
import os

# Third-Party Library Imports
import django
from django.utils import timezone

# Local Imports
from usersApp.models import OneTimeToken, CustomUser

# Set the DJANGO_SETTINGS_MODULE environment variable to your project's settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "learn_easy.settings")

# Initialize Django
django.setup()

def delete_expired_onetimetoken() -> None:
    """
    Delete expired OneTimeToken objects from the database.

    This function retrieves all OneTimeToken objects whose expiration_date is
    in the past and deletes them.

    Returns:
        None
    """
    expired_tokens = OneTimeToken.objects.filter(expiration_date__lt=timezone.now())
    count = expired_tokens.count()
    expired_tokens.delete()
    print(f'Deleted {count} expired tokens.')

def delete_customuser_objects() -> None:
    """
    Delete all CustomUser objects from the database.

    This function retrieves all CustomUser objects and deletes them.

    Returns:
        None
    """
    users = CustomUser.objects.all()
    users.delete()

if __name__ == "__main__":
    delete_expired_onetimetoken()
    delete_customuser_objects()

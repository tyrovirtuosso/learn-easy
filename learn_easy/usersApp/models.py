from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from uuid import uuid4
from django.utils import timezone
from datetime import timedelta
from .managers import CustomUserManager

class CustomUser(AbstractUser):
    """
    Custom user model extending Django's AbstractUser.

    Attributes:
        email (models.EmailField): The user's email address (unique).
    """
    username = None
    email = models.EmailField(_("email address"), unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        ordering = ['email']

    def __str__(self):
        return self.email

class OneTimeToken(models.Model):
    """
    Model to store one-time tokens for user authentication.

    Attributes:
        user (models.ForeignKey): The associated CustomUser.
        token (models.UUIDField): Unique token.
        expiration_date (models.DateTimeField): Token expiration date.
    """
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid4, editable=False, unique=True)
    expiration_date = models.DateTimeField(default=timezone.now() + timedelta(minutes=10))

    def is_valid(self) -> bool:
        """
        Check if the token is still valid.

        Returns:
            bool: True if the token is valid; False otherwise.
        """
        return timezone.now() < self.expiration_date

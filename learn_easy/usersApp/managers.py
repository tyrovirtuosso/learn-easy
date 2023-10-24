from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from typing import Any, Dict

class CustomUserManager(BaseUserManager):
    """
    A custom user manager for the CustomUser model.
    """

    def create_user(self, email: str, password: str, **extra_fields: Dict[str, Any]):
        """
        Create and save a user with the given email and password.

        :param email: The user's email address.
        :param password: The user's password.
        :param extra_fields: Additional fields to save with the user.
        :return: The created user.
        :raises ValueError: If email is not provided.
        """
        if not email:
            raise ValueError(_("The Email must be set"))
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email: str, password: str, **extra_fields: Dict[str, Any]):
        """
        Create and save a superuser with the given email and password.

        :param email: The superuser's email address.
        :param password: The superuser's password.
        :param extra_fields: Additional fields to save with the superuser.
        :return: The created superuser.
        :raises ValueError: If is_staff or is_superuser are not set to True.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)

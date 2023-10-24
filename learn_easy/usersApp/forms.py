from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from allauth.account.forms import SignupForm
from allauth.socialaccount.forms import SignupForm as SocialSignupForm
from django import forms
from django.http import HttpRequest
from typing import Optional

class CustomSignupForm(SignupForm):
    """
    Custom signup form for user registration without a username field.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        del self.fields['username']

    def save(self, request: Optional[HttpRequest]) -> CustomUser:
        """
        Save the user's registration data to the database.

        Args:
            request: The HTTP request object.

        Returns:
            CustomUser: The user object.
        """
        user = super().save(request)
        user.email = self.cleaned_data['email']
        user.save()
        return user

class SocialCustomSignupForm(SocialSignupForm):
    """
    Custom signup form for social accounts without a username field.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        del self.fields['username']

    def save(self, request: Optional[HttpRequest]) -> CustomUser:
        """
        Save the user's registration data to the database for social accounts.

        Args:
            request: The HTTP request object.

        Returns:
            CustomUser: The user object.
        """
        user = super().save(request)
        user.email = self.cleaned_data['email']
        user.save()
        return user

class CustomUserCreationForm(UserCreationForm):
    """
    Form for creating a CustomUser with email as the only required field.
    """
    class Meta:
        model = CustomUser
        fields = ("email",)

# A form used in the admin interface to change a user’s information and permissions.
class CustomUserChangeForm(UserChangeForm):
    """
    Form for changing a CustomUser's information and permissions in the admin interface.
    """
    class Meta:
        model = CustomUser
        fields = ("email",)

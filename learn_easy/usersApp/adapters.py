from django.http import HttpRequest
from django.forms import ModelForm
from django.contrib.auth import get_user_model

from allauth.account.adapter import DefaultAccountAdapter

User = get_user_model()


class CustomAccountAdapter(DefaultAccountAdapter):
    """
    Custom account adapter for handling user registration.

    This adapter extends the DefaultAccountAdapter from allauth.

    Attributes:
        request (HttpRequest): The HTTP request object.
        user (User): The user being saved.
        form (ModelForm): The form used for user registration.
        commit (bool): Flag indicating whether to save the user immediately.

    Returns:
        User: The saved user object.
    """
    
    def save_user(self, request: HttpRequest, user: User, form: ModelForm, commit: bool = True) -> User:
        """
        Save a user instance with custom attributes.

        Args:
            request (HttpRequest): The HTTP request object.
            user (User): The user being saved.
            form (ModelForm): The form used for user registration.
            commit (bool, optional): Flag indicating whether to save the user immediately.
                Defaults to True.

        Returns:
            User: The saved user object.
        """
        data = form.cleaned_data
        user.email = data['email']
        self.populate_username(request, user)
        if commit:
            user.save()
        return user

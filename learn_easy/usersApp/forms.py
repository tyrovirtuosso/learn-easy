from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

# Inherits from BaseUserCreationForm.
# It has three fields: username (from the user model), password1, and password2. 
# It verifies that password1 and password2 match, validates the password using validate_password(), and sets the user’s password using set_password().
# To help prevent confusion with similar usernames, the form doesn’t allow usernames that differ only in case.
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("email",)

# A form used in the admin interface to change a user’s information and permissions.
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ("email",)
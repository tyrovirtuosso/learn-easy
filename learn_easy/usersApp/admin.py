from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser

class CustomUserAdmin(BaseUserAdmin):
    """
    Admin class for the CustomUser model.
    """
    add_form = CustomUserCreationForm  # The form to use for adding users.
    form = CustomUserChangeForm  # The form to use for editing users.
    model = CustomUser  # The user model to manage.

    list_display = ("email", "is_staff", "is_active",)
    list_filter = ("email", "is_staff", "is_active",)
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_('Permissions'), {"fields": ("is_staff", "is_active", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email", "password1", "password2", "is_staff",
                "is_active", "groups", "user_permissions"
            )}
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)

# Register the CustomUser model with its admin class.
admin.site.register(CustomUser, CustomUserAdmin)

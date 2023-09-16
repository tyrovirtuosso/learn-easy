from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import CustomUser

class CustomUserAdmin(BaseUserAdmin):
    ordering = ('email',)
    
admin.site.register(CustomUser, CustomUserAdmin)

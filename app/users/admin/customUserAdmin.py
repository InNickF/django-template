"""Custom Users admin"""

# Django imports
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# App Models
from app.users.models import User


class CustomUserAdmin(admin.ModelAdmin):
    """User admin model"""
    list_display = ('email', 'username', 'first_name', 'last_name', 'is_staff', 'is_client')
    list_filter = ('is_staff', 'is_client', 'created_at', 'updated_at')


admin.site.register(User, CustomUserAdmin)

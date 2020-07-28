"""Profile Admin"""

# Django imports
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# App Models
from app.users.models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """User's profile admin model"""
    list_display = ('user', 'picture', 'reputation')

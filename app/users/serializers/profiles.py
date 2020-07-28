"""Profiles serializer"""

# Django REST Framework
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

# App imports
from app.users.models import Profile


class ProfileModelSerializer(serializers.ModelSerializer):
    """Profile model serializer"""

    class Meta:
        """Meta class"""
        model = Profile
        fields = [
            'picture',
            'biography',
            'reputation',
        ]

        read_only_fields = [
            'reputation',
        ]

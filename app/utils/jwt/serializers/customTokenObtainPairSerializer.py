"""Custom Token Obtain Pair Serializer

    This serializer is inheriting of Simple JWT's TokenObtainPairSerializer for create a token with custom claims.
"""

# Django REST Framework imports
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Custom Token Obtain Pair Serializer"""
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims here if you want

        return token

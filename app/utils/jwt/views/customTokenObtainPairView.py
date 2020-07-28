"""Custom Token Obtain Pair View

    This view use CustomTokenObtainPairSerializer for dispath a token with custom claims.
"""

# Django REST Framework imports
from rest_framework_simplejwt.views import TokenObtainPairView

# App imports
from app.utils.jwt.serializers import CustomTokenObtainPairSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    """Custom Token Obtain Pair View"""
    serializer_class = CustomTokenObtainPairSerializer

"""Verify if the request.user is the account owner"""

# Django REST Framework imports
from rest_framework.permissions import BasePermission


class IsAccountOwner(BasePermission):
    """Allow access only to objects owned by the requesting user."""

    def has_object_permission(self, request, view, obj):
        return request.user == obj

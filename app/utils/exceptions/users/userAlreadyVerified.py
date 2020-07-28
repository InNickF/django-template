"""User already verified exception

    These exceptions apply inheriting from django rest framework exceptions: APIException
"""

# Django imports
from django.utils.translation import gettext_lazy as _

# Django REST Framework
from rest_framework.exceptions import APIException
from rest_framework import status


class UserAlreadyVerified(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = _('This user is already verified.')
    default_code = 'not_acceptable'

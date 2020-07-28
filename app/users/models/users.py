"""Users Model"""

# Django imports
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

# App imports
from app.utils.models import CommonInfo


class User(CommonInfo, AbstractUser):
    """Custom user model"""

    def __str__(self):
        return self.username

    def get_short_name(self):
        return self.username

    email = models.EmailField(
        _('email'),
        unique=True,
        blank=False,
        error_messages={
            'unique': 'A user with that email already exist.'
        }
    )

    phone_regex = RegexValidator(
        regex=r'\+?1?\d{9,15}$',
        message='Phone number must be entered in the format: +999999999. Up to 25 digits allowed.'
    )

    phone_number = models.CharField(
        _('phone number'),
        max_length=17,
        validators=[phone_regex]
    )

    is_client = models.BooleanField(
        _('is client'),
        default=True,
        help_text=(
            'Help easily distinguish users and perform queries. '
            'Clients are the main type of users'
        )
    )

    verified = models.BooleanField(
        _('verified'),
        default=False,
        help_text="Set to true when the user's email is verified"
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

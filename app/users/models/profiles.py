"""Profile Model"""

# Django imports
from django.db import models
from django.utils.translation import gettext_lazy as _

# App imports
from app.utils.models import CommonInfo


class Profile(CommonInfo):
    """Profile model.

    A profile holds a user's public data like biography, picture, and statics.
    """

    class Meta:
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')

    def __str__(self):
        """Return user's string representation"""
        return str(self.user)

    user = models.OneToOneField(
        'users.User',
        verbose_name='user',
        on_delete=models.CASCADE
    )
    picture = models.ImageField(
        _('profile picture'),
        upload_to='users/pictures',
        blank=True,
        null=True
    )
    biography = models.TextField(
        _('biography'),
        max_length=500,
        blank=True
    )
    reputation = models.FloatField(
        _('reputation'),
        default=5.0,
        help_text="User's reputation."
    )

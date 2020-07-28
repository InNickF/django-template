
# Django's import
from django.db import models


class CommonInfo(models.Model):
    """Base model

    This table provides to every table the following attributes:
      + created_at (DateTime): Store the datetime when the object was created
      + updated_at (DateTime): Store the last datetime when the object was modified
    """

    class Meta:
        """Meta Options"""
        abstract = True
        get_latest_by = 'created_at'
        ordering = ['-created_at', '-updated_at']

    created_at = models.DateTimeField(
        'created_at',
        auto_now_add=True,
        help_text='Date time on which theobject was created'
    )

    updated_at = models.DateTimeField(
        'updated_at',
        auto_now=True,
        help_text='Date time on which theobject was created'
    )

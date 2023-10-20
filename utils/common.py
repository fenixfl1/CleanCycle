"""
This file contains the common models that will be inherited by all other models
"""

from django.db import models
from django.contrib.auth import get_user_model


class BaseModel(models.Model):
    """
    This is a base model that will be inherited by all other models
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        to_field="username",
        db_column="created_by",
        related_name="%(app_label)s_%(class)s_created_by",
    )
    state = models.CharField(
        max_length=1, default="A", help_text="A=Active, I=Inactive"
    )

    # this is a meta class that will be inherited by all other models
    class Meta:
        abstract = True

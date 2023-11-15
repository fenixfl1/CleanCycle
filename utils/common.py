"""
This file contains the common models that will be inherited by all other models
"""
from datetime import datetime
from typing import Type

from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

from rest_framework.exceptions import APIException

from utils.hlepers import dict_key_to_lower

Model = Type["Model"]


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
    state = models.BooleanField(max_length=1, default=True)

    # this is a meta class that will be inherited by all other models
    class Meta:
        abstract = True

    @classmethod
    def create(cls: Model, request, **kwargs) -> Model:
        try:
            data = dict_key_to_lower(kwargs)
            user = data.pop("user", None)

            data["created_by"] = user or request.user
            data["created_at"] = datetime.now()

            # pylint: disable=no-member
            return cls.objects.create(**data)
        except Exception as e:
            raise APIException(e) from e

    @classmethod
    def create_many(cls: Model, request, data_list: list) -> list[Model]:
        try:
            created_objects = []
            objects_to_create = []

            for data in data_list:
                kwargs = {
                    "created_by": request.user,
                    "created_at": datetime.now(),
                    **dict_key_to_lower(data),
                }

                obj = cls(**kwargs)
                objects_to_create.append(obj)

            if objects_to_create:
                cls.objects.bulk_create(objects_to_create)
                created_objects = objects_to_create

            return created_objects

        except Exception as e:
            raise APIException(e) from e

    @classmethod
    def update(cls: Model, request, instance, **kwargs) -> Model:
        try:
            data = dict_key_to_lower(kwargs)
            data["updated_at"] = timezone.now()

            # Update each field in data
            for field, value in data.items():
                setattr(instance, field, value)

            # Save the updated object
            instance.save()

            return instance

        except Exception as e:
            raise APIException(str(e)) from e

"""
Custom user model
"""

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    """

    def create_user(self, email, username, password, **extra_fields):
        """
        Create and save a User with the given email and password
        """

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)

        user.set_password(password)

        user.save()
        return user

    def create_superuser(self, email, username, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password
        """
        extra_fields["is_superuser"] = True
        extra_fields["is_staff"] = True

        user = self.create_user(email, username, password, **extra_fields)

        return user


class User(AbstractBaseUser):
    """
    Custom user model
    """

    user_id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True, null=False, blank=False)
    username = models.CharField(max_length=30, unique=True, null=False, blank=False)
    password = models.CharField(max_length=100, null=False, blank=False)
    avatar = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    about = models.TextField(null=True, blank=True)

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email", "password"]

    def __repr__(self) -> str:
        return f"{self.username}"

    class Meta:
        db_table = "USERS"
        ordering = ["username"]
        verbose_name = "User"

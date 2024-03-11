"""
Custom user model
"""

from django.db import models
from django.utils.html import format_html
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
    full_name = models.CharField(max_length=50, null=True, blank=True)
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

    def has_module_perms(self, app_label):
        """
        Does the user have permissions to view the app `app_label`?
        """
        return self.is_superuser

    def has_perm(self, perm, obj=None):
        """
        Does the user have a specific permission?
        """
        return self.is_superuser

    def render_avatar(self):
        if self.avatar:
            return format_html(
                '<img src="{}" width="60" height="60" style="border-radius: 50%;" />'.format(
                    self.avatar
                )
            )
        return ""

    render_avatar.short_description = "Avatar"

    class Meta:
        db_table = "users"
        ordering = ["username"]
        verbose_name = "User"


class Follow(models.Model):
    follower = models.ForeignKey(
        User,
        db_column="follower",
        on_delete=models.CASCADE,
        related_name="following",
        to_field="username",
    )
    following = models.ForeignKey(
        User,
        db_column="following",
        on_delete=models.CASCADE,
        related_name="followers",
        to_field="username",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    state = models.BooleanField(max_length=1, default=True)

    class Meta:
        db_table = "follows"
        unique_together = ("follower", "following")

    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"

    def __repr__(self):
        return f"{self.follower.username} follows {self.following.username}"

    def normalize_state(self):
        return "Following" if self.state else "Not following"

    def normalize_follower(self):
        return format_html(f"{self.follower.username}")

    def normalize_following(self):
        return format_html(f"{self.following.username}")

    normalize_state.short_description = "State"
    normalize_follower.short_description = "Follower"
    normalize_following.short_description = "Following"

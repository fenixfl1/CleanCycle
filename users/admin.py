from django import forms
from django.contrib import admin
from django.contrib.auth import password_validation
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import (
    AuthenticationForm,
    UserCreationForm,
    UserChangeForm,
)

from users.models import User


class UstomAuthForm(AuthenticationForm):
    def confirm_login_allowed(self, user: AbstractBaseUser):
        if not user.state:
            raise forms.ValidationError(
                self.error_messages["inactive"],
                code="inactive",
            )

    fields = ("username", "password")


class CustomCreationForm(UserCreationForm):
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

    class Meta(UserCreationForm):
        model = User
        fields = (
            "email",
            "username",
            "avatar",
            "about",
            "is_staff",
            "is_superuser",
        )


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = (
            "email",
            "username",
            "avatar",
            "about",
            "is_staff",
            "is_superuser",
            "password",
        )


class CustomUserAdmin(UserAdmin):
    """
    Custom user admin model for the admin site
    """

    add_form = CustomCreationForm
    login_form = UstomAuthForm
    model = User
    form = CustomUserChangeForm

    ordering = ("username",)
    display_name = "username"
    list_filter = ("is_staff", "is_superuser", "is_active")
    list_display = (
        "username",
        "email",
        "avatar",
        "about",
        "is_staff",
        "is_superuser",
        "is_active",
    )

    exclude = (
        "password",
        "created_at",
        "updated_at",
        "created_by",
    )

    filter_horizontal = ()

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Personal info",
            {
                "fields": (
                    "username",
                    "avatar",
                    "about",
                    "is_staff",
                    "is_superuser",
                    "is_active",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "created_at")}),
    )

    list_editable = ("is_staff", "is_superuser", "is_active")

    def has_module_permission(self, request):
        return request.user.is_authenticated

    def has_permission(self, request, _obj=None):
        return request.user.is_authenticated


admin.site.register(User, CustomUserAdmin)

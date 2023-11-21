from typing import Any
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth import password_validation
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.forms import (
    AuthenticationForm,
    UserCreationForm,
    UserChangeForm,
)


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
        model = get_user_model()
        fields = (
            "email",
            "username",
            "avatar",
            "about",
            "is_staff",
            "is_superuser",
        )


class CustomUserChangeForm(UserChangeForm):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        if "created_at" in self.fields:
            # Personaliza el campo 'created_at' aquí si es necesario
            pass

    class Meta:
        model = get_user_model()
        fields = "__all__"

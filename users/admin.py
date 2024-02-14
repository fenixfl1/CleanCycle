from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from django.utils.translation import gettext_lazy as _

from users.forms import CustomCreationForm, CustomUserChangeForm, UstomAuthForm
from users.models import User
from utils.common import BaseModelAdmin


class CustomUserAdmin(BaseModelAdmin):
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
        "render_avatar",
        "full_name",
        "username",
        "email",
        "about",
        "is_staff",
        "is_superuser",
        "is_active",
    )

    # exclude = ("password", +"created_at", "updated_at", "created_by")

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
        ("Important dates", {"fields": ("last_login",)}),
    )

    list_editable = ("is_staff", "is_superuser", "is_active")

    def has_module_permission(self, request):
        return request.user.is_authenticated

    def has_permission(self, request, _obj=None):
        return request.user.is_authenticated

    def __init__(
        self, model: type, admin_site: AdminSite | None, state_field="is_active"
    ) -> None:
        super().__init__(model, admin_site, state_field)


admin.site.register(User, CustomUserAdmin)

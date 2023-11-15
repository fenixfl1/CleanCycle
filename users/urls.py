from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from users import views

authenticate_user = views.AuthenticationViewSet.as_view({"post": "authenticate_user"})
register_user = views.AuthenticationViewSet.as_view({"post": "register_user"})
validate_email = views.AuthenticationViewSet.as_view({"post": "validate_email"})
validate_username = views.AuthenticationViewSet.as_view({"post": "validate_username"})

urlpatterns = [
    path("login", authenticate_user),
    path("register_user", register_user),
    path("validate_email", validate_email),
    path("validate_username", validate_username),
]

urlpatterns = format_suffix_patterns(urlpatterns)

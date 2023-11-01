from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from users import views
from core.settings import PATH_BASE

BASE_USER_URL = f"{PATH_BASE}users/"

authenticate_user = views.AuthenticationViewSet.as_view({"post": "authenticate_user"})
register_user = views.AuthenticationViewSet.as_view({"post": "register_user"})
validate_email = views.AuthenticationViewSet.as_view({"post": "validate_email"})
validate_username = views.AuthenticationViewSet.as_view({"post": "validate_username"})

urlpatterns = [
    path(f"{PATH_BASE}login", authenticate_user),
    path(f"{BASE_USER_URL}register_user", register_user),
    path(f"{BASE_USER_URL}validate_email", validate_email),
    path(f"{BASE_USER_URL}validate_username", validate_username),
]

urlpatterns = format_suffix_patterns(urlpatterns)

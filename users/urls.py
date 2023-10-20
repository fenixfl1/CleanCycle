from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from users import views
from core.settings import PATH_BASE

BASE_USER_URL = f"{PATH_BASE}users/"

authenticate_user = views.AuthenticationViewSet.as_view({"post": "authenticate_user"})

urlpatterns = [
    path(f"{PATH_BASE}login/", authenticate_user),
]

urlpatterns = format_suffix_patterns(urlpatterns)

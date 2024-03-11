from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from users import views

authenticate_user = views.AuthenticationViewSet.as_view({"post": "authenticate_user"})
register_user = views.AuthenticationViewSet.as_view({"post": "register_user"})
validate_email = views.AuthenticationViewSet.as_view({"post": "validate_email"})
validate_username = views.AuthenticationViewSet.as_view({"post": "validate_username"})
get_user = views.AuthenticationViewSet.as_view({"get": "get_user"})
change_password = views.AuthenticationViewSet.as_view({"put": "change_password"})

get_all_users = views.UserViewSet.as_view({"get": "get_all_users"})
follow_user = views.UserViewSet.as_view({"post": "follow_user"})
get_follow = views.UserViewSet.as_view({"get": "get_follow"})
update_user = views.UserViewSet.as_view({"put": "update_user"})
get_blocked_users = views.UserViewSet.as_view({"get": "get_blocked_users"})
unblock_user = views.UserViewSet.as_view({"put": "unblock_user"})

urlpatterns = [
    path("login", authenticate_user),
    path("register_user", register_user),
    path("validate_email", validate_email),
    path("validate_username", validate_username),
    path("get_user/<str:username>", get_user),
    path("get_all_users", get_all_users),
    path("follow_user", follow_user),
    path("get_follow/<str:username>", get_follow),
    path("update_user", update_user),
    path("change_password", change_password),
    path("get_blocked_users", get_blocked_users),
    path("unblock_user", unblock_user),
]

urlpatterns = format_suffix_patterns(urlpatterns)

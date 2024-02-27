from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from users import views

authenticate_user = views.AuthenticationViewSet.as_view({"post": "authenticate_user"})
register_user = views.AuthenticationViewSet.as_view({"post": "register_user"})
validate_email = views.AuthenticationViewSet.as_view({"post": "validate_email"})
validate_username = views.AuthenticationViewSet.as_view({"post": "validate_username"})
get_user = views.AuthenticationViewSet.as_view({"get": "get_user"})

get_all_users = views.UserViewSet.as_view({"get": "get_all_users"})
follow_user = views.UserViewSet.as_view({"post": "follow_user"})
unfollow_user = views.UserViewSet.as_view({"put": "unfollow_user"})
get_follow = views.UserViewSet.as_view({"get": "get_follow"})
update_user = views.UserViewSet.as_view({"put": "update_user"})

urlpatterns = [
    path("login", authenticate_user),
    path("register_user", register_user),
    path("validate_email", validate_email),
    path("validate_username", validate_username),
    path("get_user/<str:username>", get_user),
    path("get_all_users", get_all_users),
    path("follow_user", follow_user),
    path("unfollow_user", unfollow_user),
    path("get_follow", get_follow),
    path("update_user", update_user),
]

urlpatterns = format_suffix_patterns(urlpatterns)

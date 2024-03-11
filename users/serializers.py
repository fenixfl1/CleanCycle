import datetime
from django.db.models import Q
from rest_framework import serializers
from posts.models import Posts
from utils.helpers import excep
from utils.serializers import BaseModelSerializer
from rest_framework.authtoken.models import Token

from users.models import Follow, User


class UserSerializer(BaseModelSerializer):
    followers = serializers.SerializerMethodField()
    following = serializers.SerializerMethodField()
    posts = serializers.SerializerMethodField()

    def get_followers(self, user: User) -> list[str]:
        followers = Follow.objects.filter(
            Q(following=user) & Q(state=True)
        ).values_list("follower", flat=True)
        return followers

    def get_following(self, user: User) -> list[str]:
        following = Follow.objects.filter(Q(follower=user) & Q(state=True)).values_list(
            "following", flat=True
        )
        return following

    def get_posts(self, user: User) -> list[str]:
        return [post.title for post in Posts.objects.filter(author=user.username)]

    class Meta:
        model = User
        fields = (
            "user_id",
            "full_name",
            "username",
            "email",
            "about",
            "is_superuser",
            "avatar",
            "followers",
            "following",
            "posts",
        )


class FollowUserSerializer(BaseModelSerializer):
    username = serializers.SerializerMethodField()
    avatar = serializers.SerializerMethodField()
    full_name = serializers.SerializerMethodField()
    user_id = serializers.SerializerMethodField()

    def get_user_id(self, user: Follow) -> str:
        return user.follower.user_id

    def get_full_name(self, user: Follow) -> str:
        return user.follower.full_name

    def get_username(self, user: Follow) -> str:
        return user.follower.username

    def get_avatar(self, user: Follow) -> str:
        return user.following.avatar

    class Meta:
        model = Follow
        fields = (
            "user_id",
            "full_name",
            "username",
            "avatar",
        )


class FollowersSerializer(BaseModelSerializer):
    username = serializers.SerializerMethodField()
    avatar = serializers.SerializerMethodField()
    full_name = serializers.SerializerMethodField()
    user_id = serializers.SerializerMethodField()

    def get_user_id(self, user: Follow) -> str:
        return user.following.user_id

    def get_full_name(self, user: Follow) -> str:
        return user.following.full_name

    def get_username(self, user: Follow) -> str:
        return user.following.username

    def get_avatar(self, user: Follow) -> str:
        return user.following.avatar

    class Meta:
        model = Follow
        fields = (
            "user_id",
            "full_name",
            "username",
            "avatar",
        )


class LoginUserSerializer(BaseModelSerializer):
    session_cookie = serializers.SerializerMethodField()

    @excep
    def _get_token(self, user: User) -> str:
        token, _ = Token.objects.get_or_create(user=user)
        return token.key

    def _get_expiration(self) -> int:
        return datetime.datetime.now() + datetime.timedelta(days=10)

    def get_session_cookie(self, user: User) -> dict:
        return {
            "TOKEN": self._get_token(user),
            "EXPIRES_IN": self._get_expiration(),
        }

    class Meta:
        model = User
        fields = (
            "user_id",
            "username",
            "email",
            "is_superuser",
            "avatar",
            "session_cookie",
        )

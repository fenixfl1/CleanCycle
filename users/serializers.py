import datetime

from rest_framework import serializers
from posts.models import Posts
from utils.helpers import excep
from utils.serializers import BaseModelSerializer
from rest_framework.authtoken.models import Token

from users.models import User


class UserSerializer(BaseModelSerializer):
    followers = serializers.SerializerMethodField()
    following = serializers.SerializerMethodField()
    posts = serializers.SerializerMethodField()

    def get_followers(self, user: User) -> list[str]:
        return [follower.username for follower in user.followers.all()]

    def get_following(self, user: User) -> list[str]:
        return [following.username for following in user.following.all()]

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
    class Meta:
        model = User
        fields = (
            "user_id",
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

import datetime

from rest_framework import serializers
from utils.hlepers import excep
from utils.serializers import BaseModelSerializer
from rest_framework.authtoken.models import Token

from users.models import User


class LoginUserSerializer(BaseModelSerializer):
    session_cookie = serializers.SerializerMethodField()

    @excep
    def _get_token(self, user: User) -> str:
        token, _ = Token.objects.get_or_create(user=user)
        return token.key

    def _get_expires_in(self, user: User) -> int:
        return datetime.datetime.now() + datetime.timedelta(days=10)

    def get_session_cookie(self, user: User) -> dict:
        return {
            "TOKEN": self._get_token(user),
            "EXPIRES_IN": self._get_expires_in(user),
        }

    class Meta:
        model = User
        fields = ("username", "email", "is_superuser", "avatar", "session_cookie")

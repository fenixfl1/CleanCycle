from django.contrib.auth import authenticate
from django.forms.models import model_to_dict
from rest_framework.exceptions import APIException
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from users.serializers import LoginUserSerializer

from utils.hlepers import viewException


class AuthenticationViewSet(ViewSet):
    """
    User authentication viewset
    """

    permission_classes = [AllowAny]

    @viewException
    def authenticate_user(self, request):
        data = request.data
        if not data.get("username") or not data.get("password"):
            raise APIException("Username and password are required")

        username = data["username"]
        password = data["password"]

        user = authenticate(username=username, password=password)

        if not user:
            raise APIException("Invalid username or password.")

        serializer = LoginUserSerializer(user, data=model_to_dict(user))
        serializer.is_valid(raise_exception=True)

        return Response(
            {"message": f"Welcome {user.username}!", "data": serializer.data}
        )

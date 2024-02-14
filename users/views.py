from datetime import datetime
from django.contrib.auth import authenticate
from django.forms.models import model_to_dict
from rest_framework.exceptions import APIException
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from users.models import Follow, User
from users.serializers import FollowUserSerializer, LoginUserSerializer, UserSerializer

from utils.helpers import viewException


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

    @viewException
    def register_user(self, request):
        username = request.data.get("USERNAME")
        password = request.data.get("PASSWORD")
        email = request.data.get("EMAIL")

        if not username or not password or not email:
            raise APIException("Username, password and email are required")

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            full_name=request.data.get("FULL_NAME"),
            avatar=request.data.get("AVATAR"),
        )

        serializer = LoginUserSerializer(user, data=model_to_dict(user))
        serializer.is_valid(raise_exception=True)

        return Response(
            {"message": "User registered successfully!", "data": serializer.data}
        )

    @viewException
    def validate_email(self, request):
        email = request.data.get("EMAIL")

        if not email:
            raise APIException("Email is required")

        user = User.objects.filter(email=email).first()

        if user:
            raise APIException("Email already exists")

        return Response({"message": "Email is valid!"})

    @viewException
    def validate_username(self, request):
        username = request.data.get("USERNAME")

        if not username:
            raise APIException("Username is required")

        user = User.objects.filter(username=username).first()

        if user:
            raise APIException("Username already exists")

        return Response({"message": "Username is valid!"})

    @viewException
    def get_user(self, _request, username):
        user = User.objects.filter(username=username).first()

        if not user:
            raise APIException("User not found")

        serializer = UserSerializer(user, data=model_to_dict(user))
        serializer.is_valid(raise_exception=True)

        return Response({"data": serializer.data})


class UserViewSet(ViewSet):
    """
    User viewset
    """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @viewException
    def get_all_users(self, _request):
        users = User.objects.all()

        serializer = UserSerializer(users, many=True)

        return Response({"data": serializer.data})

    @viewException
    def follow_user(self, request):
        username = request.data.get("USERNAME")
        user = User.objects.filter(username=username).first()

        if not user:
            raise APIException("User not found")

        # check if user is already following
        if Follow.objects.filter(follower=request.user, following=user).exists():
            # undate the follow status
            Follow.objects.filter(follower=request.user, following=user).update(
                updated_at=datetime.now(), state=True
            )
        else:
            Follow.objects.create(
                follower=request.user, following=user, created_at=datetime.now()
            )

        return Response({"message": f"You are now following {user.username}"})

    @viewException
    def unfollow_user(self, request, username):
        user = User.objects.filter(username=username).first()

        if not user:
            raise APIException("User not found")

        Follow.objects.filter(follower=request.user, following=user).update(
            updated_at=datetime.now(), state=False
        )

        return Response({"message": f"You are no longer following {user.username}"})

    @viewException
    def get_follow(self, request):
        followers = Follow.objects.filter(follower=request.user, state=True)
        following = Follow.objects.filter(following=request.user, state=True)

        followers_serializer = FollowUserSerializer(followers, many=True)
        following_serializer = FollowUserSerializer(following, many=True)

        return Response(
            {
                "data": {
                    "followers": followers_serializer.data,
                    "following": following_serializer.data,
                },
            }
        )

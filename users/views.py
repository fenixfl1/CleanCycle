from datetime import datetime
from django.contrib.auth import authenticate
from django.db.models import Q
from django.forms.models import model_to_dict
from rest_framework.exceptions import APIException
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from posts.models import BloquedAuthor
from users.models import Follow, User
from users.serializers import (
    FollowUserSerializer,
    FollowersSerializer,
    LoginUserSerializer,
    UserSerializer,
)

from utils.helpers import dict_key_to_lower, viewException


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

    @viewException
    def change_password(self, request):
        data = request.data

        if not data.get("OLD_PASSWORD") or not data.get("NEW_PASSWORD"):
            raise APIException("Old password and new password are required")

        user = authenticate(
            username=request.user.username, password=data["OLD_PASSWORD"]
        )

        if not user:
            raise APIException("Invalid old password")

        user.set_password(data["NEW_PASSWORD"])
        user.save()

        return Response({"message": "Password changed successfully!"})


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
        if follow := Follow.objects.filter(follower=request.user, following=user):
            # undate the follow status
            Follow.objects.filter(follower=request.user, following=user).update(
                updated_at=datetime.now(),
                state=True if follow.first().state == False else False,
            )

        else:
            Follow.objects.create(
                follower=request.user, following=user, created_at=datetime.now()
            )

        return Response({"message": f"You are now following {user.username}"})

    @viewException
    def get_follow(self, request, username):

        if User.objects.filter(username=username).exists() == False:
            raise APIException("User not found")

        followers = Follow.objects.filter(Q(following=username) & Q(state=True))
        following = Follow.objects.filter(Q(follower=username) & Q(state=True))

        followers_serializer = FollowUserSerializer(followers, many=True)
        following_serializer = FollowersSerializer(following, many=True)

        return Response(
            {
                "data": {
                    "FOLLOWERS": followers_serializer.data,
                    "FOLLOWINGS": following_serializer.data,
                },
            }
        )

    @viewException
    def update_user(self, request):
        data = request.data

        if not data.get("USER_ID"):
            raise APIException("User ID is required")

        user = User.objects.filter(user_id=data["USER_ID"]).first()

        if not user:
            raise APIException("User not found")

        data.pop("USER_ID")
        data.pop("USERNAME", None)

        if data.get("EMAIL") and data.get("EMAIL") != user.email:
            if User.objects.filter(Q(email=data.get("EMAIL"))).exists():
                raise APIException("Email or username already exists")

        for key, value in dict_key_to_lower(data).items():
            setattr(user, key, value)

        user.save()

        serializer = UserSerializer(user, data=model_to_dict(user))
        serializer.is_valid(raise_exception=True)

        return Response({"data": serializer.data})

    @viewException
    def get_blocked_users(self, request):
        user = User.objects.filter(username=request.user.username).first()
        if not user:
            raise APIException("User not found")

        bloqued_users = BloquedAuthor.objects.filter(Q(username=user) & Q(state=True))

        users = User.objects.filter(
            username__in=[user.author for user in bloqued_users]
        )

        serializer = UserSerializer(users, many=True)

        return Response({"data": serializer.data})

    @viewException
    def unblock_user(self, request):
        user_bloqued = request.data.get("USERNAME")

        user = User.objects.filter(username=request.user.username).first()
        if not user:
            raise APIException("User not found")

        bloqued = User.objects.filter(username=user_bloqued).first()
        if not bloqued:
            raise APIException("User not found")

        user = BloquedAuthor.objects.filter(Q(username=user) & Q(author=bloqued))

        if not user:
            raise APIException("User not found")

        user.update(state=False)

        return Response({"message": f"{user_bloqued} has been unblocked"})

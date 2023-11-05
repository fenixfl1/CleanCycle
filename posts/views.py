from django.forms.models import model_to_dict
from django.contrib.auth import get_user_model
from django.db.models import Q

from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes,
)
from rest_framework.exceptions import APIException
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated

from posts.models import Posts, Likes, Comments
from posts.serializers import PostSerializer
from utils.hlepers import viewException
from utils.serializers import PaginationSerializer


class UnprotectedViewSet(ViewSet):
    """
    Unprotected Posts viewset for GET operations
    """

    permission_classes = [AllowAny]
    pagination_class = PaginationSerializer

    @viewException
    def get_posts_by_id(self, request, post_id):
        posts = Posts.objects.filter(post_id=post_id).first()

        if not posts:
            raise APIException(f"Article with id '{post_id}' not found")

        serializer = PostSerializer(posts, data=model_to_dict(posts))
        serializer.is_valid(raise_exception=True)

        return Response({"data": serializer.data})

    @viewException
    def get_posts_list(self, request):
        posts = Posts.objects.filter(Q(state=True) & Q(is_approved=True)).all()
        serializer = PostSerializer(posts, many=True)

        return Response({"data": serializer.data})

    @viewException
    def get_posts(self, request):
        state = request.data.get("state", None)

        posts = Posts.objects.filter(Q(state=state) & Q(is_approved=True)).all()
        serializer = PostSerializer(posts, many=True)

        return Response({"data": serializer.data})


class ProtectedViews(ViewSet):
    """
    Protected Posts viewset for CRUD operations
    """

    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    pagination_class = PaginationSerializer

    @viewException
    def create_post(self, request):
        data = request.data

        data["author"] = request.user

        post = Posts.create(request, **data)

        serializer = PostSerializer(post, data=model_to_dict(post))
        serializer.is_valid(raise_exception=True)

        return Response(
            {
                "message": f"Article with id '{post.post_id}' was created successfuly.",
                "data": serializer.data,
            }
        )

    @viewException
    def comment_post(self, request):
        data = request.data

        if not (username := data.get("USERNAME", None)):
            raise APIException("'USERNAME' is required")

        if not data.get("COMMENT", None):
            raise APIException("'COMMENT' is required")

        post = Posts.objects.get(post_id=data.get("POST_ID", None))
        user = get_user_model().objects.get(username=username)

        if not post:
            raise APIException("'POST_ID' is required")

        data["POST_ID"] = post
        data["USERNAME"] = user

        Comments.create(request, **data)

        return Response({"message": "Comment add successfuly."})

    @viewException
    def like_post(self, request):
        data = request.data

        if not (post_id := data.get("POST_ID", None)):
            raise APIException("POST_ID is required")

        if not (username := data.get("USERNAME", None)):
            raise APIException("'USERNAME' is required")

        post = Posts.objects.get(post_id=post_id)
        user = get_user_model().objects.get(username=username)

        if not user:
            raise APIException("User not found")

        if not post:
            raise APIException("Post not found")

        data["USERNAME"] = user
        data["POST_ID"] = post
        data["USER"] = user

        Likes.create(request, **data)

        serializer = PostSerializer(post, data=model_to_dict(post))
        serializer.is_valid(raise_exception=True)

        return Response({"data": serializer.data["LIKED_BY"]})

    @viewException
    def update_post(self, request):
        pass

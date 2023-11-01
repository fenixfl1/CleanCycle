from django.forms.models import model_to_dict
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework.exceptions import APIException
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from posts.models import Posts, Likes, Comments
from posts.serializers import PostSerializer

from utils.hlepers import login_required, viewException
from utils.serializers import PaginationSerializer


class PostsViewSet(ViewSet):
    """
    Posts viewset for CRUD operations
    """

    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    pagination_class = PaginationSerializer

    @viewException
    def get_posts_by_id(self, _request, post_id):
        permission_classes = [AllowAny]
        posts = Posts.objects.filter(post_id=post_id).first()

        if not posts:
            raise APIException(f"Article with id '{post_id}' not found")

        serializer = PostSerializer(posts, data=model_to_dict(posts))
        serializer.is_valid(raise_exception=True)

        return Response({"data": serializer.data})

    @viewException
    def get_posts_list(self, request):
        permission_classes = [AllowAny]
        posts = Posts.objects.filter(Q(state=True) & Q(is_approved=True)).all()
        serializer = PostSerializer(posts, many=True)

        return Response({"data": serializer.data})

    @login_required
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
    def update_post(self, request):
        pass

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

        option = data.pop("OPTION", None)

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

        if option == 1:
            data["STATE"] = 0
            like = Likes.objects.get(like_id=data.get("LIKE_ID", None))
            Likes.update(request, like, **data)
        else:
            Likes.create(request, **data)

        serializer = PostSerializer(post, data=model_to_dict(post))
        serializer.is_valid(raise_exception=True)

        return Response({"data": serializer.data["LIKED_BY"]})
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

from posts.models import BloquedAuthor, Posts, Likes, Comments, SavedPosts
from posts.serializers import CommentsSerializer, PostSerializer
from utils.helpers import viewException
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

        serializer = PostSerializer(
            posts, data=model_to_dict(posts), context={"request": request}
        )
        serializer.is_valid(raise_exception=True)

        return Response({"data": serializer.data})

    @viewException
    def get_posts_list(self, request, username=None):

        # get posts where the author is not the same as the username and the author is not bloqued (represented in the BloquedAuthor model)
        posts = Posts.objects.filter(
            ~Q(author__username=username) & Q(is_approved=True)
        ).all()

        bloqued = BloquedAuthor.objects.filter(
            Q(username=username) & Q(state=True)
        ).all()

        if bloqued:
            bloqued = [author.author.username for author in bloqued]
            posts = [post for post in posts if post.author.username not in bloqued]

        serializer = PostSerializer(posts, many=True, context={"request": request})

        return Response({"data": serializer.data})

    @viewException
    def get_posts(self, request):
        state = request.data.get("state", True)

        posts = Posts.objects.filter(Q(state=state) & Q(is_approved=True)).all()
        serializer = PostSerializer(posts, many=True, context={"request": request})

        return Response({"data": serializer.data})

    @viewException
    def get_post_comments(self, request):
        post_id = request.data.get("POST_ID", None)

        if not post_id:
            raise APIException("POST_ID is required")

        post = Posts.objects.filter(post_id=post_id).first()

        if not post:
            raise APIException("Post not found")

        comments = Comments.objects.filter(post_id=post).all()
        serializer = CommentsSerializer(comments, many=True)

        return Response({"data": serializer.data})

    @viewException
    def get_post_likes(self, request):
        post_id = request.data.get("POST_ID", None)

        if not post_id:
            raise APIException("POST_ID is required")

        post = Posts.objects.filter(post_id=post_id).first()

        if not post:
            raise APIException("Post not found")

        likes = [
            like.username.username
            for like in Likes.objects.filter(post_id=post_id).all()
        ]

        return Response({"data": likes})


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

        serializer = PostSerializer(
            post, data=model_to_dict(post), context={"request": request}
        )
        serializer.is_valid(raise_exception=True)

        return Response(
            {
                "message": f"Article with id '{post.post_id}' was created successfuly.",
                "data": serializer.data,
            }
        )

    @viewException
    def comment_post(self, request):
        """
        This method is used to comment a post\n
        `param: POST_ID` is required, it is the id of the post\n
        `param: USERNAME` is required, it is the username of the user\n
        `param: COMMENT` is required, it is the comment to be added\n
        """
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

        print("*" * 75)
        print(f"{data}")
        print("*" * 75)

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

        like = Likes.objects.filter(
            Q(username=data["USERNAME"]) & Q(post_id=post)
        ).first()

        if option == 0 and not like:
            Likes.create(request, **data)
        else:
            state = 0 if like.state else 1
            Likes.update(request, like, state=state)

        serializer = PostSerializer(post, data=model_to_dict(post))
        serializer.is_valid(raise_exception=True)

        return Response({"data": serializer.data["LIKED_BY"]})

    @viewException
    def save_post(self, request):
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

        data["username"] = user
        data["post_id"] = post
        data["user"] = user

        saved_post = SavedPosts.objects.filter(
            Q(username=data["username"]) & Q(post_id=post)
        ).first()

        if not saved_post:
            SavedPosts.create(request, **data)
        else:
            saved_post.state = False if saved_post.state else True
            SavedPosts.update(request, saved_post)

        return Response({"message": "Post saved successfuly."})

    @viewException
    def get_saved_posts(self, request):
        user = request.user

        saved_posts = SavedPosts.objects.filter(
            Q(username=user.username) & Q(state=True)
        ).all()

        posts = [post.post_id for post in saved_posts]
        serializer = PostSerializer(posts, many=True, context={"request": request})

        return Response({"data": serializer.data})

    @viewException
    def update_post(self, request):
        pass

    @viewException
    def my_posts(self, request):
        posts = Posts.objects.filter(author=request.user).all()
        serializer = PostSerializer(posts, many=True, context={"request": request})

        return Response({"data": serializer.data})

    @viewException
    def block_author(self, request):
        username = request.data.get("USERNAME", None)
        author = request.data.get("AUTHOR", None)
        reason = request.data.get("REASON", None)

        if not username:
            raise APIException("USERNAME is required")

        if not author:
            raise APIException("AUTHOR is required")

        if not reason:
            raise APIException("REAZON is required")

        user = get_user_model().objects.get(username=username)

        if not user:
            raise APIException("User not found")

        author = get_user_model().objects.get(username=author)

        if not author:
            raise APIException("Author not found")

        BloquedAuthor.create(request, username=user, author=author, reason=reason)

        return Response({"message": "Author blocked successfuly."})

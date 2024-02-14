from django.contrib.auth import get_user_model
from django.db.models import Q

from rest_framework import serializers

from posts.models import Posts, Comments, Images, PostImages, Likes, SavedPosts
from utils.helpers import excep
from utils.serializers import BaseModelSerializer


class CommentsSerializer(BaseModelSerializer):
    avatar = serializers.SerializerMethodField()

    def get_avatar(self, article: Posts) -> str:
        return article.username.avatar

    class Meta:
        model = Comments
        fields = (
            "comment_id",
            "post_id",
            "comment",
            "username",
            "avatar",
            "created_at",
        )


class PostSerializer(BaseModelSerializer):
    avatar = serializers.SerializerMethodField()
    liked_by = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    about_author = serializers.SerializerMethodField()
    saved = serializers.SerializerMethodField()

    @excep
    def get_about_author(self, post: Posts) -> str:
        user = get_user_model().objects.filter(username=post.author).first()
        return user.about

    @excep
    def get_comments(self, post: Posts) -> list:
        return Comments.objects.filter(post_id=post.post_id).count()

    def get_liked_by(self, post: Posts) -> list:
        likes = Likes.objects.filter(Q(post_id=post.post_id) & Q(state=1)).values_list(
            "username__username", flat=True
        )

        return likes

    def get_avatar(self, article: Posts) -> str:
        return article.author.avatar

    @excep
    def get_saved(self, post: Posts) -> bool:
        user = self.context.get("request").user
        return SavedPosts.objects.filter(
            Q(post_id=post.post_id) & Q(username=user)
        ).exists()

    class Meta:
        model = Posts
        fields = (
            "about_author",
            "author",
            "avatar",
            "comments",
            "content",
            "created_at",
            "front_page",
            "liked_by",
            "post_id",
            "preview_text",
            "saved",
            "title",
        )

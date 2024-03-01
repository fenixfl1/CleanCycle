from django.contrib.auth import get_user_model
from django.db.models import Q

from rest_framework import serializers

from posts.models import (
    CommentXPost,
    Posts,
    Comments,
    Images,
    SavedPosts,
)
from utils.helpers import excep
from utils.serializers import BaseModelSerializer


class CommentsSerializer(BaseModelSerializer):
    avatar = serializers.SerializerMethodField()

    def get_avatar(self, article: Posts) -> str:
        return article.created_by.avatar

    class Meta:
        model = Comments
        fields = ("comment_id", "comment", "avatar", "created_at", "created_by")


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
        return CommentXPost.objects.filter(post_id=post.post_id).count()

    def get_liked_by(self, post: Posts) -> list:
        likes = post.get_likes()
        return likes[0]

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


class ImageSerializer(BaseModelSerializer):
    class Meta:
        model = Images
        fields = ("image_id", "image", "created_at")

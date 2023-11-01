from rest_framework import serializers

from posts.models import Posts, Comments, Images, PostImages, Likes
from utils.hlepers import excep
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

    @excep
    def get_comments(self, article: Posts) -> list:
        comments = Comments.objects.filter(post_id=article.post_id).all()
        return CommentsSerializer(comments, many=True, read_only=True).data

    def get_liked_by(self, article: Posts) -> list:
        likes = Likes.objects.filter(post_id=article.post_id).values_list(
            "username__username", flat=True
        )

        return likes

    def get_avatar(self, article: Posts) -> str:
        return article.author.avatar

    class Meta:
        model = Posts
        fields = (
            "post_id",
            "title",
            "content",
            "author",
            "avatar",
            "created_at",
            "liked_by",
            "comments",
            "front_page",
        )

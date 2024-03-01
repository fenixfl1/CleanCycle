from django.contrib import admin

from posts.models import BloquedAuthor, Posts, Comments, CommentXPost, SavedPosts, Likes
from utils.common import BaseModelAdmin


class PostsAdmin(BaseModelAdmin):
    list_display = (
        "post_id",
        "normalize_front_page",
        "normalize_title",
        "normalize_content",
        "is_approved",
        "normalize_author",
        "created_at",
        "likes",
    )
    list_editable = ("is_approved",)
    list_filter = ("is_approved", "author")

    def likes(self, obj: Posts):
        _, count = obj.get_likes()

        return count


class CommentsXPostsAdmin(BaseModelAdmin):
    list_display = ("normalize_post", "normalize_comment", "created_by", "created_at")
    list_filter = ("created_at",)


class SavedPostsAdmin(BaseModelAdmin):
    list_display = ("post", "username")
    list_editable = ("state",)

    def post(self, obj: SavedPosts):
        return obj.post_id.title


class BloquedAuthorsAdmin(BaseModelAdmin):
    list_display = ("author", "username")
    list_editable = ("state",)


class CommentsAdmin(BaseModelAdmin):
    list_display = ("comment_id", "comment", "created_at", "created_by")
    list_filter = ("created_at",)


class LikesAdmin(BaseModelAdmin):
    list_display = (
        "normalize_user",
        "normalize_content_type",
        "normalize_object_id",
        "created_at",
    )
    list_filter = ("created_at", "user")


admin.site.register(Posts, PostsAdmin)
admin.site.register(CommentXPost, CommentsXPostsAdmin)
admin.site.register(SavedPosts, SavedPostsAdmin)
admin.site.register(BloquedAuthor, BloquedAuthorsAdmin)
admin.site.register(Comments, CommentsAdmin)
admin.site.register(Likes, LikesAdmin)

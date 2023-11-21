from django.contrib import admin

from posts.models import Posts, Comments
from utils.common import BaseModelAdmin


class PostsAdmin(BaseModelAdmin):
    list_display = ("post_id", "title", "is_approved", "author")
    list_editable = ("is_approved",)

    def author(self, obj: Posts):
        return obj.author.username


class CommentsAdmin(BaseModelAdmin):
    list_display = ("comment_id", "post", "comment", "username", "state")
    list_editable = ("state",)

    def post(self, obj: Comments):
        return obj.post_id.title


admin.site.register(Posts, PostsAdmin)
admin.site.register(Comments, CommentsAdmin)

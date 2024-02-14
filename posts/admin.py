from django.contrib import admin

from posts.models import BloquedAuthor, Posts, Comments, SavedPosts
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


class SavedPostsAdmin(BaseModelAdmin):
    list_display = ("post", "username")
    list_editable = ("state",)

    def post(self, obj: SavedPosts):
        return obj.post_id.title


class BloquedAuthorsAdmin(BaseModelAdmin):
    list_display = ("author", "username")
    list_editable = ("state",)


admin.site.register(Posts, PostsAdmin)
admin.site.register(Comments, CommentsAdmin)
admin.site.register(SavedPosts, SavedPostsAdmin)
admin.site.register(BloquedAuthor, BloquedAuthorsAdmin)

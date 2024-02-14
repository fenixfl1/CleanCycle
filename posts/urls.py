from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from posts import views

get_posts_by_id = views.UnprotectedViewSet.as_view({"get": "get_posts_by_id"})
get_posts_list = views.UnprotectedViewSet.as_view({"get": "get_posts_list"})
get_posts = views.UnprotectedViewSet.as_view({"post": "get_posts"})
get_post_comments = views.UnprotectedViewSet.as_view({"post": "get_post_comments"})
get_post_likes = views.UnprotectedViewSet.as_view({"post": "get_post_likes"})

create_post = views.ProtectedViews.as_view({"post": "create_post"})
update_post = views.ProtectedViews.as_view({"put": "update_post"})
comment_post = views.ProtectedViews.as_view({"post": "comment_post"})
like_post = views.ProtectedViews.as_view({"post": "like_post"})
my_posts = views.ProtectedViews.as_view({"get": "my_posts"})
save_post = views.ProtectedViews.as_view({"post": "save_post"})
get_saved_posts = views.ProtectedViews.as_view({"get": "get_saved_posts"})
block_author = views.ProtectedViews.as_view({"post": "block_author"})

urlpatterns = [
    path("get_posts_by_id/<int:post_id>", get_posts_by_id),
    path("get_posts_list/<str:username>", get_posts_list),
    path("get_posts_list/", get_posts_list),
    path("create_post", create_post),
    path("update_post", update_post),
    path("comment_post", comment_post),
    path("like_post", like_post),
    path("get_posts", get_posts),
    path("get_post_comments", get_post_comments),
    path("get_post_likes", get_post_likes),
    path("my_posts", my_posts),
    path("save_post", save_post),
    path("get_saved_posts", get_saved_posts),
    path("block_author", block_author),
]

urlpatterns = format_suffix_patterns(urlpatterns)

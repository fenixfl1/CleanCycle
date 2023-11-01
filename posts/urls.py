from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from posts import views
from core.settings import PATH_BASE

BASE_POST_URL = f"{PATH_BASE}posts/"

get_posts_by_id = views.PostsViewSet.as_view({"get": "get_posts_by_id"})
get_posts_list = views.PostsViewSet.as_view({"get": "get_posts_list"})
create_post = views.PostsViewSet.as_view({"post": "create_post"})
update_post = views.PostsViewSet.as_view({"put": "update_post"})
comment_post = views.PostsViewSet.as_view({"post": "comment_post"})
like_post = views.PostsViewSet.as_view({"post": "like_post"})

urlpatterns = [
    path(f"{BASE_POST_URL}get_posts_by_id/<int:post_id>", get_posts_by_id),
    path(f"{BASE_POST_URL}get_posts_list", get_posts_list),
    path(f"{BASE_POST_URL}create_post", create_post),
    path(f"{BASE_POST_URL}update_post", update_post),
    path(f"{BASE_POST_URL}comment_post", comment_post),
    path(f"{BASE_POST_URL}like_post", like_post),
]

urlpatterns = format_suffix_patterns(urlpatterns)

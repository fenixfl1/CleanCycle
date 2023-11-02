from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from posts import views
from core.settings import PATH_BASE

BASE_POST_URL = f"{PATH_BASE}posts/"

urlpatterns = [
    path(f"{BASE_POST_URL}get_posts_by_id/<int:post_id>", views.get_posts_by_id),
    path(f"{BASE_POST_URL}get_posts_list", views.get_posts_list),
    path(f"{BASE_POST_URL}create_post", views.create_post),
    path(f"{BASE_POST_URL}update_post", views.update_post),
    path(f"{BASE_POST_URL}comment_post", views.comment_post),
    path(f"{BASE_POST_URL}like_post", views.like_post),
]

urlpatterns = format_suffix_patterns(urlpatterns)

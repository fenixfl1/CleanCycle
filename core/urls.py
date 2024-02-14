from django.contrib import admin
from django.urls import include, path
from core.settings import PATH_BASE


urlpatterns = [
    path(f"{PATH_BASE}admin/", admin.site.urls),
    path(f"{PATH_BASE}users/", include("users.urls")),
    path(f"{PATH_BASE}posts/", include("posts.urls")),
    path(f"{PATH_BASE}recycling_points/", include("recycling.urls")),
    path(f"{PATH_BASE}exchanges/", include("exchanges.urls")),
]

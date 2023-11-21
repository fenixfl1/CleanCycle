from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from recycling import views


get_cities_info_list = views.PublicViewSet.as_view({"post": "get_cities_info_list"})
get_recycling_points = views.PublicViewSet.as_view({"post": "get_recycling_points"})
get_routes = views.PublicViewSet.as_view({"post": "get_routes"})
get_cycling_point_by_city = views.PublicViewSet.as_view(
    {"get": "get_cycling_point_by_city"}
)

urlpatterns = [
    path("get_cities_info_list", get_cities_info_list),
    path("get_recycling_points", get_recycling_points),
    path("get_routes", get_routes),
    path("get_cycling_point_by_city/<str:city_id>", get_cycling_point_by_city),
]

urlpatterns = format_suffix_patterns(urlpatterns)

from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns


from exchanges import views

get_exchange_item = views.PublicViewSet.as_view({"get": "get_exchange_item"})
get_exchange_items = views.PublicViewSet.as_view({"post": "get_exchange_items"})
get_tags = views.PublicViewSet.as_view({"get": "get_tags"})
get_exchange_item_likes = views.PublicViewSet.as_view(
    {"get": "get_exchange_item_likes"}
)
get_exchange_item_proposals = views.PublicViewSet.as_view(
    {"get": "get_exchange_item_proposals"}
)
get_exchange_item_comments = views.PublicViewSet.as_view(
    {"get": "get_exchange_item_comments"}
)

create_exchange_item = views.ProtectedViewSet.as_view({"post": "create_exchange_item"})
update_exchange_item = views.ProtectedViewSet.as_view({"put": "update_exchange_item"})
create_tag = views.ProtectedViewSet.as_view({"post": "create_tag"})
add_exchange_item_proposal = views.ProtectedViewSet.as_view(
    {"post": "add_exchange_item_proposal"}
)
add_comment_to_exchange_item = views.ProtectedViewSet.as_view(
    {"post": "add_comment_to_exchange_item"}
)
like_exchange_item = views.ProtectedViewSet.as_view({"post": "like_exchange_item"})


urlpatterns = [
    path("get_exchange_item/<int:item_id>", get_exchange_item),
    path("get_exchange_items", get_exchange_items),
    path("get_tags", get_tags),
    path("get_exchange_item_proposals/<int:item_id>", get_exchange_item_proposals),
    path("create_exchange_item", create_exchange_item),
    path("update_exchange_item/<int:item_id>", update_exchange_item),
    path("create_tag", create_tag),
    path("add_exchange_item_proposal", add_exchange_item_proposal),
    path("get_exchange_item_comments/<int:item_id>", get_exchange_item_comments),
    path("add_comment_to_exchange_item", add_comment_to_exchange_item),
    path("like_exchange_item", like_exchange_item),
    path("get_exchange_item_likes/<int:item_id>", get_exchange_item_likes),
]

urlpatterns = format_suffix_patterns(urlpatterns)

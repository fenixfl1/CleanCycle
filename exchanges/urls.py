from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns


from exchanges import views

get_exchange_item = views.PublicViewSet.as_view({"get": "get_exchange_item"})
get_exchange_items = views.PublicViewSet.as_view({"post": "get_exchange_items"})
get_tags = views.PublicViewSet.as_view({"get": "get_tags"})
get_exchange_item_proposals = views.PublicViewSet.as_view(
    {"get": "get_exchange_item_proposals"}
)

create_exchange_item = views.ProtectedViewSet.as_view({"post": "create_exchange_item"})
update_exchange_item = views.ProtectedViewSet.as_view({"put": "update_exchange_item"})
create_tag = views.ProtectedViewSet.as_view({"post": "create_tag"})
add_exchange_item_proposal = views.ProtectedViewSet.as_view(
    {"post": "add_exchange_item_proposal"}
)
react_to_exchange_item = views.ProtectedViewSet.as_view(
    {"react_to_exchange_item": "react_to_exchange_item"}
)


urlpatterns = [
    path("get_exchange_item/<int:item_id>", get_exchange_item),
    path("get_exchange_items", get_exchange_items),
    path("get_tags", get_tags),
    path("get_exchange_item_proposals/<int:item_id>", get_exchange_item_proposals),
    path("create_exchange_item", create_exchange_item),
    path("update_exchange_item/<int:item_id>", update_exchange_item),
    path("create_tag", create_tag),
    path("react_to_exchange_item", react_to_exchange_item),
    path("add_exchange_item_proposal", add_exchange_item_proposal),
]

urlpatterns = format_suffix_patterns(urlpatterns)

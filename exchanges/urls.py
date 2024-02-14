from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns


from exchanges import views

get_exchange_item = views.PublicViewSet.as_view({"get": "get_exchange_item"})
get_exchange_items = views.PublicViewSet.as_view({"post": "get_exchange_items"})

create_exchange_item = views.ProtectedViewSet.as_view({"post": "create_exchange_item"})
create_tag = views.ProtectedViewSet.as_view({"post": "create_tag"})
update_exchange_item = views.ProtectedViewSet.as_view({"put": "update_exchange_item"})


urlpatterns = [
    path("get_exchange_item/<int:item_id>", get_exchange_item),
    path("get_exchange_items", get_exchange_items),
    path("create_exchange_item", create_exchange_item),
    path("update_exchange_item/<int:item_id>", update_exchange_item),
    path("create_tag", create_tag),
]

urlpatterns = format_suffix_patterns(urlpatterns)

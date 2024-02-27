from django.contrib import admin
from exchanges.models import (
    ExchangesItems,
    ExhangeProposal,
    ImagesXExchangesItems,
    Reactions,
    Tags,
)
from utils.common import BaseModelAdmin


class ExchangesItemsAdmin(BaseModelAdmin):
    list_display = (
        "exchange_item_id",
        "item_name",
        "description",
        "item_owner",
        "item_state",
        "get_tags",  # Usamos un método en lugar de tags directamente
        "created_at",
    )
    search_fields = ("item_name", "description", "created_by__username", "tags__name")
    list_filter = ("state", "item_state", "tags", "created_at", "updated_at")

    # Método para obtener los tags como cadena
    def get_tags(self, obj):
        return ", ".join(tag.name for tag in obj.tags.all())

    get_tags.short_description = (
        "Tags"  # Nombre que se mostrará en el encabezado de la columna
    )

    # Método para obtener el nombre del propietario del artículo
    def item_owner(self, obj):
        return obj.created_by.username


class TagsAdmin(BaseModelAdmin):
    list_display = ("tag_id", "name", "description")
    search_fields = ("name", "description")
    list_filter = ("name", "description")


class ReactionsAdmin(BaseModelAdmin):
    list_display = ("reaction_id", "reaction", "exchange_item")
    search_fields = ("reaction", "exchange_item")
    list_filter = ("reaction", "exchange_item")


class ExhangeProposalAdmin(BaseModelAdmin):
    list_display = ("item_offered", "desired_item")
    search_fields = ("desired_item", "status")
    list_filter = ("state", "created_at")


class ImagesXExchangesItemsAdmin(BaseModelAdmin):
    list_display = ("image_id", "exchange_item_id", "created_by")
    search_fields = ("image_id", "exchange_item_id", "created_by")


admin.site.register(Tags, TagsAdmin)
admin.site.register(ExchangesItems, ExchangesItemsAdmin)
admin.site.register(Reactions, ReactionsAdmin)
admin.site.register(ExhangeProposal, ExhangeProposalAdmin)
admin.site.register(ImagesXExchangesItems, ImagesXExchangesItemsAdmin)

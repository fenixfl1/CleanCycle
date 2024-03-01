from django.contrib import admin
from exchanges.models import (
    CommentXExchangesItems,
    ExchangesItems,
    ExhangeProposal,
    ImagesXExchangesItems,
    Tags,
)
from posts.models import Comments
from utils.common import BaseModelAdmin


class ExchangesItemsAdmin(BaseModelAdmin):
    list_display = (
        "exchange_item_id",
        "item_name",
        "description",
        "item_owner",
        "item_state",
        "contact_type",
        "contact",
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


class ExhangeProposalAdmin(BaseModelAdmin):
    list_display = (
        "normalize_item_offered",
        "normalize_desired_item",
        "normalize_proposal_state",
        "created_at",
    )
    search_fields = ("desired_item", "item_offered")
    list_filter = ("state", "created_at")


class ImagesXExchangesItemsAdmin(BaseModelAdmin):
    list_display = ("image_id", "exchange_item_id", "created_by")
    search_fields = ("image_id", "exchange_item_id", "created_by")


class CommentXExchangesItemsAdmin(BaseModelAdmin):
    list_display = (
        "normalize_comment",
        "normalize_exchange_item",
        "created_at",
        "created_by",
    )
    search_fields = ("comment_id", "created_at", "created_by")
    list_filter = ("created_at",)

    filter_horizontal = ()


admin.site.register(Tags, TagsAdmin)
admin.site.register(ExchangesItems, ExchangesItemsAdmin)
admin.site.register(ExhangeProposal, ExhangeProposalAdmin)
admin.site.register(ImagesXExchangesItems, ImagesXExchangesItemsAdmin)
admin.site.register(CommentXExchangesItems, CommentXExchangesItemsAdmin)

from django.contrib.auth import get_user_model
from django.db.models import Q
from django.forms import model_to_dict

from rest_framework import serializers

from exchanges.models import (
    ExchangesItems,
    ExhangeProposal,
    ImagesXExchangesItems,
    Reactions,
    Tags,
)
from posts.models import Images
from posts.serializers import ImageSerializer
from utils.serializers import BaseModelSerializer


class TagSerializer(BaseModelSerializer):
    class Meta:
        model = Tags
        fields = ("tag_id", "name", "description", "created_at", "state")


class ExchangeItemSerializer(BaseModelSerializer):
    tags = serializers.SerializerMethodField()
    reactions = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()
    avatar = serializers.SerializerMethodField()

    def get_avatar(self, item: ExchangesItems) -> str:
        return item.created_by.avatar

    def get_images(self, item: ExchangesItems) -> list:
        images = Images.objects.raw(
            """
                SELECT * FROM images WHERE image_id IN (
                    SELECT image_id FROM images_x_exchange_items WHERE exchange_item_id = %s
                )
            """,
            [item.exchange_item_id],
        )

        serializer: list[dict] = ImageSerializer(images, many=True).data

        values = [image["IMAGE"] for image in serializer]

        return values

    def get_reactions(self, item: ExchangesItems) -> dict:
        # get the likes and dislikes for the item and return a dict with the count of each and the users that liked or disliked the item
        likes = Reactions.objects.filter(
            Q(exchange_item=item.exchange_item_id) & Q(reaction=1)
        ).values_list("created_by__username", flat=True)
        dislikes = Reactions.objects.filter(
            Q(exchange_item=item.exchange_item_id) & Q(reaction=2)
        ).values_list("created_by__username", flat=True)

        return {
            "LIKES": {"COUNT": len(likes), "USER": likes},
            "DISLIKES": {"COUNT": len(dislikes), "USER": dislikes},
        }

    def get_tags(self, item: ExchangesItems) -> list:
        return item.tags.values_list("name", flat=True)

    class Meta:
        model = ExchangesItems
        fields = (
            "exchange_item_id",
            "created_by",
            "item_name",
            "description",
            "tags",
            "reactions",
            "created_at",
            "images",
            "avatar",
        )

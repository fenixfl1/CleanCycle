from django.contrib.auth import get_user_model
from django.db.models import Q

from rest_framework import serializers

from exchanges.models import (
    ExchangesItems,
    ExhangeProposal,
    ImagesXExchangesItems,
    Reactions,
    Tags,
)
from posts.models import Images
from utils.serializers import BaseModelSerializer


class TagSerializer(BaseModelSerializer):
    class Meta:
        model = Tags
        fields = ("tag_id", "name", "description", "created_at", "state")


class ExchangeItemSerializer(BaseModelSerializer):
    tags = serializers.SerializerMethodField()
    reactions = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()

    def get_images(self, item: ExchangesItems) -> list:
        images_id = ImagesXExchangesItems.objects.filter(
            exchange_item_id=item.exchange_item_id
        ).values_list("image_id__image", flat=True)

        images = Images.objects.filter(image_id__in=images_id).values_list(
            "image", flat=True
        )

        return images

    def get_reactions(self, item: ExchangesItems) -> dict:
        # get the likes and dislikes for the item and return a dict with the count of each and the users that liked or disliked the item
        likes = Reactions.objects.filter(
            Q(exchange_item=item.exchange_item_id) & Q(reaction=1)
        ).values_list("created_by__username", flat=True)
        dislikes = Reactions.objects.filter(
            Q(exchange_item=item.exchange_item_id) & Q(reaction=2)
        ).values_list("created_by__username", flat=True)

        return {
            "likes": {"count": len(likes), "users": likes},
            "dislikes": {"count": len(dislikes), "users": dislikes},
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
        )

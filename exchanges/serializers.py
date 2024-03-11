from django.contrib.auth import get_user_model
from django.db.models import Q
from django.forms import model_to_dict

from rest_framework import serializers

from exchanges.models import (
    ExchangesItems,
    ExhangeProposal,
    ImagesXExchangesItems,
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
    images = serializers.SerializerMethodField()
    avatar = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()

    def get_comment_count(self, item: ExchangesItems) -> int:
        return item.exchange_item_comment.count()

    def get_likes(self, item: ExchangesItems) -> str:
        likes = item.get_likes()
        return likes[0]

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

    def get_tags(self, item: ExchangesItems) -> list:
        return item.tags.values_list("name", flat=True)

    class Meta:
        model = ExchangesItems
        fields = (
            "exchange_item_id",
            "created_by",
            "item_name",
            "description",
            "likes",
            "tags",
            "created_at",
            "images",
            "contact_type",
            "contact",
            "comment_count",
            "avatar",
        )

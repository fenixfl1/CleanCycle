from django.db import models

from utils.common import BaseModel


class Tags(BaseModel):
    """
    Thsi model represent the tags for the exhange items
    `TABLE`:  tags
    """

    tag_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20, null=False, blank=False, unique=True)
    description = models.TextField()

    class Meta:
        db_table = "tags"
        verbose_name = "tag"
        verbose_name_plural = "tags"
        ordering = ["name"]


class ExchangesItems(BaseModel):
    """
    This model represent the items the users want to exchange with other users
    `TABLE`: exchanges_items
    """

    ITEM_STATE_CHOICES = ((1, "Nuevo"), (2, "Usado, Como nuevo"), (3, "Usado"))

    exchange_item_id = models.AutoField(primary_key=True)
    item_name = models.CharField(max_length=150, null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    tags = models.ManyToManyField(Tags, db_column="tags")
    item_state = models.IntegerField(
        null=False, blank=False, default=3, choices=ITEM_STATE_CHOICES
    )

    class Meta:
        db_table = "exchanges_items"
        verbose_name = "Exchange Item"
        verbose_name_plural = "Exchange Items"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.item_name

    def __repr__(self) -> str:
        return self.item_name

    def add_images(self, image: dict, request) -> None:
        """
        This method add images to the exchange item
        """
        ImagesXExchangesItems.objects.create(
            image_id=image, exchange_item_id=self, created_by=request.user
        )


class Reactions(BaseModel):
    """
    This model represent the reactions for the exhange items
    `TABLE`: reactions
    """

    REACTION_CHOICES = ((1, "Like"), (2, "Dislike"))

    reaction_id = models.AutoField(primary_key=True)
    reaction = models.IntegerField(null=False, blank=False, choices=REACTION_CHOICES)
    exchange_item = models.ForeignKey(
        ExchangesItems,
        db_column="exchange_item",
        on_delete=models.CASCADE,
        related_name="exchange_item_reaction",
    )

    class Meta:
        db_table = "reactions"
        verbose_name = "Reaction"
        verbose_name_plural = "Reactions"


class ExhangeProposal(BaseModel):
    """
    This model represent the exhange proposal for a particular item
    `TABLE`: exchage_proposal
    """

    item_offered = models.ForeignKey(
        ExchangesItems,
        db_column="item_offered",
        on_delete=models.CASCADE,
        related_name="item_offered",
    )
    desired_item = models.ForeignKey(
        ExchangesItems,
        db_column="desired_item",
        on_delete=models.CASCADE,
        related_name="desired_item",
    )

    class Meta:
        db_table = "exchage_proposal"
        verbose_name = "Exchange proposal"
        constraints = [
            models.UniqueConstraint(
                fields=["item_offered", "desired_item"], name="pk_exchage_proposal"
            )
        ]


class ImagesXExchangesItems(BaseModel):
    """
    This model represent the relationshiop between the Exhange item and the image table
    `TBALE`: images_x_exchange_items
    """

    image_id = models.ForeignKey(
        "posts.Images",
        db_column="image_id",
        on_delete=models.CASCADE,
        related_name="exchange_items_image",
        to_field="image_id",
    )

    exchange_item_id = models.ForeignKey(
        ExchangesItems,
        db_column="exchange_item_id",
        on_delete=models.CASCADE,
        related_name="exchange_items_image",
        to_field="exchange_item_id",
    )

    class Meta:
        db_table = "images_x_exchange_items"
        verbose_name = "Image for exchange item"
        verbose_name_plural = "Images for exchange items"
        ordering = ["image_id"]

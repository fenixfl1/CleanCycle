from django.db import IntegrityError, models
from django.db.models import Q
from django.utils.html import format_html
from django.contrib.contenttypes.models import ContentType

from posts.models import Comments, Likes
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
    contact = models.CharField(max_length=100, null=True, blank=True)
    contact_type = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        default="phone",
        choices=(("phone", "Phone"), ("email", "Email")),
    )
    item_state = models.IntegerField(
        null=True, blank=False, default=3, choices=ITEM_STATE_CHOICES
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

    def get_likes(self):
        """
        This method return the list of usernames that liked the post and the count of likes
        """
        post_content_type = ContentType.objects.get_for_model(self)
        likes = Likes.objects.filter(
            Q(content_type=post_content_type)
            & Q(object_id=self.exchange_item_id)
            & Q(state=True)
        )

        count = likes.count()

        # Obtener la lista de nombres de usuario que dieron like
        liked_usernames = [like.user.username for like in likes]

        return (liked_usernames, count)

    def like_exchange_item(self, user):
        """
        This method allows to like a exchange item
        """
        try:
            item_content_type = ContentType.objects.get_for_model(self)
            like = Likes.objects.create(
                content_type=item_content_type,
                object_id=self.exchange_item_id,
                user=user,
                created_by=user,
            )
            return like
        except IntegrityError:
            # update the like state
            like = Likes.objects.get(
                content_type=item_content_type,
                object_id=self.exchange_item_id,
                user=user,
            )

            like.state = False if like.state else True

            like.save()

            return like


class CommentXExchangesItems(BaseModel):
    """
    This model represent the relationship between the exchange items and the commnets
    `TABLE`: comments_x_exchange_items
    """

    comment_id = models.ForeignKey(
        "posts.Comments",
        db_column="comment_id",
        on_delete=models.CASCADE,
        related_name="exchange_item_comment",
        to_field="comment_id",
    )

    exchange_item_id = models.ForeignKey(
        ExchangesItems,
        db_column="exchange_item_id",
        on_delete=models.CASCADE,
        related_name="exchange_item_comment",
        to_field="exchange_item_id",
    )

    def __str__(self) -> str:
        return f"{self.comment_id} - {self.exchange_item_id}"

    def __repr__(self) -> str:
        return f"{self.comment_id} - {self.exchange_item_id}"

    def normalize_comment(self) -> str:
        return format_html(f"{self.comment_id.comment[:50]}...")

    def normalize_exchange_item(self) -> str:
        return format_html(f"{self.exchange_item_id.item_name[:50]}...")

    @classmethod
    def add_comment(cls, comment: Comments, item: ExchangesItems, user) -> bool:
        """
        This method adds a comment to the exchange item
        """
        # Crear el objeto CommentsXExchangesItems
        comment_exchange_item = cls.objects.create(
            comment_id=comment,
            exchange_item_id=item,
            created_by=user,
        )

        # Retornar True si el comentario fue creado correctamente
        return True if comment_exchange_item else False

    normalize_comment.short_description = "Comment"
    normalize_exchange_item.short_description = "Exchange Item"

    class Meta:
        db_table = "comments_x_exchange_items"
        verbose_name = "Comment for exchange item"
        verbose_name_plural = "Comments for exchange items"
        ordering = ["comment_id"]


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
    proposal_state = models.BooleanField(default=False)

    class Meta:
        db_table = "exchage_proposal"
        verbose_name = "Exchange proposal"
        constraints = [
            models.UniqueConstraint(
                fields=["item_offered", "desired_item"], name="pk_exchage_proposal"
            )
        ]

    def __str__(self) -> str:
        return f"{self.item_offered} - {self.desired_item}"

    def __repr__(self) -> str:
        return f"{self.item_offered} - {self.desired_item}"

    def normalize_item_offered(self) -> str:
        return format_html(f"{self.item_offered.item_name[:50]}...")

    def normalize_desired_item(self) -> str:
        return format_html(f"{self.desired_item.item_name[:50]}...")

    def normalize_proposal_state(self) -> str:
        return "Accepted" if self.proposal_state else "Pending"

    normalize_item_offered.short_description = "Item offered"
    normalize_desired_item.short_description = "Desired item"
    normalize_proposal_state.short_description = "Proposal state"

    @classmethod
    def add_proposal(
        cls, item: "ExhangeProposal", proposal: "ExhangeProposal", user
    ) -> "ExhangeProposal":
        """
        This method add a proposal to the exchange item
        """
        proposal = ExhangeProposal.objects.create(
            item_offered=proposal, desired_item=item, created_by=user
        )

        return proposal


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

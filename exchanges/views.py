from functools import reduce
from operator import and_
from django.contrib.auth import get_user_model
from django.forms.models import model_to_dict
from django.db.models import Q

from rest_framework.exceptions import APIException
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from exchanges.models import (
    CommentXExchangesItems,
    ExchangesItems,
    ExhangeProposal,
    Tags,
)
from exchanges.serializers import ExchangeItemSerializer, TagSerializer
from posts.models import Comments, Images, Likes
from posts.serializers import CommentsSerializer
from utils.helpers import viewException
from utils.serializers import PaginationSerializer


class PublicViewSet(ViewSet):
    """
    Public viewset for the exchanges app, you only can get the data
    """

    permission_classes = [AllowAny]
    pagination_class = PaginationSerializer

    @viewException
    def get_exchange_item(self, request, item_id):
        """
        This method return the exchange item with the given id
        """
        exchange_item = ExchangesItems.objects.filter(exchange_item_id=item_id).first()

        serializer = ExchangeItemSerializer(
            exchange_item,
            data=model_to_dict(exchange_item),
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)

        return Response({"data": serializer.data})

    @viewException
    def get_exchange_items(self, request):
        """
        This method return the exchange items\n
        `METHOD`: POST\n
        """

        conditions: list[dict] = request.data.get("conditions", None)

        if conditions is not None:
            filter = reduce(
                and_, [Q(**{key: value}) for key, value in conditions.items()]
            )
        else:
            filter = Q(state=True)

        exchange_items = ExchangesItems.objects.filter(filter).all()

        serializer = ExchangeItemSerializer(
            exchange_items, many=True, context={"request": request}
        )

        return Response({"data": serializer.data})

    @viewException
    def get_exchange_item_proposals(self, request, item_id):
        """
        This method return the proposals for the exchange item with the given id
        """

        statement = f"""
            SELECT * FROM exchanges_items WHERE exchange_item_id IN (
                SELECT item_offered FROM exchage_proposal WHERE desired_item = {item_id}
            )
        """

        items = ExchangesItems.objects.raw(statement)

        serializer = ExchangeItemSerializer(
            items, many=True, context={"request": request}
        )

        return Response({"data": serializer.data})

    @viewException
    def get_exchange_item_likes(self, request, item_id):
        """
        This method return the likes for the exchange item with the given id\n
        `METHOD`: GET\n
        """
        item = ExchangesItems.objects.filter(exchange_item_id=item_id).first()
        likes, count = item.get_likes()

        return Response({"data": {"LIKES": likes, "COUNT": count}})

    @viewException
    def get_tags(self, request):
        """
        This method return the tags\n
        `METHOD`: GET\n
        """
        tags = Tags.objects.filter(state=True).all()

        serializer = TagSerializer(tags, many=True)

        return Response({"data": serializer.data})

    @viewException
    def get_exchange_item_comments(self, request, item_id):
        """
        This method return the comments for the exchange item width the given id\n
        `METHOD`: GET\n
        """
        data = request.data

        item_comments = CommentXExchangesItems.objects.filter(exchange_item_id=item_id)
        comments = Comments.objects.filter(
            comment_id__in=[comment.comment_id.comment_id for comment in item_comments]
        )

        serializer = CommentsSerializer(comments, many=True)

        return Response({"data": serializer.data})


class ProtectedViewSet(ViewSet):
    """
    Protected viewset for the exchanges app, you can get and post data
    """

    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    pagination_class = PaginationSerializer

    @viewException
    def create_exchange_item(self, request):
        """
        This method creates a new exchange item\n
        `METHOD`: POST\n
        """
        data = request.data
        tags = data.pop("TAGS", None)
        images = data.pop("IMAGES", None)

        if not data.get("ITEM_NAME"):
            raise APIException("Name is required")

        if not data.get("DESCRIPTION"):
            raise APIException("Description is required")

        if tags is not None and not isinstance(tags, list):
            raise APIException("Tags must be a list")

        # Create the exchange item
        exchange_item = ExchangesItems.create(request, **data)

        if exchange_item is None:
            raise APIException("An error occurred while creating the item")

        if tags is not None:
            tag_objects = [Tags.objects.get(tag_id=tag) for tag in tags]
            exchange_item.tags.set(tag_objects)

        # Add images if provided
        if images is not None:

            for image in images:
                img = Images.create(request, **image)
                exchange_item.add_images(img, request)

        # Serialize the exchange item and return the response
        serializer = ExchangeItemSerializer(
            exchange_item,
            data=model_to_dict(exchange_item),
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)

        return Response({"data": serializer.data})

    @viewException
    def update_exchange_item(self, request, item_id):
        """
        This method update the exchange item with the given id\n
        `METHOD`: PUT\n
        """
        data = request.data
        tags = data.pop("TAGS", None)
        images: dict = data.pop("IMAGES", None)

        if not data.get("ITEM_NAME"):
            raise APIException("Name is required")

        if not data.get("DESCRIPTION"):
            raise APIException("Description is required")

        if (tags is not None) and (not isinstance(tags, list)):
            raise APIException("Tags must be a list")

        exchange_item = ExchangesItems.objects.filter(exchange_item_id=item_id).first()

        if exchange_item is None:
            raise APIException("The item does not exist")

        exchange_item = ExchangesItems.update(request, exchange_item, **data)

        if exchange_item is None:
            raise APIException("An error occurred while updating the item")

        if images is not None:
            images = Images.create(request, **images)
            exchange_item.add_images(images, request)

        serializer = ExchangeItemSerializer(
            exchange_item,
            data=model_to_dict(exchange_item),
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)

        return Response({"data": serializer.data})

    @viewException
    def add_exchange_item_proposal(self, request):
        """
        This method add a proposal to the exchange item with the given id\n
        `METHOD`: POST\n
        """

        item_id = request.data.get("ITEM_ID", None)
        proposal_item_id = request.data.get("PROPOSAL_ITEM_ID", None)

        if item_id is None:
            raise APIException("The item id is required")

        if proposal_item_id is None:
            raise APIException("The proposal item id is required")

        desired_item = ExchangesItems.objects.filter(exchange_item_id=item_id).first()
        proposal_item = ExchangesItems.objects.filter(
            exchange_item_id=proposal_item_id
        ).first()

        if desired_item is None:
            raise APIException("The item does not exist")

        if proposal_item is None:
            raise APIException("The proposal item does not exist")

        proposal = ExhangeProposal.add_proposal(
            desired_item, proposal_item, request.user
        )

        if proposal is None:
            raise APIException("An error occurred while creating the proposal")

        return Response({"message": "Proposal added successfully"})

    @viewException
    def create_tag(self, request):
        """
        This method create a new tag\n
        `METHOD`: POST\n
        """
        data = request.data
        tag = Tags.create(request, **data)

        if tag is None:
            raise APIException("An error occurred while creating the tag")

        serializer = TagSerializer(
            tag,
            data=model_to_dict(tag),
        )
        serializer.is_valid(raise_exception=True)

        return Response({"data": serializer.data})

    @viewException
    def add_comment_to_exchange_item(self, request):
        """
        This method add a comment to the exchange item with the given id\n
        `METHOD`: POST\n
        """
        data = request.data
        exchange_item = ExchangesItems.objects.filter(
            exchange_item_id=data.pop("EXCHANGE_ITEM_ID")
        ).first()

        if exchange_item is None:
            raise APIException("The item does not exist")

        user = get_user_model().objects.filter(username=data.pop("USERNAME")).first()

        comment = Comments.create(request, **data)

        if comment is None:
            raise APIException("An error occurred while creating the comment")

        isSaved = CommentXExchangesItems.add_comment(
            comment=comment, item=exchange_item, user=user
        )

        if isSaved is False:
            comment.delete()
            raise APIException("An error occurred while creating the comment")

        serializer = CommentsSerializer(
            comment,
            data=model_to_dict(comment),
        )
        serializer.is_valid(raise_exception=True)

        return Response({"data": serializer.data})

    @viewException
    def like_exchange_item(self, request):
        """
        This method add a like to the exchange item with the given id\n
        `METHOD`: POST\n
        """
        item_id = request.data.get("EXCHANGE_ITEM_ID", None)

        exchange_item = ExchangesItems.objects.filter(exchange_item_id=item_id).first()

        if exchange_item is None:
            raise APIException("The item does not exist")

        like = exchange_item.like_exchange_item(request.user)

        if not like:
            raise APIException("An error occurred while creating the like")

        return Response({"message": "Reaction added successfully"})

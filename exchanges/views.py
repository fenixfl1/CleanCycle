from functools import reduce
from operator import and_
from django.forms.models import model_to_dict
from django.db.models import Q

from rest_framework.exceptions import APIException
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from exchanges.models import ExchangesItems, ExhangeProposal, Reactions, Tags
from exchanges.serializers import ExchangeItemSerializer, TagSerializer
from posts.models import Images
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
        proposals = ExhangeProposal.objects.filter(
            Q(item_offered=item_id) & Q(state=True)
        ).all()

        serializer = ExchangeItemSerializer(
            proposals, many=True, context={"request": request}
        )

        return Response({"data": serializer.data})

    @viewException
    def get_tags(self, request):
        """
        This method return the tags\n
        `METHOD`: GET\n
        """
        tags = Tags.objects.filter(state=True).all()

        serializer = TagSerializer(tags, many=True)

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
        data = request.data

        item_id = data.get("ITEM_ID", None)
        proposal_item_id = data.get("PROPOSAL_ITEM_ID", None)

        exchange_item = ExchangesItems.objects.filter(exchange_item_id=item_id).first()

        if exchange_item is None:
            raise APIException("The item does not exist")

        proposal = ExhangeProposal.create(request, exchange_item, **data)

        if proposal is None:
            raise APIException("An error occurred while creating the proposal")

        return Response({"message": "Proposal added successfully"})

    @viewException
    def react_to_exchange_item(self, request):
        """
        This method add a reaction to the exchange item with the given id\n
        `METHOD`: POST\n
        """

        data = request.data

        item_id = data.get("ITEM_ID", None)
        reaction = data.get("REACTION", None)

        exchange_item = ExchangesItems.objects.filter(exchange_item_id=item_id).first()

        if exchange_item is None:
            raise APIException("The item does not exist")

        # validar si existe una reaccion del usuario al item
        reaction = Reactions.objects.filter(
            Q(exchange_item=exchange_item) & Q(created_by=request.user)
        ).first()

        if reaction is not None:
            # update the reaction state
            reaction.state = True if reaction.state == False else False
            reaction.save()

        else:
            data["exchange_item"] = exchange_item

            reaction = Reactions.create(request, **data)

            if reaction is None:
                raise APIException("An error occurred while creating the reaction")

        return Response({"message": "Reaction added successfully"})

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

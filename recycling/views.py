from functools import reduce
from operator import and_

from django.contrib.auth import authenticate
from django.forms.models import model_to_dict
from django.db.models import Q

from rest_framework.exceptions import APIException
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated

from recycling.serializers import CitySerializer, RecyclingPointsSerializer
from users.serializers import LoginUserSerializer

from utils.hlepers import viewException
from utils.serializers import PaginationSerializer

from recycling.models import Cities, RecyclesTypes, RecyclingPoints, Routes


class PublicViewSet(ViewSet):
    """
    Public viewset for public endpoints like get cities list, get recycle types list, etc
    """

    permission_classes = [AllowAny]
    authentication_classes = [TokenAuthentication]
    pagination_class = PaginationSerializer

    @viewException
    def get_cities_info_list(self, request):
        data = request.data.get("CITY", "")

        if data is None:
            raise APIException("City is required")

        cities = Cities.objects.filter(
            Q(name__icontains=data) | Q(city_id__contains=data)
        ).all()

        serializer = CitySerializer(cities, many=True)

        return Response({"data": serializer.data})

    @viewException
    def get_recycling_points(self, request):
        condition = request.data.get("condition", None)

        filter = Q(state=True)

        if condition is not None:
            filter = reduce(
                and_, [Q(**{key: value}) for key, value in condition.items()]
            )

        points = RecyclingPoints.objects.filter(filter).all()

        serializer = RecyclingPointsSerializer(points, many=True)

        return Response({"data": serializer.data})


class PostsViewSet(ViewSet):
    """
    Posts viewset for CRUD operations
    """

    permission_classes = [IsAuthenticated, AllowAny]
    authentication_classes = [TokenAuthentication]
    pagination_class = PaginationSerializer

    @viewException
    def get_articles_by_id(self, _request, post_id):
        pass

    @viewException
    def get_articles_list(self, request):
        pass

    @viewException
    def create_article(self, request):
        pass

    @viewException
    def update_article(self, request):
        pass

    @viewException
    def comment_article(self, request):
        pass

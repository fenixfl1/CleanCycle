from django.db.models import Q
from rest_framework import serializers
from utils.hlepers import excep
from utils.serializers import BaseModelSerializer

from recycling.models import (
    Cities,
    RecyclePointType,
    RecyclesTypes,
    RecyclingPoints,
    Routes,
)


class CitySerializer(BaseModelSerializer):
    cant_recycling_points = serializers.SerializerMethodField()
    recycling_points = serializers.SerializerMethodField()

    def get_recycling_points(self, city: Cities) -> list:
        points = RecyclingPoints.objects.filter(city=city)
        return RecyclingPointsSerializer(points, many=True).data

    def get_cant_recycling_points(self, city: Cities) -> int:
        return RecyclingPoints.objects.filter(city=city).count()

    class Meta:
        model = Cities
        fields = (
            "city_id",
            "name",
            "lnt",
            "lat",
            "recycling_points",
            "cant_recycling_points",
        )


class RecyclesTypesSerializer(BaseModelSerializer):
    class Meta:
        model = RecyclesTypes
        fields = ("recycle_type_id", "name", "description")


class RecyclingPointsSerializer(BaseModelSerializer):
    city = serializers.SerializerMethodField()
    recycling_types = serializers.SerializerMethodField()
    # schedules = serializers.SerializerMethodField()

    def get_recycling_types(self, point: RecyclingPoints) -> list:
        types = RecyclePointType.objects.filter(recycle_point=point)
        return [name for name in types.values_list("recycle_type__name", flat=True)]

    def get_city(self, instance):
        return Cities.objects.get(city_id=instance.city.city_id).name

    class Meta:
        model = RecyclingPoints
        fields = (
            "recycle_point_id",
            "location_name",
            "location_address",
            "latitude",
            "longitude",
            "description",
            "phone",
            "email",
            "state",
            "cover",
            "city",
            "recycling_types",
        )


class RoutesSerializer(BaseModelSerializer):
    class Meta:
        model = Routes
        fields = ("route_id", "route_name", "latitude", "longitude", "reference_point")


class ScheduleSerializer(BaseModelSerializer):
    class Meta:
        model = Routes
        fields = ("schedule_id", "route_id", "truck_id", "date", "time")


class ReviewsSerializer(BaseModelSerializer):
    class Meta:
        model = Routes
        fields = ("review_id", "recycle_point_id", "rating", "comment")

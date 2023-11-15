from rest_framework import serializers
from utils.hlepers import excep
from utils.serializers import BaseModelSerializer

from recycling.models import Cities, RecyclesTypes, RecyclingPoints, Routes


class CitySerializer(BaseModelSerializer):
    cant_recycling_points = serializers.SerializerMethodField()

    def get_cant_recycling_points(self, city: Cities) -> int:
        return RecyclingPoints.objects.filter(city=city).count()

    class Meta:
        model = Cities
        fields = ("city_id", "name", "lnt", "lat", "cant_recycling_points")


class RecyclesTypesSerializer(BaseModelSerializer):
    class Meta:
        model = RecyclesTypes
        fields = ("recycle_type_id", "name", "description")


class RecyclingPointsSerializer(BaseModelSerializer):
    city = CitySerializer(read_only=True)

    class Meta:
        model = RecyclingPoints
        fields = (
            "recycle_point_id",
            "location_name",
            "location_address",
            "latitude",
            "longitude",
            "description",
            "state",
            "city",
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

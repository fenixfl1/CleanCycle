from itertools import groupby
from operator import attrgetter

from django.urls import reverse
from django.utils.html import format_html
from django.contrib import admin
from django.contrib.admin.sites import AdminSite

from recycling.forms import RecyclingPointsForm
from recycling.models import (
    RecyclePointGallery,
    RecyclePointType,
    RecyclesTypes,
    RecyclingPoints,
    Routes,
    Trucks,
    Schedule,
    Reviews,
    Cities,
)
from utils.common import BaseModelAdmin
from posts.models import Images


class RecyclesTypesAdmin(BaseModelAdmin):
    list_display = ("recycle_type_id", "name", "description")

    def recycle_type_id(self, obj: RecyclesTypes):
        return obj.recycle_type_id

    def recycle_type_name(self, obj: RecyclesTypes):
        return obj.recycle_type_name


class RecycleTypeInline(admin.TabularInline):
    model = RecyclingPoints.recycle_types.through

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "recycle_type":
            kwargs["queryset"] = RecyclesTypes.objects.filter(state=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class RecyclingPointsAdmin(BaseModelAdmin):
    form = RecyclingPointsForm
    inlines = [RecycleTypeInline]
    list_display = (
        "normalize_cover",
        "location_name",
        "location_address",
        "phone",
        "email",
        "latitude",
        "longitude",
        "city",
    )
    search_fields = ["location_name", "location_address", "city__city_name"]
    fieldsets = (
        (
            "Location Information",
            {
                "fields": (
                    "created_by",
                    "location_name",
                    "location_address",
                    "phone",
                    "email",
                    "latitude",
                    "longitude",
                    "city",
                    "cover",
                    "state",
                )
            },
        ),
        ("Additional Information", {"fields": ("description",)}),
    )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "city":
            kwargs["queryset"] = Cities.objects.filter(state=True)
            kwargs["label"] = "City"
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class RoutesAdmin(BaseModelAdmin):
    list_display = (
        "route_id",
        "route_name",
        "latitude",
        "longitude",
        "reference_point",
        "created_by",
    )


class TrucksAdmin(BaseModelAdmin):
    list_display = ("truck_id", "truck_name", "created_by")


class ScheduleAdmin(BaseModelAdmin):
    list_display = (
        "schedule_id",
        "schedule_date",
        "route",
        "truck",
        "title",
        "description",
        "created_by",
    )


class ReviewsAdmin(BaseModelAdmin):
    list_display = (
        "review_id",
        "recycle_point",
        "rating",
        "comment",
        "created_by",
    )


class CitiesAdmin(BaseModelAdmin):
    list_display = ("city_id", "name", "lnt", "lat", "created_by")


class RecyclePointTypeAdmin(BaseModelAdmin):
    list_display = ("recycle_point", "recycle_type", "created_by")
    list_filter = ("recycle_point", "recycle_type")


class RecyclePointGalleryAdmin(BaseModelAdmin):
    list_display = ("normalize_image", "normalie_recycling_point", "created_by")


class ImageAdmin(BaseModelAdmin):
    list_display = ("normalize_image", "name", "created_by")


admin.site.site_header = "Puntos de Reciclaje"
admin.site.site_title = "Puntos de Reciclaje"
admin.site.index_title = "Puntos de Reciclaje"

admin.site.register(RecyclesTypes, RecyclesTypesAdmin)
admin.site.register(RecyclingPoints, RecyclingPointsAdmin)
admin.site.register(Routes, RoutesAdmin)
admin.site.register(Trucks, TrucksAdmin)
admin.site.register(Schedule, ScheduleAdmin)
admin.site.register(Reviews, ReviewsAdmin)
admin.site.register(Cities, CitiesAdmin)
admin.site.register(RecyclePointType, RecyclePointTypeAdmin)
admin.site.register(RecyclePointGallery, RecyclePointGalleryAdmin)
admin.site.register(Images, ImageAdmin)

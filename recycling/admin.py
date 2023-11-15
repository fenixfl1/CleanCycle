from django.contrib import admin
from django.contrib.admin.sites import AdminSite

from recycling.models import (
    RecyclesTypes,
    RecyclingPoints,
    Routes,
    Trucks,
    Schedule,
    Reviews,
    Cities,
)


class RecyclesTypesAdmin(admin.ModelAdmin):
    list_display = ("recycle_type_id", "recycle_type_name")

    def recycle_type_id(self, obj: RecyclesTypes):
        return obj.recycle_type_id

    def recycle_type_name(self, obj: RecyclesTypes):
        return obj.recycle_type_name


class RecycleTypeInline(
    admin.TabularInline
):  # Puedes usar StackedInline si prefieres un diseño diferente
    model = RecyclingPoints.recycle_types.through


class RecyclingPointsAdmin(admin.ModelAdmin):
    inlines = [RecycleTypeInline]
    list_display = (
        "location_name",
        "location_address",
        "latitude",
        "longitude",
        "city",
        "state",
    )
    search_fields = ["location_name", "location_address", "city__city_name"]
    list_editable = ("state",)
    raw_id_fields = ("city",)
    fieldsets = (
        (
            "Location Information",
            {
                "fields": (
                    "created_by",
                    "location_name",
                    "location_address",
                    "latitude",
                    "longitude",
                    "city",
                    "state",
                )
            },
        ),
        ("Additional Information", {"fields": ("description",)}),
    )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        print("*" * 75)
        print(f"{db_field.name}")
        print("*" * 75)
        if db_field.name == "city":
            kwargs["queryset"] = Cities.objects.all()
            kwargs["label"] = "City"
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class RoutesAdmin(admin.ModelAdmin):
    list_display = (
        "route_id",
        "route_name",
        "latitude",
        "longitude",
        "reference_point",
        "state",
        "created_by",
    )


class TrucksAdmin(admin.ModelAdmin):
    list_display = ("truck_id", "truck_name", "state", "created_by")


class ScheduleAdmin(admin.ModelAdmin):
    list_display = (
        "schedule_id",
        "schedule_date",
        "route",
        "truck",
        "title",
        "description",
        "state",
        "created_by",
    )


class ReviewsAdmin(admin.ModelAdmin):
    list_display = (
        "review_id",
        "recycle_point",
        "rating",
        "comment",
        "state",
        "created_by",
    )


class CitiesAdmin(admin.ModelAdmin):
    list_display = ("city_id", "name", "lnt", "lat", "state", "created_by")
    list_editable = ("state",)


admin.site.register(RecyclesTypes, RecyclesTypesAdmin)
admin.site.register(RecyclingPoints, RecyclingPointsAdmin)
admin.site.register(Routes, RoutesAdmin)
admin.site.register(Trucks, TrucksAdmin)
admin.site.register(Schedule, ScheduleAdmin)
admin.site.register(Reviews, ReviewsAdmin)
admin.site.register(Cities, CitiesAdmin)

from django.db import models
from django.utils.html import format_html

from utils.common import BaseModel


class RecyclesTypes(BaseModel):
    recycle_type_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)

    def __repr__(self) -> str:
        return f"{self.name}"

    def __str__(self) -> str:
        return f"{self.name}"

    class Meta:
        db_table = "recycle_types"


class Cities(BaseModel):
    """
    This model represents the cities where the recycling points are located
    `TABLE NAME:` CITIES
    """

    city_id = models.CharField(primary_key=True, max_length=2)
    name = models.CharField(max_length=100, null=False, blank=False)
    lnt = models.CharField(max_length=100, null=True, blank=True)
    lat = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        db_table = "cities"
        ordering = ["name"]
        verbose_name = "City"

    def __str__(self) -> str:
        return f"{self.name}"


class RecyclingPoints(BaseModel):
    recycle_point_id = models.AutoField(primary_key=True)
    location_name = models.CharField(max_length=100)
    location_address = models.CharField(max_length=100)
    latitude = models.CharField(max_length=100)
    longitude = models.CharField(max_length=100)
    description = models.CharField(max_length=250)
    recycle_types = models.ManyToManyField(RecyclesTypes, through="RecyclePointType")
    cover = models.TextField(null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    city = models.ForeignKey(
        Cities,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        db_column="city_id",
        to_field="city_id",
    )

    def __repr__(self) -> str:
        return f"{self.location_name}"

    def __str__(self) -> str:
        return f"{self.location_name}"

    def normalize_cover(self):
        if self.cover:
            return format_html(
                '<img src="{}" width="100" height="100" />'.format(self.cover)
            )
        return ""

    normalize_cover.short_description = "Cover"

    class Meta:
        db_table = "recycling_points"


class RecyclePointType(BaseModel):
    recycle_point = models.ForeignKey(RecyclingPoints, on_delete=models.CASCADE)
    recycle_type = models.ForeignKey(RecyclesTypes, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.recycle_point.location_name} - {self.recycle_type.name}"

    class Meta:
        db_table = "recycle_point_type"


class Routes(BaseModel):
    route_id = models.AutoField(primary_key=True)
    route_name = models.CharField(max_length=100)
    latitude = models.CharField(max_length=100)
    longitude = models.CharField(max_length=100)
    reference_point = models.CharField(max_length=100)

    def __repr__(self) -> str:
        return f"{self.route_name}"

    class Meta:
        db_table = "routes"


class Trucks(BaseModel):
    truck_id = models.AutoField(primary_key=True)
    truck_name = models.CharField(max_length=100)

    def __repr__(self) -> str:
        return f"{self.truck_name}"

    class Meta:
        db_table = "trucks"


class Schedule(BaseModel):
    schedule_id = models.AutoField(primary_key=True)
    schedule_date = models.DateField()
    route = models.ForeignKey(Routes, on_delete=models.CASCADE)
    truck = models.ForeignKey(Trucks, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=250)

    def __repr__(self) -> str:
        return f"{self.schedule_date}"

    class Meta:
        db_table = "schedule"


class Reviews(BaseModel):
    """
    This model represent the reviews of the recycling points
    `TABLE NAME:` REVIEWS
    """

    review_id = models.AutoField(primary_key=True)
    recycle_point = models.ForeignKey(RecyclingPoints, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.CharField(max_length=250)
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="reviews",
        to_field="username",
    )

    def __repr__(self) -> str:
        return f"{self.rating}"

    class Meta:
        db_table = "reviews"

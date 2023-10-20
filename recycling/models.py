from django.db import models

from utils.common import BaseModel


class RecyclesTypes(BaseModel):
    recycle_type_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)

    def __repr__(self) -> str:
        return f"{self.name}"

    class Meta:
        db_table = "RECYCLE_TYPES"


class RecyclingPoints(BaseModel):
    recycle_point_id = models.AutoField(primary_key=True)
    location_name = models.CharField(max_length=100)
    location_address = models.CharField(max_length=100)
    latitude = models.CharField(max_length=100)
    longitude = models.CharField(max_length=100)
    description = models.CharField(max_length=250)
    recycle_types = models.ManyToManyField(RecyclesTypes, through="RecyclePointType")

    def __repr__(self) -> str:
        return f"{self.location_name}"

    class Meta:
        db_table = "RECYCLING_POINTS"


class RecyclePointType(BaseModel):
    recycle_point = models.ForeignKey(RecyclingPoints, on_delete=models.CASCADE)
    recycle_type = models.ForeignKey(RecyclesTypes, on_delete=models.CASCADE)


class Routes(BaseModel):
    route_id = models.AutoField(primary_key=True)
    route_name = models.CharField(max_length=100)
    latitude = models.CharField(max_length=100)
    longitude = models.CharField(max_length=100)
    reference_point = models.CharField(max_length=100)

    def __repr__(self) -> str:
        return f"{self.route_name}"

    class Meta:
        db_table = "ROUTES"


class Trucks(BaseModel):
    truck_id = models.AutoField(primary_key=True)
    truck_name = models.CharField(max_length=100)

    def __repr__(self) -> str:
        return f"{self.truck_name}"

    class Meta:
        db_table = "TRUCKS"


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
        db_table = "SCHEDULES"


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
        db_table = "REVIEWS"

# first django
from django.db import models

# third my applications
from core import (
    models as core_models,
)  # core_models are preventing repetition. Refer to #4.0 Lecture

# from users import models as user_models


class AbstractItem(core_models.TimeStampedModel):

    """ Abstract Item """

    name = models.CharField(max_length=80)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Amenity(AbstractItem):

    """ Amenity Model Definition """

    # verbose name stands for name that appears in admin webpage
    class Meta:
        verbose_name_plural = "Amenities"

    pass


class PhotoLocation(core_models.TimeStampedModel):

    """ Photo Model Definition """

    caption = models.CharField(max_length=80)
    file = models.ImageField()  # image field for storing image

    # connecting with the Exercise. But since Exercise is defined below, it has to be done as string.
    location = models.ForeignKey("Location", on_delete=models.CASCADE)

    def __str__(self):
        return self.caption


class Location(core_models.TimeStampedModel):

    """ Location Model Definition """

    center_name = models.CharField(max_length=15)
    amenities = models.ManyToManyField("Amenity", related_name="locations", blank=True)
    naver_map_url = models.CharField(max_length=50)

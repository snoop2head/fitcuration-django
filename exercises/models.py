# first django
from django.db import models

# randomly assigning category pictures
import random

# takes the name of url and returns the actual url
from django.urls import reverse

# second third party apps
from django_countries.fields import CountryField

# third my applications
from core import models as core_models
from parsers.youtube_parser import get_yt_video_id


class AbstractItem(core_models.TimeStampedModel):

    """ Abstract Item """

    name = models.CharField(max_length=80)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Photo(core_models.TimeStampedModel):

    """ Photo Model Definition """

    caption = models.CharField(max_length=80, blank=True)
    # URLField related: https://docs.djangoproject.com/en/3.0/ref/models/fields/#urlfield
    image_url = models.URLField()  # representative image of exercise
    # image field for storing image
    file = models.ImageField(
        upload_to="exercise_photos", blank=True
    )  # saving pictures to exercise_photos
    # connecting with the Exercise. But since Exercise is defined below, it has to be done as string.
    exercise = models.ForeignKey(
        "Exercise", related_name="photos", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.caption

    # image file being saved to project folder's ./uploads/exercise_photos
    # file = models.ImageField(upload_to="exercise_photos", blank=True)


class Video(core_models.TimeStampedModel):

    """ Video Model Definition """

    video_caption = models.CharField(max_length=80, blank=True)
    # URLField relatd: https://docs.djangoproject.com/en/3.0/ref/models/fields/#urlfield
    video_url = models.URLField()  # representative video of exercise
    # connecting with the Exercise. But since Exercise is defined below, it has to be done as string.
    exercise = models.ForeignKey(
        "Exercise", related_name="videos", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.video_caption


# All of classes above are inherited here.
class Exercise(core_models.TimeStampedModel):

    """ Exercise Model Definition """

    # unique
    name = models.CharField(max_length=20)  # name of exercise
    summary = models.CharField(max_length=140, blank=True)
    description = models.TextField()  # breif description of exercise
    # list_carousels = models.ManyToManyField(
    #     "lists_carousels.ListCarousel", related_name="exercises", blank=True
    # )
    country = CountryField(blank=True)  # country of where exercise started
    category = models.ForeignKey(
        "categories.Category",
        related_name="exercises",
        on_delete=models.SET_NULL,
        null=True,
    )

    # returning name of the class when called from photo (or other fields)
    def __str__(self):
        return self.name

    # connecting with other tables
    # location = ""  # location of the center
    # naver_map_url = ""  # fetching naver map v5 url

    # method of returning absolute url for the model
    def get_absolute_url(self):
        # <name of namespace in config urls.py> : <name of url patterns in rooms urls.py>
        # keyworded arguments = {<url patterns path in rooms urls.py>: self.<url patterns path in rooms urls.py>}
        return reverse("exercises:detail", kwargs={"pk": self.pk})

    def exercise_photo_url(self):
        # queryset
        # print(self.photos.all()[:1])
        # pythonic way of assembling values into list
        (photo,) = self.photos.all()[:1]
        return photo.image_url

    """
    def exercise_photo_file(self):
        # pythonic way of assembling values into list
        (photo,) = self.photos.all()[:1]
        # print(photo.file.url)
        return photo.file.url
    """

    def exercise_video_url(self):
        # print(self.videos.all())
        (video,) = self.videos.all()[:1]
        youtube_id = get_yt_video_id(video.video_url)
        embeddable_yt_url = "https://www.youtube.com/embed/" + youtube_id
        return embeddable_yt_url

    """
    def category_pic(self):
        # print(Photo.image_url)
        # print(self.category.photos.all())
        (category,) = self.category.photos.all()[:1]
        # print(category)
        return category.image_url
    """

    def same_category_exercise_pic(self):
        category_exercises_qs = Exercise.objects.filter(category=self.category)
        # print(category_exercises_qs)
        category_exercises_qs_ids = category_exercises_qs.values_list("id", flat=True)
        category_exercises_list = list(category_exercises_qs_ids)
        category_exercises_list.remove(self.pk)
        random_primary_key = random.choice(category_exercises_list)
        # print(random_primary_key)
        # rndm_category_photo = Exercise.objects.filter(id=random_primary_key).values()
        # rndm_category_photo = random_exercise_query.photo.image_url
        # rndm_category_photo = Exercise.objects.select_relatedget(photos__id=random_primary_key)
        exercise_pic = Photo.objects.filter(exercise_id=random_primary_key)
        (image,) = exercise_pic.values("image_url").all()[:1]
        # print(image["image_url"])
        return image["image_url"]

    pass

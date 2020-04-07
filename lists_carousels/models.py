from django.db import models
from core import models as core_models

# randomly assigning category pictures
import random


class AbstractItem(core_models.TimeStampedModel):

    """ Abstract Item """

    name = models.CharField(max_length=80)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Photo(core_models.TimeStampedModel):

    """ Photo Model Definition """

    # Pointing to photo tables from ListCarousel
    # But since ListCarousel is defined below, it has to be done as string.
    category = models.ForeignKey(
        "ListCarousel", related_name="photos", on_delete=models.CASCADE
    )

    # URLField related: https://docs.djangoproject.com/en/3.0/ref/models/fields/#urlfield
    image_url = models.URLField()  # representative image of exercise
    image_caption = models.CharField(max_length=80, blank=True)

    # image file being saved to project folder's ./uploads/exercise_photos
    # file = models.ImageField(upload_to="exercise_photos", blank=True)


class ListCarousel(core_models.TimeStampedModel):
    """ ListCarousel Model Definition """

    name = models.CharField(max_length=80)
    description = models.TextField(blank=True)  # breif description of category
    exercises = models.ManyToManyField(
        "exercises.Exercise", related_name="listscarousels", blank=True
    )  # Pointing to ListCarousel tables from exercises database

    # returning class as name
    def __str__(self):
        return self.name

    # count how many exercises in ListCarousel
    def count_exercises(self):
        return self.exercises.count()

    count_exercises.short_description = "Number of exercises"
    """
    def random_category_photos(self):
        random_category_photo_queries = (
            lambda x: random.choice(self.photos.all(), k=3),
        )
        random_category_photo_list = []
        for query in random_category_photo_queries:
            random_category_photo_list.append(query.image_url)

        print(random_category_photo_list)
        return random_category_photo_list
    

    def random_category_photo(self):
        (random_photo_query,) = lambda x: random.choice(self.photos.all())
        print(random_photo_query)
        rndm_category_photo = random_photo_query[:1].image_url
        print(rndm_category_photo)
        return rndm_category_photo

    def category_photo(self):
        (photo,) = self.photos.all()[:1]
        return photo.image_url
    

    # user field is temporalily suspended from ListCarousel
    # user = models.OneToOneField(
    #     "users.User", related_name="listsCarousels", on_delete=models.CASCADE
    # )
    """

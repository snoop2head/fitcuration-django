from django.db import models
from core import models as core_models
from exercises import models as exercise_models


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
        "Category", related_name="photos", on_delete=models.CASCADE
    )

    # URLField related: https://docs.djangoproject.com/en/3.0/ref/models/fields/#urlfield
    image_url = models.URLField()  # representative image of exercise
    image_caption = models.CharField(max_length=80, blank=True)

    # image file being saved to project folder's ./uploads/exercise_photos
    # file = models.ImageField(upload_to="exercise_photos", blank=True)


class Category(core_models.TimeStampedModel):
    """ Category Model Definition """

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    name = models.CharField(max_length=80)
    short_name = models.TextField(
        max_length=10, blank=True
    )  # breif description of category

    # def random_category_photo(self):
    #     (random_photo_query,) = lambda x: random.choice(self.photos.all())
    #     print(random_photo_query)
    #     rndm_category_photo = random_photo_query[:1].image_url
    #     print(rndm_category_photo)
    #     return rndm_category_photo

    # returning class as name
    def __str__(self):
        return self.name

    def get_exercise_numbers(self):
        return self.exercises.count()

    def category_photo_url(self):
        # queryset
        # print(self.photos.all()[:1])
        # pythonic way of assembling values into list
        (photo,) = self.photos.all()[:1]
        return photo.image_url

    def exercises_in_category(self):
        exercises_qs = exercise_models.Exercise.objects.filter(category=self.pk)
        exercise_bundles = []
        for queryset in exercises_qs:
            # print(vars(queryset))
            exercise_pic_qs = exercise_models.Photo.objects.filter(
                exercise_id=queryset.id
            )
            (image,) = exercise_pic_qs.values("image_url").all()[:1]

            bundle = {
                "pk": queryset.id,
                "name": queryset.name,
                "description": queryset.description,
                "summary": queryset.summary,
                "image_url": image["image_url"],
            }
            exercise_bundles.append(bundle)
        return exercise_bundles

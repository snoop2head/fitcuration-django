from django.contrib import admin
from django.utils.html import mark_safe  # marking safe for inputted scripts to Django
from . import models  # from the same folder, import models
from exercises import models as exercise_models

# https://docs.djangoproject.com/en/3.0/ref/contrib/admin/#django.contrib.admin.ModelAdmin.inlines
class PhotoInline(admin.TabularInline):

    model = models.Photo


class ExerciseInline(admin.TabularInline):

    model = exercise_models.Exercise
    # https://docs.djangoproject.com/en/3.0/ref/contrib/admin/#django.contrib.admin.InlineModelAdmin.raw_id_fields
    extra = 0
    readonly_fields = ("name", "summary", "description", "category", "country")


# http://127.0.0.1:7000/admin/lists_carousels/listcarousel/
@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):

    """Category Admin Definition"""

    # displaying categories tables on admin panel
    # list_display = ("name", "short_name", "count_exercises")
    list_display = ("name", "short_name", "get_exercise_numbers")

    # filtering categories with exercise name
    list_filter = ("exercises__name",)

    # searching categories with exercise name
    search_fields = ("exercises__name", "name")

    # # like tistory widget, adding exercises to categories side by side
    # autocomplete_fields = ("exercises",)

    # making photo inline for category
    inlines = (PhotoInline, ExerciseInline)

    pass


@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):
    """ Photo Admin Definition """

    # check classes from models.py
    # print(dir("category"))

    list_display = (
        "category",
        "get_image_from_url",
    )

    # get thumbnail from inputted url
    def get_image_from_url(self, obj):
        # print(obj.image_url)
        return mark_safe(f'<img width="300px" src="{obj.image_url}""')

    get_image_from_url.short_description = "Thumbnail"

    # NEED TO CHANGE THIS PART TO BE Filterable WITH EXERCISE__NAME
    # list_filter = ("exercises__name",)

    # NEED TO CHANGE THIS PART TO BE SEARCHABLE WITH EXERCISE__NAME
    search_fields = ("category__name",)

    pass

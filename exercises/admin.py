from django.contrib import admin
from django.utils.html import mark_safe  # marking safe for inputted scripts to Django
from . import models  # from the same folder, import models
from parsers.youtube_parser import get_yt_video_id

# https://docs.djangoproject.com/en/3.0/ref/contrib/admin/#django.contrib.admin.ModelAdmin.inlines
class PhotoInline(admin.TabularInline):

    model = models.Photo


# https://docs.djangoproject.com/en/3.0/ref/contrib/admin/#django.contrib.admin.ModelAdmin.inlines
class VideoInline(admin.TabularInline):

    model = models.Video


# http://127.0.0.1:7000/admin/exercises/exercise/
@admin.register(models.Exercise)
class ExerciseAdmin(admin.ModelAdmin):

    """ Exercise Admin Definition """

    inlines = (
        PhotoInline,
        VideoInline,
    )

    list_display = ("name", "summary", "description", "category")
    list_filter = ("name",)
    # https://docs.djangoproject.com/en/3.0/ref/contrib/admin/#django.contrib.admin.ModelAdmin.search_fields
    search_fields = ("name", "summary", "description", "category")

    # raw_id_fields for selecting foreignkey/ManytoMany objects
    # https://docs.djangoproject.com/en/3.0/ref/contrib/admin/#django.contrib.admin.ModelAdmin.raw_id_fields
    raw_id_fields = ("category",)


# http://127.0.0.1:7000/admin/exercises/photo/
@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):
    """ Photo Admin Definition """

    # check exercise from models.py
    # print(dir("exercise"))

    # show tables on admin page
    list_display = ("exercise", "get_image_from_url", "caption")

    # selectable panel on the right side of admin page, with exercise name
    list_filter = ("exercise__name",)

    # search by exercise names on admin page
    search_fields = ("exercise__name", "caption")

    # Instead of dropdown, make pop-up search panel for exercise
    raw_id_fields = ("exercise",)

    # get thumbnail from inputted url
    def get_image_from_url(self, obj):
        # print(obj.image_url)
        return mark_safe(f'<img width="300px" src="{obj.image_url}""')

    get_image_from_url.short_description = "Thumbnail"


# http://127.0.0.1:7000/admin/exercises/video/
@admin.register(models.Video)
class VideoAdmin(admin.ModelAdmin):
    """ Video Admin Definition """

    # show tables on admin page
    list_display = ("exercise", "get_video_url", "video_caption")

    # selectable panel on the right side of admin page, with exercise name
    list_filter = ("exercise__name",)

    # Instead of dropdown, make pop-up search panel for exercise
    raw_id_fields = ("exercise",)

    # get video from inputted url
    def get_video_url(self, obj):
        youtube_input_url = obj.video_url
        youtube_id = get_yt_video_id(youtube_input_url)
        embeddable_yt_url = "https://www.youtube.com/embed/" + youtube_id
        return mark_safe(
            f'<iframe id="ytplayer" type="text/html" width="640" height="360" src="{embeddable_yt_url}" frameborder="0"></iframe>'
        )

    get_video_url.short_description = "Video Embedded"

    # search by exercise names on admin page
    search_fields = ("exercise__name", "video_caption")

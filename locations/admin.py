from django.contrib import admin
from . import models  # from the same folder, import models

# refer ./models.py
@admin.register(models.Amenity)
class ItemAdmin(admin.ModelAdmin):

    """ Item Admin Definition """

    pass


@admin.register(models.PhotoLocation)
class PhotoLocationAdmin(admin.ModelAdmin):

    """ PhotoLocation Admin Definition """

    pass


@admin.register(models.Location)
class LocationAdmin(admin.ModelAdmin):

    """ Location Admin Definition """

    # making table-like display on admin page
    list_display = (
        "center_name",
        "naver_map_url",
    )

    list_filter = ()

    pass

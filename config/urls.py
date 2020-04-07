import os

from django.contrib import admin
from django.urls import path, include

# django will know which settings.py that you've set up in project folder
from django.conf import settings
from django.conf.urls.static import static


# sample router to trigger sentry
def trigger_error(request):
    division_by_zero = 1 / 0


# patterns of requested urls
urlpatterns = [
    # dividing router to core app's urls.py
    path("", include("core.urls", namespace="core")),
    # dividing router to each apps' urls.py
    path("exercises/", include("exercises.urls", namespace="exercises")),
    path("categories/", include("categories.urls", namespace="categories")),
    # dividing router to admin
    path(os.environ.get("ADMIN_PATH"), admin.site.urls),
    path("users/", include("users.urls", namespace="users")),
    # sample router to trigger sentry
    path("sentry-debug/", trigger_error),
]

# When I am developping, I set DEBUG in settings.py as True
# When I am on production level (when server is live), I set DEBUG in settings.py False
# If I am developping, serve the files from the project folder
# If you are on production level, never put images on project server folder
if settings.DEBUG:
    # static connecting url with the folder
    # folder is media root
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

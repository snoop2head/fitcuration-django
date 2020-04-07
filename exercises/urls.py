from django.urls import path
from . import views

# making separate urls.py for rooms
app_name = "exercises"

# receiving "localhost/exercises/110230" to use it as primary key for database
urlpatterns = [
    path("<int:pk>", views.ExerciseDetail.as_view(), name="detail"),
    path("search/", views.SearchView.as_view(), name="search"),
]

from django.urls import path
from . import views

# making separate urls.py for rooms
app_name = "categories"

# receiving "localhost/rooms/110230" to use it as primary key for database
urlpatterns = [
    path("<int:pk>", views.CategoryDetail.as_view(), name="detail"),
]

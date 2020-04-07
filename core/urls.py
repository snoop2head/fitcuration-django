from django.urls import path
from exercises import views as exercise_views

app_name = "core"

urlpatterns = [path("", exercise_views.HomeView.as_view(), name="home")]

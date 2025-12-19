from django.urls import path

from . import views


app_name = "hero"

urlpatterns = [
    path("heroes/", views.heroes, name="heroes"),
]

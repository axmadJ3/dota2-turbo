from django.urls import path

from . import views


app_name = "hero"

urlpatterns = [
    path("heroes/", views.heroes, name="heroes"),
    path("heroes/facets/", views.facets, name="facets"),
]

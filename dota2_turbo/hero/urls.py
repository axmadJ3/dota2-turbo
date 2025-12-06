from django.urls import path

from . import views


app_name = 'dota2_turbo.hero'

urlpatterns = [
    path('heroes/', views.heroes, name='heroes'),
]

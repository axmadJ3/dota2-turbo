from django.urls import path

from dota2_turbo.player import views


app_name = "player"

urlpatterns = [
    path("player/<int:steamid32>/", views.player_stats, name="player"),
]

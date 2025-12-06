from django.urls import path

from . import views


app_name = 'dota2_turbo.leaderboard'

urlpatterns = [
    path('', views.leaderboard, name='leaderboard'),
]

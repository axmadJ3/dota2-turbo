from django.urls import path

from dota2_turbo.leaderboard import views
from dota2_turbo.leaderboard.api import views as api_views


app_name = 'leaderboard'

urlpatterns = [
    path('', views.leaderboard, name='leaderboard'),
    path('about/', views.about, name='about'),
    path("api/leaderboard/", api_views.LeaderboardAPIView.as_view(), name="leaderboard-api"),
]

from django.db.models import Sum
from django.db.models.functions import Coalesce

from dota2_turbo.authentication.models import SteamUser


def calculate_rating_change(win, kills, deaths, assists):
    return (20 if win else -20) + kills * 4 - deaths * 4 + assists * 1


def calculate_total_rating():
    users = SteamUser.objects.annotate(
        total_rating = Coalesce(
            Sum('matches__rating_change'), 0
        )
    ).order_by('-total_rating')
    return users

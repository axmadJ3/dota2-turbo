from django.db.models import Sum, F, Window, IntegerField
from django.db.models.functions import Coalesce, Rank

from dota2_turbo.authentication.models import SteamUser


def calculate_rating_change(win, kills, deaths, assists):
    return (20 if win else -20) + kills * 4 - deaths * 4 + assists * 1


def calculate_total_rating():
    return SteamUser.objects.annotate(
        total_rating=Coalesce(
            Sum('matches__rating_change'), 0,
            output_field=IntegerField()
        ),
        rank=Window(
            expression=Rank(),
            order_by=F('total_rating').desc()
        )
    )

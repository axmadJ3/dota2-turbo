from django.shortcuts import render
from django.db.models import Sum
from django.db.models.functions import Coalesce

from dota2_turbo.authentication.models import SteamUser


def leaderboard(request):
    users = SteamUser.objects.annotate(
        total_rating = Coalesce(
            Sum('matches__rating_change'), 0
        )
    ).order_by('-total_rating')

    context = {
        'users': users,
        'title': 'Leaderboard - Dota 2 Turbo Stats'
    }
    return render(
        request,
        'leaderboard/leaderboard.html',
        context=context
    )


def about(request):
    context = {
        'title': 'About - Dota 2 Turbo Stats'
    }
    return render(
        request,
        'leaderboard/about.html',
        context=context
    )

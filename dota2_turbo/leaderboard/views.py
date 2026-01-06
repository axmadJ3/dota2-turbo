from datetime import timedelta

from django.shortcuts import render
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.core.paginator import Paginator
from django.utils import timezone

from dota2_turbo.authentication.models import SteamUser
from dota2_turbo.player.tasks import parse_steam_friendlist


def leaderboard(request):
    users = SteamUser.objects.annotate(
        total_rating = Coalesce(
            Sum('matches__rating_change'), 0
        )
    ).order_by('-total_rating')

    friend_ids = set()
    if request.user.is_authenticated:
        user = request.user

        needs_update = (
            not user.steam_friends_updated_at or
            timezone.now() - user.steam_friends_updated_at > timedelta(days=3)
        )

        if needs_update:
            parse_steam_friendlist.delay(user.steamid)

        friend_ids = set(user.steam_friends or [])

    paginator = Paginator(users, 50)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    context = {
        'page': page,
        'friend_ids': friend_ids,
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

from datetime import timedelta

from django.shortcuts import render
from django.core.paginator import Paginator
from django.utils import timezone

from dota2_turbo.leaderboard.utils import calculate_total_rating
from dota2_turbo.player.tasks import parse_steam_friendlist


def leaderboard(request):
    users = calculate_total_rating()

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

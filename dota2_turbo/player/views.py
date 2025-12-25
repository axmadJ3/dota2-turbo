from datetime import timezone, datetime

from django.core.cache import cache
from django.core.paginator import Paginator
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect

from dota2_turbo.authentication.models import SteamUser
from dota2_turbo.leaderboard.models import Match
from dota2_turbo.player.models import PlayerHeroStats
from dota2_turbo.player.tasks import update_player_hero_stats


def player_stats(request, steamid32):
    group = request.GET.get("group", "matches")
    player = get_object_or_404(SteamUser, steamid32=steamid32)

    context = {"group": group, "player": player, "title": "Game Statistics"}

    if group == "matches":
        cache_key = f"player_matches_{player.steamid32}"
        matches = cache.get(cache_key)
        if matches is None:
            matches = (
                Match.objects.filter(player=player)
                .select_related("hero", "hero_facet")
                .order_by("-match_id")
            )
            matches = list(matches)
            cache.set(cache_key, matches, timeout=3600)
        paginator = Paginator(matches, 50)

    elif group == "heroes":
        cache_key = f"player_heroes_{player.steamid32}"
        cache.delete(cache_key)
        update_player_hero_stats.delay(player.steamid32)
        hero_stats = cache.get(cache_key)
        if hero_stats is None:
            hero_stats = list(
                PlayerHeroStats.objects.filter(player=player)
                .select_related("hero")
            )
            hero_stats.sort(
                key=lambda x: (
                    x.games == 0,
                    -(x.last_played.timestamp() if x.last_played else 0)
                )
            )
            cache.set(cache_key, hero_stats, timeout=3600)
        paginator = Paginator(hero_stats, 50)

    else:
        return redirect(f"{request.path}?group=matches")

    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    context["page"] = page

    return render(
        request, 
        "player/statistics.html", 
        context
    )

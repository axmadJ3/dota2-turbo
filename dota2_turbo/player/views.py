from datetime import datetime, timezone

from django.core.cache import cache
from django.core.paginator import Paginator
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.db.models import Count, Q

from dota2_turbo.authentication.models import SteamUser
from dota2_turbo.leaderboard.models import Match
from dota2_turbo.player.models import PlayerHeroStats
from dota2_turbo.player.tasks import update_player_hero_stats, update_player_match_history


def player_stats(request, steamid32):
    group = request.GET.get("group", "matches")
    player = get_object_or_404(SteamUser, steamid32=steamid32)

    matches = Match.objects.filter(player=player)
    player_stats = (
        matches
        .aggregate(
            games=Count("id"),
            wins=Count("id", filter=Q(win=True)),
            losses=Count("id", filter=Q(win=False)),
        )
    )
    player_stats['winrate'] = round(
        (player_stats['wins'] / player_stats['games']) * 100, 1
    ) if player_stats['games'] > 0 else 0

    context = {
        "group": group,
        "player": player,
        "player_stats": player_stats,
        "title": "Game Statistics"
    }

    if group == "matches":
        cache_key = f"player_matches_{player.steamid32}"
        cache_timestamp_key = f"player_matches_ts_{player.steamid32}"
        
        matches = cache.get(cache_key)
        last_update = cache.get(cache_timestamp_key)
        
        if matches is None or not last_update or (datetime.now(timezone.utc).timestamp() - last_update > 1800):
            update_player_match_history.delay(player.id)
        
        if matches is None:
            matches = list(
                Match.objects.filter(player=player)
                .select_related("hero", "hero_facet")
                .order_by("-match_time")
            )
            cache.set(cache_key, matches, timeout=1800)
            cache.set(cache_timestamp_key, datetime.now(timezone.utc).timestamp(), timeout=1800)
        
        paginator = Paginator(matches, 50)

    elif group == "heroes":
        cache_key = f"player_heroes_{player.steamid32}"
        cache_timestamp_key = f"player_heroes_ts_{player.steamid32}"
        
        hero_stats = cache.get(cache_key)
        last_update = cache.get(cache_timestamp_key)
        
        if hero_stats is None or not last_update or (datetime.now(timezone.utc).timestamp() - last_update > 1800):
            update_player_hero_stats.delay(player.steamid32)
        
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
            cache.set(cache_key, hero_stats, timeout=1800)
            cache.set(cache_timestamp_key, datetime.now(timezone.utc).timestamp(), timeout=1800)
        
        paginator = Paginator(hero_stats, 50)

    else:
        return redirect(f"{request.path}?group=matches")

    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    context["page"] = page

    return render(
        request, 
        "player/statistics.html", 
        context=context
    )

from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404

from dota2_turbo.authentication.models import SteamUser
from dota2_turbo.player.utils import (
    get_player_stats,
    get_or_update_cache,
    get_player_heroes,
    get_player_matches
)
from dota2_turbo.player.tasks import (
    update_player_hero_stats, 
    update_player_match_history
)


PAGE_SIZE = 50


def player_stats(request, steamid32):
    group = request.GET.get("group", "matches")

    player = get_object_or_404(SteamUser, steamid32=steamid32)
    player_stats = get_player_stats(player)
    context = {
        "group": group,
        "player": player,
        "player_stats": player_stats,
        "title": "Game Statistics"
    }

    if group == "matches":
        items = get_or_update_cache(
            cache_key=f"player_matches_{player.steamid32}",
            ts_key=f"player_matches_ts_{player.steamid32}",
            func=lambda: get_player_matches(player),
            update_task=update_player_match_history,
            update_task_args=(player.id,),
        )
    elif group == "heroes":
        items = get_or_update_cache(
            cache_key=f"player_heroes_{player.steamid32}",
            ts_key=f"player_heroes_ts_{player.steamid32}",
            func=lambda : get_player_heroes(player),
            update_task=update_player_hero_stats,
            update_task_args=(player.steamid32,),
        )
    else:
        return redirect(f"{request.path}?group=matches")

    paginator = Paginator(items, PAGE_SIZE)
    context["page"] = paginator.get_page(request.GET.get("page"))

    return render(
        request, 
        "player/statistics.html", 
        context
    )

from datetime import datetime, timezone

from django.core.cache import cache
from django.db.models import Count, Q

from dota2_turbo.leaderboard.models import Match
from dota2_turbo.player.models import PlayerHeroStats


CACHE_TTL = 300


def get_player_stats(player):
    cache_key = f"player_stats_{player.steamid32}"

    stats = cache.get(cache_key)
    if stats:
        return stats

    stats = Match.objects.filter(player=player).aggregate(
        games=Count("id"),
        wins=Count("id", filter=Q(win=True)),
        losses=Count("id", filter=Q(win=False)),
    )
    stats["winrate"] = round(
        (stats["wins"] / stats["games"]) * 100, 1
    ) if stats["games"] else 0

    cache.set(cache_key, stats, CACHE_TTL)
    return stats


def get_or_update_cache(
    *,
    cache_key: str,
    ts_key: str,
    func,
    update_task=None,
    update_task_args=(),
    timeout=CACHE_TTL,
    ):

    data = cache.get(cache_key)
    last_update = cache.get(ts_key)
    now_ts = datetime.now(timezone.utc).timestamp()

    if data is None or not last_update or (now_ts - last_update > timeout):
        if update_task:
            update_task.delay(*update_task_args)

    if data is None:
        data = func()
        cache.set(cache_key, data, timeout=timeout)
        cache.set(ts_key, now_ts, timeout=timeout)

    return data


def get_player_heroes(player):
    heroes = list(
        PlayerHeroStats.objects
        .filter(player=player)
        .select_related("hero")
    )
    heroes.sort(
        key=lambda x: (
            x.games == 0,
            -(x.last_played.timestamp() if x.last_played else 0)
        )
    )
    return heroes

def get_player_matches(player):
    matches = list(
        Match.objects.filter(player=player)
        .select_related("hero", "hero_facet")
        .order_by("-match_time")
    )
    return matches

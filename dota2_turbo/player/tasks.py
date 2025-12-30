from datetime import datetime, timezone
from requests.exceptions import ReadTimeout, ConnectionError, HTTPError

from celery import shared_task
from django.core.cache import cache

from dota2_turbo.authentication.models import SteamUser
from dota2_turbo.leaderboard.models import Match
from dota2_turbo.player.models import PlayerHeroStats
from dota2_turbo.player.services.update_player_hero_stats import update_hero_stats
from dota2_turbo.leaderboard.services.update_matches_for_player import update_matches


@shared_task(
    autoretry_for=(ReadTimeout, ConnectionError, HTTPError),
    retry_backoff=5,
    retry_jitter=True,
    retry_kwargs={"max_retries": 3},
)
def update_player_hero_stats(steamid32):
    result = update_hero_stats(steamid32)
    try:
        player = SteamUser.objects.get(steamid32=steamid32)
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
        cache_key = f"player_heroes_{steamid32}"
        cache_timestamp_key = f"player_heroes_ts_{steamid32}"
        
        cache.set(cache_key, hero_stats, timeout=1800)
        cache.set(cache_timestamp_key, datetime.now(timezone.utc).timestamp(), timeout=1800)
    except SteamUser.DoesNotExist:
        pass
    return result


@shared_task(
    autoretry_for=(ReadTimeout, ConnectionError, HTTPError),
    retry_backoff=5,
    retry_jitter=True,
    retry_kwargs={"max_retries": 3},
)
def update_player_match_history(player_id):
    result = update_matches(player_id)
    try:
        player = SteamUser.objects.get(id=player_id)
        matches = list(
            Match.objects.filter(player=player)
            .select_related("hero", "hero_facet")
            .order_by("-match_id")
        )
        
        cache_key = f"player_matches_{player.steamid32}"
        cache_timestamp_key = f"player_matches_ts_{player.steamid32}"
        
        cache.set(cache_key, matches, timeout=1800)
        cache.set(cache_timestamp_key, datetime.now(timezone.utc).timestamp(), timeout=1800)
    except SteamUser.DoesNotExist:
        pass
    return result

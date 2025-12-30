from requests.exceptions import ReadTimeout, ConnectionError, HTTPError

from celery import shared_task
from django.core.cache import cache

from dota2_turbo.player.services.update_player_hero_stats import update_hero_stats
from dota2_turbo.player.services.update_player_match_history import update_match_history

@shared_task(
    autoretry_for=(ReadTimeout, ConnectionError, HTTPError),
    retry_backoff=5,
    retry_jitter=True,
    retry_kwargs={"max_retries": 3},
)
def update_player_hero_stats(steamid32):
    result = update_hero_stats(steamid32)
    cache.delete(f"player_heroes_{steamid32}")
    return result


@shared_task(
    autoretry_for=(ReadTimeout, ConnectionError, HTTPError),
    retry_backoff=5,
    retry_jitter=True,
    retry_kwargs={"max_retries": 3},
)
def update_player_match_history(steamid32):
    result = update_match_history(steamid32)
    cache.delete(f"player_matches_{steamid32}")
    return result

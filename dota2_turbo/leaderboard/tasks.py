import logging
from requests.exceptions import ReadTimeout, ConnectionError, HTTPError

from celery import shared_task

from dota2_turbo.authentication.models import SteamUser
from dota2_turbo.leaderboard.services.sync_matches import sync_matches_for_player


logger = logging.getLogger(__name__)


@shared_task(
    autoretry_for=(ReadTimeout, ConnectionError, HTTPError),
    retry_backoff=5,
    retry_jitter=True,
    retry_kwargs={"max_retries": 3},
)
def sync_player_matches(player_id):
    logger.info(f"Start sync for player {player_id}")
    added = sync_matches_for_player(player_id)
    logger.info(f"Player {player_id}: added {added} matches")
    return added


@shared_task
def sync_all_players():
    player_ids = SteamUser.objects.values_list("id", flat=True)

    for player_id in player_ids:
        logger.info(f"Send sync task for player {player_id}")
        sync_player_matches.delay(player_id)

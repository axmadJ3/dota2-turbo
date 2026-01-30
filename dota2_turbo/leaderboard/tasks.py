import logging
from requests.exceptions import ReadTimeout, ConnectionError, HTTPError

from celery import shared_task

from dota2_turbo.authentication.models import SteamUser
from dota2_turbo.leaderboard.services.update_matches_for_player import update_matches
from dota2_turbo.leaderboard.services.remove_low_rating_users import remove_users


logger = logging.getLogger(__name__)


@shared_task(
    autoretry_for=(ReadTimeout, ConnectionError, HTTPError),
    retry_backoff=5,
    retry_jitter=True,
    retry_kwargs={"max_retries": 3},
)
def update_matches_for_player(player_id):
    logger.info(f"Starting update matches for player {player_id}")
    added = update_matches(player_id)
    logger.info(f"Player {player_id}: added {added} matches")
    return added


@shared_task
def update_all_players():
    player_ids = SteamUser.objects.values_list("id", flat=True)

    for player_id in player_ids:
        update_matches_for_player.delay(player_id)


@shared_task
def remove_low_rating_users():
    removed = remove_users()
    return removed

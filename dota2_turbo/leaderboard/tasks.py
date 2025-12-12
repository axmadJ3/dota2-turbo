from celery import shared_task

from dota2_turbo.authentication.models import SteamUser
from dota2_turbo.leaderboard.services.sync_matches import sync_matches_for_player


@shared_task(
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 3},
)
def sync_player_matches(player_id):
    sync_matches_for_player(player_id)


@shared_task
def sync_all_players():
    for player in SteamUser.objects.values_list("id", flat=True):
        sync_player_matches.delay(player)

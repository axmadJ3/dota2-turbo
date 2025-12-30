"""
Синхронизация статистики героев игрока:
- храним только статистику за последние 180 дней
- добавляем новых героев или обновляем
"""

import logging
import requests
from datetime import datetime, timezone

from dota2_turbo.authentication.models import SteamUser
from dota2_turbo.hero.models import Hero
from dota2_turbo.player.models import PlayerHeroStats

logger = logging.getLogger(__name__)

def update_hero_stats(steamid32):
    try:
        player = SteamUser.objects.get(steamid32=steamid32)
    except SteamUser.DoesNotExist:
        return 0

    url = f"https://api.opendota.com/api/players/{steamid32}/heroes?game_mode=23&significant=0&date=180"
    try:
        response = requests.get(url=url, timeout=10)
        response.raise_for_status()
        heroes = response.json()
    except Exception:
        return 0

    default_date = datetime(1970, 1, 1, tzinfo=timezone.utc)
    
    count = 0
    for item in heroes:
        last_played_ts = item.get("last_played", 0)
        last_played = datetime.fromtimestamp(last_played_ts, tz=timezone.utc) if last_played_ts > 0 else default_date

        try:
            hero_obj = Hero.objects.get(hero_id=item["hero_id"])
        except Hero.DoesNotExist:
            continue

        PlayerHeroStats.objects.update_or_create(
            player=player,
            hero=hero_obj,
            defaults={
                "last_played": last_played,
                "games": item.get("games", 0),
                "win": item.get("win", 0),
                "with_games": item.get("with_games", 0),
                "with_win": item.get("with_win", 0),
                "against_games": item.get("against_games", 0),
                "against_win": item.get("against_win", 0),
            }
        )
        count += 1
    return count
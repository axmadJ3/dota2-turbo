"""
Синхронизация матчей игрока:
- храним только матчи за последние 180 дней
- удаляем старые матчи
- добавляем новые
- обновляем facet если нет
"""

import requests
from datetime import datetime, timedelta, timezone

from dota2_turbo.authentication.models import SteamUser
from dota2_turbo.hero.models import Hero, HeroFacet
from dota2_turbo.leaderboard.models import Match
from dota2_turbo.leaderboard.utils import calculate_rating_change


def update_matches(player_id):
    try:
        player = SteamUser.objects.get(id=player_id)
    except SteamUser.DoesNotExist:
        return 0

    if not player.steamid32:
        return 0

    url = (
        f"https://api.opendota.com/api/players/{player.steamid32}/matches?game_mode=23&date=180&significant=0"
    )

    response = requests.get(url, timeout=10)
    if not response.ok:
        response.raise_for_status()

    matches = response.json()

    cutoff_date = datetime.now(timezone.utc) - timedelta(days=180)

    Match.objects.filter(player=player, match_time__lt=cutoff_date).delete()

    added_count = 0
    for m in matches:
        match_time = datetime.fromtimestamp(
            m["start_time"], tz=timezone.utc
        )

        if match_time < cutoff_date:
            continue

        win = (
            (m["player_slot"] < 128 and m["radiant_win"]) or
            (m["player_slot"] >= 128 and not m["radiant_win"])
        )

        rating_change = calculate_rating_change(
            win, m["kills"], m["deaths"], m["assists"]
        )

        try:
            hero = Hero.objects.get(hero_id=m["hero_id"])
        except Hero.DoesNotExist:
            continue

        facet_obj = None
        facet_id = m.get("hero_variant")
        if facet_id is not None:
            facet_obj = HeroFacet.objects.filter(
                hero=hero,
                facet_id=int(facet_id) - 1
            ).first()

        obj, created = Match.objects.get_or_create(
            match_id=m["match_id"],
            player=player,
            defaults={
                "hero": hero,
                "hero_facet": facet_obj,
                "kills": m["kills"],
                "deaths": m["deaths"],
                "assists": m["assists"],
                "win": win,
                "rating_change": rating_change,
                "match_time": match_time,
                "duration": m["duration"],
            }
        )

        if created:
            added_count += 1
        elif obj.hero_facet is None and facet_obj:
            obj.hero_facet = facet_obj
            obj.save(update_fields=["hero_facet"])

    return added_count

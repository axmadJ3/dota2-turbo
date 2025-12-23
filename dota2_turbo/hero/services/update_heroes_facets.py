"""
Синхронизация аспектов героев:
- статистика только за последние 180 дней
- вычисляем винрейт, пикрейт и тир
"""

from decimal import Decimal

from django.db.models import Count, Q

from dota2_turbo.hero.utils import calculate_tier
from dota2_turbo.hero.models import HeroFacet
from dota2_turbo.leaderboard.models import Match


def update_heroes_facets():
    updated = 0

    matches = Match.objects.filter(hero_facet__isnull=False)
    if not matches.exists():
        return 0

    hero_games_map = {
        row["hero"]: row["games"]
        for row in (
            matches
            .values("hero")
            .annotate(games=Count("id"))
        )
    }

    hero_facets = (
        matches
        .values("hero", "hero_facet__facet_id")
        .annotate(
            games=Count("id"),
            wins=Count("id", filter=Q(win=True)),
        )
    )

    for stats in hero_facets:
        hero_id = stats["hero"]
        facet_id = stats["hero_facet__facet_id"]

        games = stats["games"]
        wins = stats["wins"]
        hero_games = hero_games_map.get(hero_id, 0)

        if hero_games == 0:
            continue

        winrate = (
            Decimal(wins) / Decimal(games) * 100
        ).quantize(Decimal("0.01"))

        pickrate = (
            Decimal(games) / Decimal(hero_games) * 100
        ).quantize(Decimal("0.01"))

        tier = calculate_tier(winrate)

        HeroFacet.objects.update_or_create(
            hero_id=hero_id,
            facet_id=facet_id,
            defaults={
                "tier": tier,
                "winrate": winrate,
                "pickrate": pickrate,
            }
        )

        updated += 1

    return updated

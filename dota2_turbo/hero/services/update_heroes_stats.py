"""
Синхронизация героев:
- статистика только за последние 180, 60 и 30 дней
- вычисляем винрейт, пикрейт и тир
"""

from decimal import Decimal
from datetime import datetime, timedelta, timezone

from django.db.models import Count, Q

from dota2_turbo.hero.utils import calculate_tier
from dota2_turbo.hero.models import Hero, HeroTier
from dota2_turbo.leaderboard.models import Match


def update_heroes_stats():
    PERIODS = {
        "month": 30,
        "3months": 90,
        "6months": 180,
    }

    updated = 0
    now = datetime.now(timezone.utc)
    for period, days in PERIODS.items():
        start_date = now - timedelta(days=days)
        matches = Match.objects.filter(match_time__gte=start_date)

        total_matches = matches.count()
        if total_matches == 0:
            HeroTier.objects.filter(period=period).delete()
            continue

        hero_stats = (
            matches
            .values("hero")
            .annotate(
                games=Count("id"),
                wins=Count("id", filter=Q(win=True))
            )
        )

        for stats in hero_stats:
            hero_id = stats["hero"]
            try:
                hero = Hero.objects.get(id=hero_id)
            except Hero.DoesNotExist:
                continue

            games = stats["games"]
            wins = stats["wins"]
            winrate = (Decimal(wins) / Decimal(games) * 100).quantize(Decimal("0.01"))
            pickrate = (Decimal(games) / Decimal(total_matches) * 100).quantize(Decimal("0.01"))
            tier = calculate_tier(winrate)
            HeroTier.objects.update_or_create(
                hero=hero,
                period=period,
                defaults={
                    "tier": tier,
                    "winrate": winrate,
                    "pickrate": pickrate,
                }
            )
            updated += 1
    return updated

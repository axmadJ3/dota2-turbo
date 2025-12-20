from django.shortcuts import render
from django.db.models import When, Case, IntegerField

from dota2_turbo.hero.models import HeroTier
from dota2_turbo.hero import utils

def heroes(request):
    period = request.GET.get("period", "6months")
    position = request.GET.get("position", "All")
    sort = request.GET.get("sort", "winrate")
    direction = request.GET.get("dir", "desc")

    hero_tiers = HeroTier.objects.filter(period=period).select_related("hero")

    if position != "All":
        hero_tiers = hero_tiers.filter(hero__positions__contains=[position])

    if sort not in utils.SORT_MAP:
        sort = "winrate"
    sort_field = utils.SORT_MAP[sort]
    if sort_field == "tier":
        hero_tiers = hero_tiers.annotate(
            tier_order=Case(
                When(tier="S", then=1),
                When(tier="A", then=2),
                When(tier="B", then=3),
                When(tier="C", then=4),
                When(tier="D", then=5),
                output_field=IntegerField(),
            )
        )
        order = "-tier_order" if direction == "desc" else "tier_order"
        hero_tiers = hero_tiers.order_by(order)
    else:
        order = f"-{sort_field}" if direction == "desc" else sort_field
        hero_tiers = hero_tiers.order_by(order)

    context = {
        "hero_tiers": hero_tiers,
        "periods": utils.PERIODS,
        "positions": utils.POSITIONS,
        "sort_headers": utils.SORT_HEADERS,
        "current_dir": direction,
        "current_sort": sort,
        "current_period": period,
        "current_position": position,
        "title": "Heroes - Dota 2 Turbo Stats"
    }
    return render(
        request,
        "hero/heroes.html",
        context=context 
    )

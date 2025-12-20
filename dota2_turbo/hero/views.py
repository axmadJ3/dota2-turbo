from django.shortcuts import render

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
    if direction == "desc":
        sort_field = f"-{sort_field}"
    hero_tiers = hero_tiers.order_by(sort_field)

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

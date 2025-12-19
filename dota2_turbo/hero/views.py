from django.shortcuts import render

from dota2_turbo.hero.models import HeroTier
from dota2_turbo.hero import utils

def heroes(request):
    period = request.GET.get("period", "6months")
    position = request.GET.get("position", "All")

    hero_tiers = HeroTier.objects.filter(period=period).select_related("hero")
    if position != "All":
        hero_tiers = hero_tiers.filter(hero__positions__contains=[position])
    hero_tiers = hero_tiers.order_by("-winrate")

    context = {
        "hero_tiers": hero_tiers,
        "positions": utils.POSITIONS,
        "current_position": position,
        "periods": utils.PERIODS,
        "current_period": period,
        "title": "Heroes - Dota 2 Turbo Stats"
    }
    return render(
        request,
        "hero/heroes.html",
        context=context 
    )

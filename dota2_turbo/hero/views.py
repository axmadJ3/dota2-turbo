from django.shortcuts import render

from dota2_turbo.hero.models import HeroTier, HeroFacet
from dota2_turbo.hero import utils

def heroes(request):
    period = request.GET.get("period", "6months")
    position = request.GET.get("position", "All")
    sort = request.GET.get("sort", "winrate")
    direction = request.GET.get("dir", "desc")

    qs = HeroTier.objects.select_related("hero")
    hero_tiers = utils.common_filters(
        qs,
        period=period,
        position=position,
        sort=sort,
        direction=direction,
        sort_map=utils.SORT_MAP,
    )

    context = {
        "group": "Heroes",
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


def facets(request):
    position = request.GET.get("position", "All")
    sort = request.GET.get("sort", "winrate")
    direction = request.GET.get("dir", "desc")

    qs = HeroFacet.objects.exclude(tier="NR").select_related("hero")
    hero_facets = utils.common_filters(
        qs,
        position=position,
        sort=sort,
        direction=direction,
        sort_map=utils.SORT_MAP,
    )

    context = {
        "group": "Facets",
        "hero_facets": hero_facets,
        "positions": utils.POSITIONS,
        "facet_sort_headers": utils.FACET_SORT_HEADERS,
        "current_dir": direction,
        "current_sort": sort,
        "current_position": position,
        "title": "Facets - Dota 2 Turbo Stats"
    }
    return render(
        request,
        "hero/facets.html",
        context=context 
    )

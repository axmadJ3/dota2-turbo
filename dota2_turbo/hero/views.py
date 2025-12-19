from django.shortcuts import render
from .models import HeroTier


def heroes(request):
    period = request.GET.get('period', '6months')
    hero_tiers = HeroTier.objects.filter(period=period).select_related('hero').order_by('-winrate')
    context = {
        'hero_tiers': hero_tiers,
        'period': period,
        'title': 'Heroes - Dota 2 Turbo Stats'
    }
    return render(
        request,
        'hero/heroes.html',
        context=context 
    )

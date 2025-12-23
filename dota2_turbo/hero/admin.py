from django.contrib import admin

from dota2_turbo.hero.models import Hero, HeroFacet, HeroTier
from dota2_turbo.leaderboard.models import Match


@admin.register(Hero)
class HeroAdmin(admin.ModelAdmin):
    list_display = ('name', 'hero_id')


@admin.register(HeroTier)
class HeroTierAdmin(admin.ModelAdmin):
    list_display = [
        'hero__name', 
        'tier', 
        'winrate', 
        'pickrate', 
        'period'
    ]


@admin.register(HeroFacet)
class HeroFacetAdmin(admin.ModelAdmin):
    list_display = [
        'hero_name', 
        'facet_id', 
        'title', 
        'icon', 
        'color',
        'winrate',
        'pickrate',
        'tier',
        'matches_count'
    ]

    @admin.display(description='Hero')
    def hero_name(self, obj):
        return obj.hero.name

    @admin.display(description='Matches')
    def matches_count(self, obj):
        return Match.objects.filter(hero_facet=obj).count()

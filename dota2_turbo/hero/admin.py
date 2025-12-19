from django.contrib import admin

from dota2_turbo.hero.models import Hero, HeroFacet, HeroTier


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
        'hero__name', 
        'facet_id', 
        'title', 
        'icon', 
        'color'
    ]

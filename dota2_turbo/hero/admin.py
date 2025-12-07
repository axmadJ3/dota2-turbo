from django.contrib import admin

from dota2_turbo.hero.models import Hero


@admin.register(Hero)
class HeroAdmin(admin.ModelAdmin):
    list_display = ('name', 'hero_id')

from django.contrib import admin

from dota2_turbo.player.models import PlayerHeroStats


@admin.register(PlayerHeroStats)
class PlayerHeroStatsAdmin(admin.ModelAdmin):
    list_display = ['hero__name', 'player__personaname', 'last_played', 'games', 'win']

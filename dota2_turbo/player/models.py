from django.db import models

from dota2_turbo.authentication.models import SteamUser
from dota2_turbo.hero.models import Hero


class PlayerHeroStats(models.Model):
    class Meta:
        verbose_name = 'PlayerHeroStats'
        verbose_name_plural = 'PlayerHeroStats'
        ordering = ['-hero_id']
        unique_together = ('player', 'hero_id')

    hero = models.ForeignKey(
        Hero, on_delete=models.CASCADE, 
        related_name='player_heroes_stats'
    )
    player = models.ForeignKey(SteamUser, 
        on_delete=models.CASCADE, 
        related_name='player_heroes_stats'
    )
    last_played = models.DateTimeField(null=True, blank=True)
    games = models.IntegerField(default=0)
    win = models.IntegerField(default=0)
    with_games = models.IntegerField(default=0)
    with_win = models.IntegerField(default=0)
    against_games = models.IntegerField(default=0)
    against_win = models.IntegerField(default=0)

from django.db import models

from dota2_turbo.authentication.models import SteamUser
from dota2_turbo.hero.models import Hero, HeroFacet


class Match(models.Model):
    class Meta:
        verbose_name = "Match"
        verbose_name_plural = "Matches"
        unique_together = ('match_id', 'player')
        indexes = [
            models.Index(fields=["player", "match_id"]),
        ]
        
    player = models.ForeignKey(
        SteamUser, 
        on_delete=models.CASCADE, 
        related_name='matches'
    )
    hero = models.ForeignKey(
        Hero, 
        on_delete=models.CASCADE,
        related_name='matches'
    )
    hero_facet = models.ForeignKey(
        HeroFacet, 
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="matches"
    )
    match_id = models.BigIntegerField()
    kills = models.IntegerField()
    deaths = models.IntegerField()
    assists = models.IntegerField()
    win = models.BooleanField()
    rating_change = models.IntegerField()
    match_time = models.DateTimeField()
    duration = models.IntegerField(help_text="Duration in seconds")

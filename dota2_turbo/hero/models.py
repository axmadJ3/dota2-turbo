from decimal import Decimal

from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.postgres.indexes import GinIndex


class Hero(models.Model):
    class Meta:
        verbose_name = "Hero"
        verbose_name_plural = "Heroes"
        indexes = [
            models.Index(fields=['name']),
            GinIndex(fields=['positions']),
        ]

    hero_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=100, unique=True, db_index=True)
    image_url = models.URLField()
    positions = ArrayField(models.CharField(max_length=50), default=list)

    def __str__(self):
        return self.name


class HeroTier(models.Model):
    PERIOD_CHOICES = [
        ("month", "Last 30 days"),
        ("3months", "Last 90 days"),
        ("6months", "Last 180 days"),
    ]

    class Meta:
        verbose_name = 'HeroTier'
        verbose_name_plural = 'HeroTiers'
        unique_together = ("hero", "period")
        indexes = [
            models.Index(fields=["period"]),
            models.Index(fields=["hero"]),
            models.Index(fields=["tier"]),
        ]

    hero = models.ForeignKey(
        Hero, related_name="tiers", 
        on_delete=models.CASCADE
    )
    tier = models.CharField(max_length=2)
    winrate = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0.00'))
    pickrate = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0.00'))
    period = models.CharField(max_length=20, choices=PERIOD_CHOICES, default='6months')

    def __str__(self):
        return f"{self.hero.name} — {self.positions}: {self.tier}"


class HeroFacet(models.Model):
    class Meta:
        verbose_name = 'HeroFacet'
        verbose_name_plural = 'HeroFacets'
        unique_together = ("hero", "facet_id")
        indexes = [
            models.Index(fields=["hero"]),
            models.Index(fields=["tier"]),
        ]

    hero = models.ForeignKey(
        Hero,
        on_delete=models.CASCADE,
        related_name="facets"
    )
    facet_id = models.IntegerField()
    title = models.CharField(max_length=150)
    description = models.TextField()
    icon = models.CharField(max_length=50)
    color = models.CharField(max_length=50)
    gradient_id = models.IntegerField(default=0)
    winrate = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0.00'))
    pickrate = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0.00'))
    tier = models.CharField(max_length=2, default='NR')

    def __str__(self):
        return f"{self.hero.name}: facet {self.facet_id} — {self.title}"

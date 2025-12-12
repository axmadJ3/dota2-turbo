import json

from django.conf import settings
from django.core.management.base import BaseCommand

from dota2_turbo.hero.models import Hero, HeroFacet


FACETS_JSON = settings.BASE_DIR / "dota2_turbo/hero/feeds/facets.json"

class Command(BaseCommand):
    help = "Load hero facets from facets.json"

    def handle(self, *args, **kwargs):
        if not FACETS_JSON.exists():
            self.stderr.write(self.style.ERROR("facets.json.json not found"))
            return

        with open(FACETS_JSON, "r", encoding="utf-8") as f:
            data = json.load(f)

        created = 0
        for _, hero_block in data.items():
            hero_id = hero_block['hero_id']
            hero = Hero.objects.get(hero_id=hero_id)
              
            for facet in hero_block['facets']:
                HeroFacet.objects.update_or_create(
                    hero=hero,
                    facet_id=facet['id'],
                    defaults={
                        "title": facet["title"],
                        "description": facet["description"],
                        "icon": facet["icon"],
                        "color": facet["color"],
                        "gradient_id": facet["gradient_id"],
                        "tier": "NR",
                        "winrate": 0.0,
                        "pickrate": 0.0,
                    }
                )
                created += 1

        self.stdout.write(self.style.SUCCESS(
            f"Hero facets imported: {created}."
        ))

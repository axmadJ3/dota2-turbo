import json

from django.conf import settings
from django.core.management.base import BaseCommand

from dota2_turbo.hero.models import Hero


HEROES_JSON = settings.BASE_DIR / "dota2_turbo/hero/feeds/heroes.json"

class Command(BaseCommand):
    help = "Load heroes from heroes.json"

    def handle(self, *args, **kwargs):
        if not HEROES_JSON.exists():
            self.stderr.write(self.style.ERROR("heroes.json.json not found"))
            return

        with open(HEROES_JSON, "r", encoding="utf-8") as f:
            data = json.load(f)

        created = 0
        for entry in data:
            hero_id = entry["hero_id"]
            name = entry["hero"]
            image_url = entry.get("image_url", "")

            Hero.objects.create(
                hero_id=hero_id,
                name=name,
                image_url=image_url
            )
            created += 1

        self.stdout.write(self.style.SUCCESS(
            f"Heroes created: {created}."
        ))

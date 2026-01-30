import csv
import os

from django.core.management.base import BaseCommand
from dota2_turbo.authentication.models import SteamUser


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "--output",
            type=str,
            default="users.csv",
            help="Output CSV file path (default: users.csv)",
        ) 

    def handle(self, *args, **options):
        output_path = options["output"]

        users = SteamUser.objects.values_list("steamid32", flat=True)

        if not users.exists():
            self.stdout.write(self.style.WARNING("No Steam users found"))
            return

        os.makedirs(os.path.dirname(output_path), exist_ok=True) if "/" in output_path else None

        with open(output_path, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["account_id"])

            for steamid32 in users:
                writer.writerow([steamid32])

        self.stdout.write(
            self.style.SUCCESS(
                f"Exported {users.count()} steamid32 values to {output_path}"
            )
        )

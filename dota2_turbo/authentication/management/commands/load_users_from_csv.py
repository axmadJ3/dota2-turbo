import csv
import time
import requests

from django.conf import settings
from django.utils import timezone
from django.core.management.base import BaseCommand
from social_django.models import UserSocialAuth

from dota2_turbo.authentication.models import SteamUser


USERS_CSV = settings.BASE_DIR / "dota2_turbo/authentication/feeds/users.csv"

class Command(BaseCommand):
    help = 'Load users from authentication/feeds/users.csv and fills in their profile via OpenDota'

    def handle(self, *args, **kwargs):
        if not USERS_CSV.exists():
            self.stderr.write(self.style.ERROR("users.csv not found"))
            return

        with open(USERS_CSV, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            created = 0
            for row in reader:
                if not row:
                    continue

                steamid = row[0].strip()

                if steamid.lower() == 'account_id':
                    continue
                try:
                    full_steamid = str(int(steamid) + 76561197960265728)
                except ValueError:
                    self.stdout.write(self.style.WARNING(f"Invalid Steam ID: {steamid}"))
                    continue

                if SteamUser.objects.filter(steamid32=steamid).exists():
                    continue
                if UserSocialAuth.objects.filter(uid=full_steamid, provider='steam').exists():
                    continue

                r = requests.get(f'https://api.opendota.com/api/players/{steamid}')
                if not r.ok:
                    continue

                profile = r.json().get('profile')
                if not profile:
                    continue

                full_steamid = str(int(steamid) + 76561197960265728)
                user = SteamUser.objects.create_user(
                    steamid=full_steamid,
                    steamid32=steamid,
                    password=None,
                    personaname=profile.get('personaname') or '',
                    profileurl=profile.get('profileurl') or '',
                    avatar=profile.get('avatar') or '',
                    avatarmedium=profile.get('avatarmedium') or '',
                    avatarfull=profile.get('avatarfull') or '',
                    is_active=True,
                    date_joined=timezone.now(),
                )

                if not UserSocialAuth.objects.filter(user=user, provider='steam').exists():
                    UserSocialAuth.objects.create(
                        user=user,
                        provider='steam',
                        uid=full_steamid,
                        extra_data={'player': {
                            'personaname': user.personaname,
                            'profileurl': user.profileurl,
                            'avatar': user.avatar,
                            'avatarmedium': user.avatarmedium,
                            'avatarfull': user.avatarfull,
                        }}
                    )
                    
                created += 1
                self.stdout.write(f"Added: {profile.get('personaname', steamid)}")
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS(f"\nTotal users added: {created}"))

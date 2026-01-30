from django.db import transaction
from django.db.models import Sum

from dota2_turbo.authentication.models import SteamUser


def remove_users():
    users = (
        SteamUser.objects
        .annotate(total_rating=Sum("matches__rating_change"))
        .filter(total_rating__lt=500)
    )

    count = users.count()
    with transaction.atomic():
        users.delete()

    return count

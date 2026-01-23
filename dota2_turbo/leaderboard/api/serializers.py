from rest_framework import serializers

from dota2_turbo.authentication.models import SteamUser


class LeaderboardSerializer(serializers.ModelSerializer):
    total_rating = serializers.IntegerField()
    rank = serializers.IntegerField()
    is_friend = serializers.BooleanField()
    is_me = serializers.BooleanField()

    class Meta:
        model = SteamUser
        fields = (
            "steamid",
            "personaname",
            "avatar",
            "total_rating",
            "rank",
            "is_friend",
            "is_me",
        )

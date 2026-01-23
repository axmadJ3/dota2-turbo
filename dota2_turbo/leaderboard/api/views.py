from datetime import timedelta

from django.utils import timezone
from rest_framework.generics import GenericAPIView
from rest_framework.pagination import PageNumberPagination

from dota2_turbo.leaderboard.api.serializers import LeaderboardSerializer
from dota2_turbo.leaderboard.utils import calculate_total_rating
from dota2_turbo.player.tasks import parse_steam_friendlist


class LeaderboardPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 100


class LeaderboardAPIView(GenericAPIView):
    serializer_class = LeaderboardSerializer
    pagination_class = LeaderboardPagination

    def get_queryset(self):
        return calculate_total_rating()

    def get(self, request, *args, **kwargs):
        users = list(self.get_queryset())

        friend_ids = set()
        my_rank = None

        if request.user.is_authenticated:
            user = request.user
            needs_update = (
                not user.steam_friends_updated_at or
                timezone.now() - user.steam_friends_updated_at > timedelta(days=3)
            )
            if needs_update:
                parse_steam_friendlist.delay(user.steamid)

            friend_ids = set(user.steam_friends or [])

        for idx, user_obj in enumerate(users, start=1):
            user_obj.rank = idx
            user_obj.is_friend = user_obj.steamid in friend_ids
            user_obj.is_me = (
                request.user.is_authenticated and
                user_obj.steamid == request.user.steamid
            )

            if request.user.is_authenticated and user_obj.id == request.user.id:
                my_rank = user_obj

        page = self.paginate_queryset(users)
        serializer = self.get_serializer(page, many=True)

        response = self.get_paginated_response(serializer.data)
        response.data["my_rank"] = (
            self.get_serializer(my_rank).data if my_rank else None
        )
        return response

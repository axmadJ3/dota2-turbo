from django.contrib import admin

from .models import SteamUser


@admin.register(SteamUser)
class SteamUserAdmin(admin.ModelAdmin):
    list_display = ['personaname', 'steamid', 'steamid32']
    search_fields = ['personaname', 'steamid', 'steamid32']

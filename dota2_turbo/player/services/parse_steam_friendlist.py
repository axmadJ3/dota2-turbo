import requests
from requests.exceptions import RequestException

from decouple import config


API_KEY = config('STEAM_API_KEY')

def parse_friendlist(steam_id, api_key=None):
    if api_key is None:
        api_key = API_KEY

    if not api_key:
        return []

    url = (
        "http://api.steampowered.com/ISteamUser/GetFriendList/v0001/"
    )
    params = {
        'key': api_key,
        'steamid': steam_id,
        'relationship': 'friend'
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        friends = data.get('friendslist', {}).get('friends', [])
        return [str(friend.get('steamid')) for friend in friends if friend.get('steamid')]
    except (RequestException, ValueError, KeyError):
        return []

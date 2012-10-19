# Create your views here.
import requests

from django.http import HttpResponse
from django.template import Context, loader
from django.utils.html import escape
from django.contrib.auth.decorators import login_required
from social_auth.models import UserSocialAuth
from towerofdimensions.models import Steam, Player
from django.conf import settings
from django.template import RequestContext


def info(request):
    try:
        steam = Steam.objects.get(steamId = request.user.social_auth.get(user_id = request.user.id).uid)
        player = steam.player

        steamId = request.user.social_auth.get(user_id = request.user.id).uid.partition("http://steamcommunity.com/openid/id/")
        r = requests.get('http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key='+settings.STEAM_HASH+'&steamids='+steamId[2])
        player.name= r.json["response"]["players"][0]["personaname"]
        player.avatar = r.json["response"]["players"][0]["avatarfull"]

        player.save()

    except Steam.DoesNotExist: 
        steamId = request.user.social_auth.get(user_id = request.user.id).uid.partition("http://steamcommunity.com/openid/id/")
        r = requests.get('http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key='+settings.STEAM_HASH+'&steamids='+steamId[2])
        player = Player(name= r.json["response"]["players"][0]["personaname"], avatar = r.json["response"]["players"][0]["avatarfull"], coins = 300 ) 
        player.save()

        steam = Steam(steamId = request.user.social_auth.get(user_id = request.user.id).uid, player = player)
        steam.save()

    t = loader.get_template('game.html')
    c = RequestContext(request,{
        "player" : player,
    })

    return HttpResponse(t.render(c))
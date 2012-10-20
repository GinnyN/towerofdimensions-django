from django.http import HttpResponseRedirect
from django.http import HttpRequest
from social_auth.models import UserSocialAuth, SOCIAL_AUTH_MODELS_MODULE
from social_auth.backends.exceptions import AuthAlreadyAssociated
from django.utils.translation import ugettext
from pprint import pprint
from towerofdimensions.models import Steam, Player

def steam(request, *args, **kwargs):
    player = Player(coins = 500)
    player.save()
    steam = Steam(steamId= request.GET.get("openid.claimed_id","not found"), player = player, userId = request.user.username)
    steam.save()
    request.user.save()
    return request

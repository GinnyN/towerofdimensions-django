# Create your views here.
import requests

from django.http import HttpResponse
from django.template import Context, loader
from django.utils.html import escape
from django.contrib.auth.decorators import login_required
from social_auth.models import UserSocialAuth
from towerofdimensions.models import Steam, Player, Mercenary
from django.conf import settings
from django.template import RequestContext


def setup(request):
    
    steam = Steam.objects.get(steamId = request.user.social_auth.get(user_id = request.user.id).uid)
    player = steam.player

    mercenaries = Mercenary.objects.filter(player = player)

    t = loader.get_template('mercenaries.html')
    c = RequestContext(request,{
        "mercenaries" : mercenaries,
    })

    return HttpResponse(t.render(c))

def fullView(request, mercenary_id):

    steam = Steam.objects.get(steamId = request.user.social_auth.get(user_id = request.user.id).uid)
    player = steam.player

    mercenary = Mercenary.objects.get(id = mercenary_id)

    t = loader.get_template('mercenaries-fullview.html')
    c = RequestContext(request,{
        "mercenary" : mercenary,
    })

    return HttpResponse(t.render(c))

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

@login_required
def setup(request):
    
    steam = Steam.objects.get(steamId = request.user.social_auth.get(user_id = request.user.id).uid)
    player = steam.player

    mercenaries = Mercenary.objects.filter(player = player)

    t = loader.get_template('mercenaries.html')
    c = RequestContext(request,{
        "mercenaries" : mercenaries,
    })

    return HttpResponse(t.render(c))

@login_required
def fullView(request, mercenary_id):

    steam = Steam.objects.get(steamId = request.user.social_auth.get(user_id = request.user.id).uid)
    player = steam.player

    mercenary = Mercenary.objects.get(id = mercenary_id)

    description = requests.get(settings.STATIC_URL+"/towerofdimensions/json/characters.json").json["character"][mercenary.idBase]["description"]

    itemsJson = requests.get(settings.STATIC_URL+"/towerofdimensions/json/items.json")

    if(mercenary.item1 != None):
        item1 = itemsJson.json["item"][mercenary.item1.idBase]
    else:
        item1 = -1

    if(mercenary.item2 != None):
        item2 = itemsJson.json["item"][mercenary.item2.idBase]
    else:
        item2 = -1

    if(mercenary.item3 != None):
        item3 = itemsJson.json["item"][mercenary.item3.idBase]
    else:
        item3 = -1

    if(mercenary.item4 != None):
        item4 = itemsJson.json["item"][mercenary.item4.idBase]
    else:
        item4 = -1

    if(mercenary.item5 != None):
        item5 = itemsJson.json["item"][mercenary.item5.idBase]
    else:
        item5 = -1

    if(mercenary.item6 != None):
        item6 = itemsJson.json["item"][mercenary.item6.idBase]
    else:
        item6 = -1

    t = loader.get_template('mercenaries-fullview.html')
    c = RequestContext(request,{
        "mercenary" : mercenary,
        "description": description,
        "item1": item1,
        "item2": item2,
        "item3": item3,
        "item4": item4,
        "item5": item5,
        "item6": item6
    })

    return HttpResponse(t.render(c))

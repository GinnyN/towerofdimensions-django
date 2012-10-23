# Create your views here.
import requests

from django.http import HttpResponse
from django.template import Context, loader
from django.utils.html import escape
from django.contrib.auth.decorators import login_required
from social_auth.models import UserSocialAuth
from towerofdimensions.models import Steam, Player, Mercenary, Item
from django.conf import settings
from django.template import RequestContext

@login_required
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

        newUser = requests.get(settings.STATIC_URL+"/towerofdimensions/json/newUser.json")
        mercenaries = requests.get(settings.STATIC_URL+"/towerofdimensions/json/characters.json")
        items = requests.get(settings.STATIC_URL+"/towerofdimensions/json/items.json")

        count = 0
        while (count < len (newUser.json["user"]["mercenarios"])):
            baseId = newUser.json["user"]["mercenarios"][count]
            character = mercenaries.json["character"][baseId]
            
            c = 1
            while (c < 7):
                if(character["item"+str(c)] != -1):
                    item = Item(player = player, flag = 1, idBase = character["item"+str(c)])
                    character["item"+str(c)] = item 
                    item.save()
                    itemJson = items.json["item"][item.idBase]
                    character["hpMax"] = character["hpMax"] + itemJson["bonusHpMax"]
                    character["agilidad"] = character["agilidad"] + itemJson["bonusAgilidad"]
                    character["destreza"] = character["destreza"] + itemJson["bonusDestreza"]
                    character["constitucion"] = character["constitucion"] + itemJson["bonusConstitucion"]
                    character["fuerza"] = character["fuerza"] + itemJson["bonusFuerza"]
                    character["inteligencia"] = character["inteligencia"] + itemJson["bonusInteligencia"]
                    character["sabiduria"] = character["sabiduria"] + itemJson["bonusSabiduria"]
                    character["carisma"] = character["carisma"] + itemJson["bonusCarisma"]
                    character["poder"] = character["poder"] + itemJson["bonusPoder"]
                    character["marcial"] = character["marcial"] + itemJson["bonusMarcial"]
                    character["stealth"] = character["stealth"] + itemJson["bonusStealth"]
                    character["magia"] = character["magia"] + itemJson["bonusMagia"]
                    character["tecnologia"] = character["tecnologia"] + itemJson["bonusTecnologia"]
                else:
                    character["item"+str(c)] = None
                c = c + 1

            mercenary = Mercenary(player = player, idBase= character["idBase"], nombre = character["nombre"], nivel = character["nivel"], exp = character["exp"], agilidad = character["agilidad"], destreza = character["destreza"], constitucion = character["constitucion"], fuerza = character["fuerza"], inteligencia = character["inteligencia"], sabiduria = character["sabiduria"], carisma = character["carisma"], poder = character["poder"], marcial = character["marcial"], stealth = character["stealth"], magia = character["magia"], tecnologia = character["tecnologia"],  crecimientoAgilidad = character["crecimientoAgilidad"], crecimientoDestreza = character["crecimientoDestreza"], crecimientoConstitucion = character["crecimientoConstitucion"], crecimientoFuerza = character["crecimientoFuerza"], crecimientoInteligencia = character["crecimientoInteligencia"], crecimientoSabiduria = character["crecimientoSabiduria"], crecimientoCarisma = character["crecimientoCarisma"], crecimientoPoder = character["crecimientoPoder"], crecimientoMarcial = character["crecimientoMarcial"], crecimientoStealth = character["crecimientoStealth"],  crecimientoMagia = character["crecimientoMagia"], crecimientoTecnologia = character["crecimientoTecnologia"], hpCalculo = character["hpCalculo"], item1 = character["item1"], item2 = character["item2"], item3 = character["item3"], item4 = character["item4"], item5 = character["item5"], item6 = character["item6"], hpMax = character["hpMax"], hpActual = character["hpActual"], misionActual = character["misionActual"])
            mercenary.save()
            count = count + 1

    t = loader.get_template('game.html')
    c = RequestContext(request,{
        "player" : player,
    })

    return HttpResponse(t.render(c))
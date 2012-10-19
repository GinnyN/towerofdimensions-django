from django.db import models

# Create your models here.
class Player(models.Model):
    coins = models.IntegerField()
    name = models.CharField(max_length=300)
    avatar = models.CharField(max_length=1000)

class Steam(models.Model):
    steamId = models.CharField(max_length=300)
    player = models.ForeignKey(Player)
    

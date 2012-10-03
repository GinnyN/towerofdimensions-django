from django.db import models

# Create your models here.
class Player(models.Model):
    coins = models.IntegerField()

class Steam(models.Model):
    steamId = models.CharField(max_length=200)
    player = models.ForeignKey(Player)

from django.db import models
from authentication.models import Account
import datetime


class Player(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE,)
    gold = models.BigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    level = models.IntegerField(default=0)


class Equipment(models.Model):
    name = models.TextField(max_length=30, null=False, unique=True)
    price = models.IntegerField(default=0)
    text_name = models.TextField(max_length=20)
    intro = models.TextField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class EquipRecord(models.Model):
    equipment = models.ForeignKey(Equipment, on_delete=True)
    player = models.ForeignKey(Player, on_delete=True)
    number = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("equipment", "player")
        index_together = ("equipment", "player")





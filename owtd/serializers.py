from django.shortcuts import render

# Create your views here.
from rest_framework import serializers
from authentication.serializers import AccountSerializer
from owtd.models import Player, Equipment, EquipRecord


class PlayerSerializer(serializers.ModelSerializer):
    account = AccountSerializer(required=True)

    class Meta:
        model = Player

        fields = ('id', 'account', 'gold', 'level', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at', 'account')

    def update(self, instance, validated_data):
        instance.level = validated_data.get('level', instance.level)
        instance.gold = validated_data.get('gold', instance.gold)
        instance.save()
        return instance

    def get_validation_exclusions(self, *args, **kwargs):
        exclusions = super(PlayerSerializer, self).get_validation_exclusions()

        return exclusions + ['account']


class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = ('id', 'name', 'price', 'text_name', 'intro', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at', )


class EquipRecordSerializer(serializers.ModelSerializer):
    player = PlayerSerializer(required=True)
    equipment = EquipmentSerializer(required=True)

    class Meta:
        model = EquipRecord

        fields = ('id', 'player', 'equipment', 'created_at', 'updated_at', 'number')
        read_only_fields = ('id', 'created_at', 'updated_at', 'player', 'equipment')


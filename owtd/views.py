from rest_framework import permissions, viewsets
from rest_framework.response import Response

from owtd.models import Player, EquipRecord, Equipment
#from owtd.permissions import
from owtd.serializers import PlayerSerializer, EquipRecordSerializer, EquipmentSerializer
#from owtd.permissions import IsAccountOfPlayer
from rest_framework.decorators import action, permission_classes
from games.utils.metadata import Metadata, MetadataSerializer, MetadataListSerializer, MetaListdata


class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer

    # def get_permissions(self):
    #     if self.request.method in permissions.SAFE_METHODS:
    #         return (permissions.AllowAny(),)
    #     return (permissions.IsAuthenticated(), IsAccountOfPlayer(), )
    @action(methods=['get'], detail=False)
    @permission_classes((permissions.IsAuthenticated,))
    def current(self, request):
        player = self.queryset.get(account=request.user)
        data = self.serializer_class(player).data
        return Response(Metadata(data=data).serialized_data())

    def update(self, request, pk):
        data = request.data
        try:
            player = self.queryset.get(id=pk);

            player.gold = data['gold']

            player.level = data['level']
            player.save()
            result = self.serializer_class(player).data
        except Player.DoesNotExist:
            return Response(Metadata(status="NotFound", message="No such player").serialized_data())
        return Response(Metadata(data=result).serialized_data())


def perform_create(self, serializer):
    instance = serializer.save(account=self.request.user)

    return super(PlayerViewSet, self).perform_create(serializer)


class AccountPlayerViewSet(viewsets.ViewSet):
    queryset = Player.objects.select_related('account').all()
    serializer_class = PlayerSerializer

    def list(self, request, account_username):
        queryset = self.queryset.get(account__username=account_username)
        serializer = self.serializer_class(queryset)
        return Response(serializer.data)




class PlayerEquipRecordViewSet(viewsets.ViewSet):
    queryset = EquipRecord.objects.select_related('equipment', 'player').all()
    serializer_class = EquipRecordSerializer

    def list(self, request, player_pk):
        records = self.queryset.filter(player__account=request.user, player=player_pk)
        total = records.count()
        data = self.serializer_class(records, many=True).data
        return Response(MetaListdata(data=data, total=total).serialized_data())


class EquipRecordViewSet(viewsets.ModelViewSet):
    queryset = EquipRecord.objects.select_related('equipment', 'player').all()
    serializer_class = EquipRecordSerializer


class EquipmentViewSet(viewsets.ModelViewSet):
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer

    @action(methods=['post'], detail=True)
    def purchase(self, request, pk):
        equip = self.queryset.get(id=pk)
        player = Player.objects.get(account=request.user)

        if player.gold < equip.price:
            return Response(Metadata(status="forbidden", message="No enough gold").serialized_data())
        try:
            record = EquipRecord.objects.get(player=player, equipment=equip)
            record.number += 1
            record.save()
        except EquipRecord.DoesNotExist:
            record = EquipRecord(equipment=equip, player=player, number=1)
            record.save()
        data = EquipRecordSerializer(record).data
        return Response(Metadata(data=data).serialized_data())

    @action(methods=['post'], detail=True)
    def use(self, request, pk):
        try:
            record = EquipRecord.objects.get(player__account=request.user, equipment=pk)
            if record.number is 0:
                return Response(Metadata(status="forbidden", message="Your don't have this equipment"))
            record.number -= 1
            record.save()
        except EquipRecord.DoesNotExist:
            return Response(Metadata(status="forbidden", message="Your don't have this equipment"))
        data = EquipRecordSerializer(record).data
        return Response(Metadata(data=data).serialized_data())

    def list(self, request):
        count = self.queryset.count()
        data = self.serializer_class(self.queryset, many=True).data
        return Response(MetaListdata(data=data, total=count).serialized_data())
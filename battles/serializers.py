from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField
from .models import *
from chats.serializers import *
from users.serializers import *
from monsters.serializers import *
from equipments.serializers import *


class BattleSerializer(serializers.ModelSerializer):

    character = CharacterSerializer()
    monster = MonsterSerializer()
    equipment = EquipmentSerializer()

    class Meta:
        model = Battle
        fields = '__all__'

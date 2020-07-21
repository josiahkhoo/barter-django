from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField
from .models import *
from chats.serializers import *
from users.serializers import *
from monsters.serializers import *


class BattleSerializer(serializers.ModelSerializer):

    user = UserSerializer()
    monster = MonsterSerializer()

    class Meta:
        model = Battle
        fields = '__all__'

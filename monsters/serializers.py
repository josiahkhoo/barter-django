from rest_framework import serializers
from .models import *


class MonsterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Monster
        fields = [
            'id',
            'name',
            'duration',
            'appearance_config',
            'level',
            'is_active'
        ]

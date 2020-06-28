from rest_framework import serializers
from .models import *


class CharacterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Character
        fields = [
            'id',
            'name',
            'appearance_config',
            'user'
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        """
        FIXME: Sets default level to 1 temporarily, to set logic to
        incorporate this into the model in the future
        """
        data["level"] = 1
        return data

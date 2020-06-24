from rest_framework import serializers
from .models import *


class CharacterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Character
        fields = '__all__'

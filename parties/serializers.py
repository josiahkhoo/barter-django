from rest_framework import serializers
from .models import *
from chats.serializers import *


class PartyBaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Party
        fields = '__all__'


class PartySerializer(PartyBaseSerializer):

    chat = ChatSerializer()
    users = UserSerializer(many=True)

    def get_current_user(self, instance):
        if self.context and "user" in self.context:
            user = self.context.get("user")
            return UserSerializer(user).data
        return None

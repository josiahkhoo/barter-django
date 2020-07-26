from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from .models import *
from users.serializers import *


class MessageSerializer(serializers.ModelSerializer):

    username = SerializerMethodField()

    class Meta:
        model = Message
        fields = "__all__"

    def get_is_current_user(self, instance):
        if self.context and "user" in self.context:
            user = self.context.get("user")
            if instance.user == user:
                return True
        return False

    def get_username(self, instance):
        return instance.user.username


class ReceiptSerializer(serializers.ModelSerializer):

    class Meta:
        model = Receipt
        fields = "__all__"


class ChatSerializer(serializers.ModelSerializer):

    # messages = serializers.SerializerMethodField()
    messages = MessageSerializer(many=True)

    class Meta:
        model = Chat
        fields = "__all__"
        # extra_fields = [
        #     "messages"
        # ]

    def get_messages(self, instance):
        """
        Returns first 20 messages sorted by datetime created
        """
        if self.context and "oldest_message_id" in self.context:
            oldest_message_id = self.context.get("oldest_message_id")
            messages = instance.messages.filter(
                pk__lt=oldest_message_id
            ).order_by('-datetime_created')[:20]
        else:
            messages = instance.messages.order_by('-datetime_created')[:20]
        return MessageSerializer(
            messages,
            context=self.context,
            many=True
        ).data


class ConversationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Conversation
        fields = "__all__"

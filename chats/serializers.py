from rest_framework import serializers
from .models import *
from users.serializers import *


class MessageSerializer(serializers.ModelSerializer):

    user = UserSerializer()
    is_current_user = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = "__all__"

    def get_is_current_user(self, instance):
        if self.context and "user" in self.context:
            user = self.context.get("user")
            if instance.user == user:
                return True
        return False


class ReceiptSerializer(serializers.ModelSerializer):

    class Meta:
        model = Receipt
        fields = "__all__"


class ChatSerializer(serializers.ModelSerializer):

    # messages = serializers.SerializerMethodField()
    receipt = serializers.SerializerMethodField()
    unread_messages = serializers.SerializerMethodField()

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

    def get_receipt(self, instance):
        if self.context and "user" in self.context:
            user = self.context.get("user")
            receipt = instance.receipts.filter(user=user).first()
            if receipt:
                return ReceiptSerializer(instance=receipt).data
            else:
                return None
        else:
            return None

    def get_unread_messages(self, instance):
        if self.context and "user" in self.context:
            user = self.context.get("user")
            receipt = instance.receipts.filter(user=user).first()
            other_messages = instance.messages.exclude(user=user)
            if receipt:
                datetime_updated = receipt.datetime_updated
                unread_messages = other_messages.filter(
                    datetime_created__gt=datetime_updated).count()
                return unread_messages
            else:
                return other_messages.count()
        return None

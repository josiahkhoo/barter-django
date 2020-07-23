from django.db import models
from django.utils import timezone
from users.models import *
from services.firestore.firestore import db as firestore_db
from chats.utils import *


# Create your models here.
class Chat(models.Model):

    datetime_created = models.DateTimeField(default=timezone.now)

    def get_user_list(self):
        if self.party:
            return self.party.users.all()


class Message(models.Model):

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='messages',
        null=True, blank=True)
    datetime_created = models.DateTimeField(default=timezone.now)
    content = models.TextField()
    chat = models.ForeignKey(
        Chat, on_delete=models.CASCADE, related_name='messages', null=True, blank=True)
    message_type = models.IntegerField(choices=MessageType.choices())
    recipient_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='incoming_messages',
        null=True, blank=True
    )

    @staticmethod
    def create_message_system(chat, content):
        """
        Creates and sends a message to the chat from the system
        """
        message = Message(
            content=content,
            chat=chat,
            message_type=int(MessageType.MESSAGE_SYSTEM)
        )
        message.save()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.send_to_firebase()

    def to_dict(self):
        data = {
            "content": self.content,
            "datetime_created": self.datetime_created,
            "message_type": self.message_type,
        }
        if self.chat_id:
            data["chat_id"] = self.chat.id
        if self.user:
            data["user_id"] = self.user.id
        if self.recipient_user:
            data["recipient_user_id"] = self.recipient_user.id
        return data

    def send_to_firebase(self):
        doc_ref = firestore_db.collection(u'messages'
                                          ).document(u'{}'.format(self.id))
        doc_ref.set(
            self.to_dict()
        )


class Receipt(models.Model):

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='receipts'
    )
    chat = models.ForeignKey(
        Chat, on_delete=models.CASCADE, related_name='receipts'
    )
    datetime_updated = models.DateTimeField(auto_now=True)

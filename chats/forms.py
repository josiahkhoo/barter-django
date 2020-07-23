from django import forms
from .models import *


class MessageForm(forms.ModelForm):

    class Meta:
        model = Message
        fields = [
            'user',
            'content',
            'chat',
            'message_type',
            'recipient_user'
        ]

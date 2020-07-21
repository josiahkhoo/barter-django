from django import forms
from .models import *


class BattleForm(forms.ModelForm):

    class Meta:
        model = Battle
        fields = [
            'user',
            'monster'
        ]

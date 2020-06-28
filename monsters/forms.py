from django import forms
from .models import Monster


class MonsterForm(forms.ModelForm):

    class Meta:
        model = Monster
        fields = (
            'name',
            'level',
            'duration',
            'appearance_config'
        )

from battles.utils import BattleState
from django.db import models
from characters.models import *
from monsters.models import *
from battles.utils import *
from equipments.models import *

# Create your models here.


class Battle(models.Model):

    character = models.ForeignKey(
        Character, on_delete=models.CASCADE, related_name='battles')
    monster = models.ForeignKey(
        Monster, on_delete=models.CASCADE, related_name='battles')
    datetime_created = models.DateTimeField(default=timezone.now)
    datetime_updated = models.DateTimeField(auto_now=True)
    state = models.IntegerField(
        choices=BattleState.choices(), default=BattleState.ONGOING)
    equipment = models.ForeignKey(
        Equipment, on_delete=models.CASCADE, related_name='battles', null=True,
        blank=True
    )

    def set_state_complete(self):
        if self.state != BattleState.ONGOING:
            raise Exception("Battle state is not ongoing")
        self.state = int(BattleState.COMPLETED)
        self.equipment = self.monster.get_drop()
        self.save()
        return self

    def set_state_forfeited(self):
        if self.state != BattleState.ONGOING:
            raise Exception("Battle state is not ongoing")
        self.state = int(BattleState.FORFEITED)
        self.save()
        return self

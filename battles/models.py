from battles.utils import BattleState
from django.db import models
from users.models import *
from monsters.models import *
from battles.utils import *

# Create your models here.


class Battle(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    monster = models.ForeignKey(Monster, on_delete=models.CASCADE)
    datetime_created = models.DateTimeField(default=timezone.now)
    datetime_updated = models.DateTimeField(auto_now=True)
    state = models.IntegerField(
        choices=BattleState.choices(), default=BattleState.ONGOING)

    def set_state_complete(self):
        if self.state != BattleState.ONGOING:
            raise Exception("Battle state is not ongoing")
        self.state = int(BattleState.COMPLETED)
        self.save()
        return self

    def set_state_forfeited(self):
        if self.state != BattleState.ONGOING:
            raise Exception("Battle state is not ongoing")
        self.state = int(BattleState.FORFEITED)
        self.save()
        return self

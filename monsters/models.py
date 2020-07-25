from django.db import models
from django.contrib.postgres.fields import JSONField
from django.utils import timezone
from equipments.models import *
import random
# Create your models here.


class Monster(models.Model):
    name = models.CharField(max_length=100, unique=True)
    level = models.IntegerField()
    # duration is in seconds preferably
    duration = models.IntegerField()
    appearance_config = JSONField()
    datetime_added = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    party_size = models.IntegerField(default=1)
    drop_set = models.ForeignKey(
        Set, on_delete=models.CASCADE, related_name='monsters')

    def get_drop(self):
        # 40% helmet
        # 30% armour
        # 20% shield
        # 10% sword
        possible_equipments = self.drop_set.equipments
        item_type = [0] * 40 + [1] * 30 + [2] * 20 + [3] * 10
        picked_item_type = random.choice(item_type)
        picked_item = possible_equipments.filter(
            equipment_type=picked_item_type).first()
        return picked_item

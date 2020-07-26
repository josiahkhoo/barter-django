from django.db import models
from django.contrib.postgres.fields import JSONField, ArrayField
from django.utils import timezone
from users.models import User
from equipments.models import Equipment
from equipments.utils import *
# Create your models here.


class Character(models.Model):
    name = models.CharField(max_length=15)
    appearance_config = JSONField()
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='characters')
    datetime_added = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    currently_equipped = "False"

    def equip(self, equipment):
        battles = self.battles.all()
        equipments = list(
            filter(lambda x: x, map(lambda x: x.equipment, battles)))
        if equipment not in equipments:
            raise Exception("Equipment not in inventory")
        if equipment.equipment_type == int(EquipmentType.HELMET):
            self.appearance_config["ValueList"][5] = \
                equipment.appearance_config["ValueList"][5]
        elif equipment.equipment_type == int(EquipmentType.CHEST):
            self.appearance_config["ValueList"][8] = \
                equipment.appearance_config["ValueList"][8]
        elif equipment.equipment_type == int(EquipmentType.SHIELD):
            self.appearance_config["ValueList"][13] = \
                equipment.appearance_config["ValueList"][13]
        elif equipment.equipment_type == int(EquipmentType.WEAPON):
            self.appearance_config["ValueList"][9] = \
                equipment.appearance_config["ValueList"][9]
        else:
            raise Exception("Can't equip specified item")
        self.save()
        return self

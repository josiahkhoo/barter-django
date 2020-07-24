from django.db import models
from django.contrib.postgres.fields import JSONField
from equipments.utils import *

# Create your models here.


class Set(models.Model):

    name = models.CharField(max_length=100, unique=True)


class Equipment(models.Model):

    name = models.CharField(max_length=100, unique=True)
    appearance_config = JSONField()
    equipment_type = models.IntegerField(choices=EquipmentType.choices())
    equipment_set = models.ForeignKey(
        Set, on_delete=models.CASCADE, related_name='equipments')

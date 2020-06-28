from django.db import models
from django.contrib.postgres.fields import JSONField
from django.utils import timezone

# Create your models here.


class Monster(models.Model):
    name = models.CharField(max_length=100, unique=True)
    level = models.IntegerField()
    # duration is in seconds preferably
    duration = models.IntegerField()
    appearance_config = JSONField()
    datetime_added = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)

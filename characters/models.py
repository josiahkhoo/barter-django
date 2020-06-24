from django.db import models
from django.contrib.postgres.fields import JSONField, ArrayField
from users.models import User

# Create your models here.


class Character(models.Model):
    name = models.CharField(max_length=15)
    appearance_config = JSONField()
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='characters')
    is_active = models.BooleanField(default=True)

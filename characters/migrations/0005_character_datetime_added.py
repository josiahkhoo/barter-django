# Generated by Django 3.0.2 on 2020-06-28 07:51

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('characters', '0004_auto_20200624_0824'),
    ]

    operations = [
        migrations.AddField(
            model_name='character',
            name='datetime_added',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]

# Generated by Django 3.0.2 on 2020-07-25 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monsters', '0005_monster_drop_set'),
    ]

    operations = [
        migrations.AddField(
            model_name='monster',
            name='drop_rate',
            field=models.IntegerField(default=40),
            preserve_default=False,
        ),
    ]

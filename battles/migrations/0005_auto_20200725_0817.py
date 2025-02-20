# Generated by Django 3.0.2 on 2020-07-25 08:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('characters', '0005_character_datetime_added'),
        ('battles', '0004_auto_20200725_0815'),
    ]

    operations = [
        migrations.AlterField(
            model_name='battle',
            name='character',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='battles', to='characters.Character'),
        ),
    ]

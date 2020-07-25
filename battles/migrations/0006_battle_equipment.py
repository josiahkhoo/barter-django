# Generated by Django 3.0.2 on 2020-07-25 09:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('equipments', '0001_initial'),
        ('battles', '0005_auto_20200725_0817'),
    ]

    operations = [
        migrations.AddField(
            model_name='battle',
            name='equipment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='battles', to='equipments.Equipment'),
        ),
    ]

# Generated by Django 3.0.2 on 2020-07-25 08:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('equipments', '0001_initial'),
        ('monsters', '0004_monster_party_size'),
    ]

    operations = [
        migrations.AddField(
            model_name='monster',
            name='drop_set',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='monsters', to='equipments.Set'),
            preserve_default=False,
        ),
    ]

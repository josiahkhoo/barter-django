# Generated by Django 3.0.2 on 2020-06-28 08:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monsters', '0002_auto_20200628_0751'),
    ]

    operations = [
        migrations.AlterField(
            model_name='monster',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]

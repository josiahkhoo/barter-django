# Generated by Django 3.0.2 on 2020-07-21 08:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chats', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Party',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('datetime_updated', models.DateTimeField(auto_now=True)),
                ('access_code', models.CharField(blank=True, max_length=6, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('chat', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='party', to='chats.Chat')),
                ('leader', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='parties_in_charge', to=settings.AUTH_USER_MODEL)),
                ('users', models.ManyToManyField(blank=True, related_name='parties', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PartyEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('party_event_type', models.IntegerField(choices=[(0, 'UI_PARTY_UPDATE'), (1, 'UI_PARTY_COMPLETE')])),
                ('party', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='parties.Party')),
            ],
        ),
    ]

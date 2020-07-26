from os import access
from django.db import models, IntegrityError
from chats.models import *
from parties.utils import *
from monsters.models import *
from services.firestore.firestore import db as firestore_db
from django.core.cache import cache
import datetime
import uuid

# Create your models here.


class Party(models.Model):

    monster = models.ForeignKey(
        Monster, related_name='parties', on_delete=models.CASCADE)
    users = models.ManyToManyField(User, blank=True, related_name='parties')
    datetime_created = models.DateTimeField(default=timezone.now)
    datetime_updated = models.DateTimeField(auto_now=True)
    chat = models.OneToOneField(
        Chat, null=True, blank=True, on_delete=models.CASCADE,
        related_name='party')
    access_code = models.CharField(
        max_length=6, unique=True, blank=True)
    is_active = models.BooleanField(default=True)
    state = models.IntegerField(
        choices=PartyState.choices(), default=0
    )

    def save(self, *args, **kwargs):
        if not self.access_code:
            self.access_code = self.get_generated_code()
        success = False
        errors = 0
        while not success:
            try:
                super().save(*args, **kwargs)
            except IntegrityError:
                errors += 1
                if errors > 3:
                    # tried 3 times, still fail. raise the integrity error
                    raise
                else:
                    self.access_code = self.get_generated_code()
            else:
                success = True
        # generate a chat object
        if not (self.chat):
            chat = Chat()
            chat.save()
            self.chat = chat
        super().save(*args, **kwargs)

    def get_generated_code(self):
        return uuid.uuid4().hex[:6].upper()

    def add_user(self, user):
        self.users.add(user)
        Message.create_message_system(
            content="{} has joined the party!".format(user.username),
            chat=self.chat
        )
        PartyEvent.create_ui_party_update(
            party=self
        )

    def remove_user(self, user):
        """
        Occurs when user leaves chat on his own
        """
        self.users.remove(user)
        Message.create_message_system(
            content="{} has left the party.".format(user.username),
            chat=self.chat,
        )
        PartyEvent.create_ui_party_update(
            party=self
        )

    def get_size_required(self):
        return self.monster.party_size

    def poll(self, user, character, status):
        access_code = self.access_code

        # cache this
        key = "{}_{}".format(str(access_code), str(user.id))
        cache.set(
            key, {
                "status": int(status),
                "character": character
            }, timeout=10
        )

        # check for everyone
        pattern = "{}_*".format(access_code)
        all_keys = cache.keys(pattern)
        print(all_keys)

        ready_characters = []
        all_characters = []
        for key in all_keys:
            items = cache.get(key)
            print(items)
            other_character = items["character"]
            if items["status"] == 1:
                ready_characters += [other_character]
            all_characters += [other_character]

        if len(ready_characters) >= self.get_size_required():
            all_ready = True
        else:
            all_ready = False

        return {
            'ready_characters': ready_characters,
            'all_characters': all_characters,
            'all_ready': all_ready,
        }


class PartyEvent(models.Model):

    datetime_created = models.DateTimeField(default=timezone.now)
    party = models.ForeignKey(Party, on_delete=models.CASCADE)
    party_event_type = models.IntegerField(choices=PartyEventType.choices())

    def to_dict(self):
        return {
            "datetime_created": self.datetime_created,
            "party_event_type": self.party_event_type,
            "party_id": self.party.id,
        }

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.send_to_firebase()

    def send_to_firebase(self):
        doc_ref = firestore_db.collection(
            u'events'
        ).document(
            u'party'
        ).collection(
            u'parties'
        ).document(u'{}'.format(self.id))

        doc_ref.set(
            self.to_dict()
        )

    @staticmethod
    def create_ui_party_update(party):
        """
        Creates and prompts client to update through sending party_event
        """
        party_event = PartyEvent(
            party=party,
            party_event_type=int(PartyEventType.UI_PARTY_UPDATE)
        )
        party_event.save()

    @staticmethod
    def create_ui_party_complete(party):
        """
        Creates and prompts client update that the party is complete
        """
        party_event = PartyEvent(
            party=party,
            party_event_type=int(PartyEventType.UI_PARTY_COMPLETE)
        )
        party_event.save()

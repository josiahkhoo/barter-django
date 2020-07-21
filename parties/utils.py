from enum import IntEnum


class PartyState(IntEnum):
    ONGOING = 0
    COMPLETED = 1

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


class PartyEventType(IntEnum):

    UI_PARTY_UPDATE = 0
    UI_PARTY_COMPLETE = 1

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]

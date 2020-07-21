from enum import IntEnum


class MessageType(IntEnum):

    MESSAGE_SYSTEM = 0
    MESSAGE_USER = 1

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]

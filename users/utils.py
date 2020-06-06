from enum import IntEnum


class UserStatus(IntEnum):
    UNVERIFIED = 0
    VERIFIED = 1
    DEACTIVATED = 2
    BANNED = 3

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


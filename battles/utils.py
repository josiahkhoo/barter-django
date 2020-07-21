from enum import IntEnum


class BattleState(IntEnum):
    ONGOING = 0
    COMPLETED = 1
    FORFEITED = 2

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]

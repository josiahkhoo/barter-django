from enum import IntEnum


class EquipmentType(IntEnum):
    HELMET = 0
    CHEST = 1
    SHIELD = 2
    WEAPON = 3

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


class EquipmentSet(IntEnum):
    CLOTH = 0
    STEEL = 1
    IRON = 2
    MAGIC = 3
    DARK = 4

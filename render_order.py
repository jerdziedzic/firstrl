from enum import auto, Enum # An enum is a set of values that will not change, auto assigns incrementing ints automatically


class RenderOrder(Enum):
    CORPSE = auto()
    ITEM = auto()
    ACTOR = auto()
from __future__ import annotations

from enum import Enum, IntEnum
from typing import NewType

import numpy as np

STARTING_POSITION = np.array([1] * 12 + [0] * 8 + [-1] * 12, dtype=np.int8)
SquareT = NewType("SquareT", int)


class Color(Enum):
    WHITE = -1
    BLACK = 1


class Entity(IntEnum):
    BLACK_KING = Color.BLACK.value * 10
    BLACK_MAN = Color.BLACK.value
    WHITE_KING = Color.WHITE.value * 10
    WHITE_MAN = Color.WHITE.value
    KING = 10
    MAN = 1
    EMPTY = 0


ENTITY_REPR = {
    Entity.BLACK_MAN: "b",
    Entity.WHITE_MAN: "w",
    Entity.EMPTY: ".",
    Entity.BLACK_KING: "B",
    Entity.WHITE_KING: "W",
}

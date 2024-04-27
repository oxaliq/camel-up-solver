

from dataclasses import dataclass
from enum import Enum
from typing import Union


class CamelColor(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3
    PURPLE = 4
    YELLOW = 5
    BLACK = 6
    WHITE = 7

class TicketColor(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3
    PURPLE = 4
    YELLOW = 5

class DiceColor(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3
    PURPLE = 4
    YELLOW = 5
    GRAY = 6

@dataclass
class Ticket:
    color: TicketColor
    first_place_value: int


@dataclass
class Camel:
    color: CamelColor
    position: Union[int, 'Camel']


@dataclass
class Board:
    tickets: list[Ticket]
    remaining_dice_colors: set


def init_board():
    camel_set = set(CamelColor)
    print(camel_set)


init_board()

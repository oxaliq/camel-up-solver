

from dataclasses import dataclass
from enum import Enum
from typing import Union


class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3
    PURPLE = 4
    YELLOW = 5


@dataclass
class Ticket:
    color: Color
    first_place_value: int

@dataclass
class Camel:
    color: Color
    position: Union[int, 'Camel']


@dataclass
class Board:
    tickets: list[Ticket]
    remaining_dice_colors: set



red_camel = Camel(color=Color.RED, position=4)
green_camel = Camel(color=Color.GREEN, position=red_camel)

from dataclasses import dataclass
from enum import Enum
from collections import defaultdict
from typing import Optional


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


class DiePrintColor(Enum):
    WHITE = 1
    BLACK = 2


@dataclass
class Move:
    pass


@dataclass
class DieRoll(Move):
    color: DiceColor
    value: int  # TODO: set range 1-3
    print_color: Optional[DiePrintColor]


@dataclass
class TicketTake(Move):
    color: TicketColor


@dataclass
class Ticket:
    color: TicketColor
    first_place_value: int


@dataclass
class Camel:
    color: CamelColor


@dataclass
class Board:
    tickets: defaultdict(list[Ticket])
    remaining_dice_colors: set
    track: list[list[Camel]]
    remaining_pyramid_tickets: int

    def __str__(self):
        for key in self.tickets:
            print(key)
            print(self.tickets[key])
        print()
        print(self.remaining_dice_colors)
        print()
        print(self.track)
        print()

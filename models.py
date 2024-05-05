from dataclasses import dataclass
from enum import Enum
from collections import defaultdict


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


@dataclass
class Board:
    tickets: defaultdict(list[Ticket])
    remaining_dice_colors: set
    track: list[list[Camel]]

    def __str__(self):
        for key in self.tickets:
            print(key)
            print(self.tickets[key])
        print()
        print(self.remaining_dice_colors)
        print()
        print(self.track)
        print()

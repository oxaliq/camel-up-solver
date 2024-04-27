import random
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
    camels_positions: defaultdict(list)

    def __str__(self):
        for key in self.tickets:
            print(key)
            print(self.tickets[key])
        print()
        print(self.remaining_dice_colors)
        print()
        print(self.camels_positions)
        print()

def single_die_roll():
    return random.randint(1, 3)

def init_board():
    camels_positions = defaultdict(list)
    camel_colors = set(TicketColor)
    while camel_colors:
        camel_color = camel_colors.pop()
        position = single_die_roll()
        camels_positions[position].append(Camel(color=camel_color))

    tickets=defaultdict(list[Ticket])
    for ticket_color in TicketColor:
        this_ticket_list = list()
        for first_place_value in [5,3,2,2]:
            this_ticket_list.append(Ticket(color=ticket_color, first_place_value=first_place_value))
        tickets[ticket_color] = this_ticket_list

    return Board(tickets, set(DiceColor), camels_positions)



board=init_board()
print(board)

def payout_given_roll(board, die_color, die_value, ticket_color):
    pass


def calculate_simple_payouts_for_choosing_red_ignoring_chaos(board):
    total_payout = 0
    remaining_dice_count = len(board.remaining_dice_colors)
    for die_color in board.remaining_dice_colors:
        for die_value in [1,2,3]:
            total_payout += payout_given_roll(board, die_color, die_value,
                                              ticket_color=TicketColor.RED)
    return total_payout / remaining_dice_count * 3

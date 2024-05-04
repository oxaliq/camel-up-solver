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
        for first_place_value in [2, 2, 3, 5]:
            this_ticket_list.append(Ticket(color=ticket_color, first_place_value=first_place_value))
        tickets[ticket_color] = this_ticket_list

    return Board(tickets, set(DiceColor), camels_positions)



board=init_board()


def get_camels_in_order(camel_positions):
    pass

def payout_given_roll(board, die_color, die_value, ticket_color):
    # move the cames
    camel_position=-1
    index_to_move=-1
    print(board.camels_positions)
    print("")
    for position, camels in board.camels_positions.items():
        for i, camel in enumerate (camels):
            if camel.color == die_color:
                camel_position=position
                index_to_move = i
                break
        if index_to_move >= 0:
            break

    camels_to_move=board.camels_positions[camel_position][index_to_move:]
    camels_to_keep=board.camels_positions[camel_position][:index_to_move]
    board.camels_positions[camel_position] = camels_to_keep
    board.camels_positions[camel_position+die_value].extend(camels_to_move)
    print(board.camels_positions)

    # calculate winnings
    total_winnings = 0
    winner_position = max(board.camels_positions.keys())
    camels_at_position = board.camels_positions[winner_position]
    if not camels_at_position:
        # still have to calculate second place winnings and later winnings
        return 0
    winner = camels_at_position[-1]
    if winner.color == ticket_color:
        # TODO handle case where there are no tickets left
        ticket_value = board.tickets[ticket_color][-1].first_place_value
        return ticket_value

def calculate_simple_payouts_for_choosing_red_ignoring_chaos(board):
    total_payout = 0
    remaining_dice_count = len(board.remaining_dice_colors)
    for die_color in board.remaining_dice_colors:
        for die_value in [1,2,3]:
            total_payout += payout_given_roll(board, die_color, die_value,
                                              ticket_color=TicketColor.RED)
    return total_payout / remaining_dice_count * 3

payout = payout_given_roll(board, DiceColor.RED, 3, TicketColor.RED)
print()
print(f"payout={payout}")

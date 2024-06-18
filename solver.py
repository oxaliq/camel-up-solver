import random
from collections import defaultdict
from itertools import chain
import copy
from models import TicketColor, Camel, Ticket, DiceColor, Board, Move
from typing import List


DIE_VALUES = [1, 2, 3]
FIRST_PLACE_TICKET_VALUES = [2, 2, 3, 5]
TRACK_LENGTH = 16
STARTING_PYRAMID_TICKET_COUNT = 5


def single_die_roll():
    return random.randint(1, 3)


def init_known_board(game_history: List[Move]):
    track = [[] for _ in range(TRACK_LENGTH)]
    camel_colors = set(TicketColor)
    tickets = defaultdict(list[Ticket])
    for ticket_color in TicketColor:
        this_ticket_list = list()
        for first_place_value in FIRST_PLACE_TICKET_VALUES:
            this_ticket_list.append(
                Ticket(color=ticket_color, first_place_value=first_place_value)
            )
        tickets[ticket_color] = this_ticket_list

    board = Board(
        tickets=tickets,
        remaining_dice_colors=set(DiceColor),
        track=track,
        remaining_pyramid_tickets=STARTING_PYRAMID_TICKET_COUNT,
    )

    # set initial camels at 0

    for move in game_history:
        match type(move).__name__:
            case "DieRoll":
                camel_color, die_value = move.print_color or move.color, move.value
                board = make_camel_move_with_pyramid_ticket(
                    board=board,
                    die_color=move.color,
                    camel_color=camel_color,
                    die_value=die_value,
                )
                pass
            case "TicketTake":
                board = take_betting_ticket_move(board=board, ticket_color=move.color)
            case _:
                raise Exception

    return board


def init_random_board():
    track = [[] for _ in range(TRACK_LENGTH)]

    camel_colors = set(TicketColor)
    while camel_colors:
        camel_color = camel_colors.pop()
        position = single_die_roll()
        track[position].append(Camel(color=camel_color))

    tickets = defaultdict(list[Ticket])
    for ticket_color in TicketColor:
        this_ticket_list = list()
        for first_place_value in FIRST_PLACE_TICKET_VALUES:
            this_ticket_list.append(
                Ticket(color=ticket_color, first_place_value=first_place_value)
            )
        tickets[ticket_color] = this_ticket_list

    return Board(
        tickets=tickets,
        remaining_dice_colors=set(DiceColor),
        track=track,
        remaining_pyramid_tickets=STARTING_PYRAMID_TICKET_COUNT,
    )


def copy_board(board):
    return copy.deepcopy(board)


def get_camels_in_order(board_track):
    return list(chain.from_iterable(board_track))


def make_camel_move_with_pyramid_ticket(board, camel_color, die_color, die_value):
    """

    :return: a copy of the board w/ the new state
    """
    new_board = copy_board(board)
    # move the camels
    camel_position = -1
    index_to_move = -1
    for position, camels in enumerate(new_board.track):
        for i, camel in enumerate(camels):
            if camel.color == camel_color:
                camel_position = position
                index_to_move = i
                break
        if index_to_move >= 0:
            break

    new_board.remaining_dice_colors.remove(die_color)
    new_board.remaining_pyramid_tickets -= 1

    # special case, if camel has not been placed on board yet
    if index_to_move == -1:
        new_board.track[index_to_move + die_value].append(Camel(color=camel_color))
        return new_board

    camels_to_move = new_board.track[camel_position][index_to_move:]
    camels_to_keep = new_board.track[camel_position][:index_to_move]
    new_board.track[camel_position] = camels_to_keep
    new_board.track[camel_position + die_value].extend(camels_to_move)
    return new_board


def take_betting_ticket_move(board, ticket_color):
    """
    take the top betting ticket for a given camel color

    :return: (new_board, ticket)
    """
    result_board = copy_board(board)
    ticket = result_board.tickets[ticket_color].pop()
    return (result_board, ticket)


def payout_given_roll(board, die_color, die_value, ticket_color):
    # TODO does not handle gray die
    camel_color = die_color
    new_board = make_camel_move_with_pyramid_ticket(
        board, camel_color, die_color, die_value
    )
    camels_in_order = get_camels_in_order(new_board.track)
    # print(camels_in_order)
    first_place = camels_in_order[-1]
    second_place = camels_in_order[-2]

    match ticket_color:
        case first_place.color:
            # TODO handle case where there are no tickets left
            ticket_value = new_board.tickets[ticket_color][-1].first_place_value
            return ticket_value
        case second_place.color:
            return 1
        case _:
            return -1


def calculate_simple_payouts_ignoring_chaos(board, chosen_ticket_color):
    total_payout = 0
    remaining_dice_count = len(board.remaining_dice_colors)
    for die_color in board.remaining_dice_colors:
        for die_value in DIE_VALUES:
            total_payout += payout_given_roll(
                board, die_color, die_value, ticket_color=chosen_ticket_color
            )
    return total_payout / remaining_dice_count * 3


board = init_random_board()
camels_in_order = get_camels_in_order(board.track)

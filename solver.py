import random
from collections import defaultdict
from itertools import chain
import copy
from models import TicketColor, Camel, Ticket, DiceColor, Board


DIE_VALUES = [1, 2, 3]
FIRST_PLACE_TICKET_VALUES = [2, 2, 3, 5]
TRACK_LENGTH = 16
STARTING_PYRAMID_TICKETS = 5


def single_die_roll():
    return random.randint(1, 3)


def init_board():
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
        remaining_pyramid_tickets=STARTING_PYRAMID_TICKETS,
    )


def get_camels_in_order(camel_positions):
    return list(chain.from_iterable(camel_positions))


def make_camel_move_with_pyramid_ticket(board, die_color, die_value):
    """

    :return: a copy of the board w/ the new state
    """
    track_copy = copy.deepcopy(board.track)
    # move the camels
    camel_position = -1
    index_to_move = -1
    for position, camels in enumerate(track_copy):
        for i, camel in enumerate(camels):
            if camel.color == die_color:
                camel_position = position
                index_to_move = i
                break
        if index_to_move >= 0:
            break

    camels_to_move = track_copy[camel_position][index_to_move:]
    camels_to_keep = track_copy[camel_position][:index_to_move]
    track_copy[camel_position] = camels_to_keep
    track_copy[camel_position + die_value].extend(camels_to_move)
    return Board(
        tickets=copy.deepcopy(board.tickets),
        remaining_dice_colors=board.remaining_dice_colors.copy(),
        track=track_copy,
        remaining_pyramid_tickets=board.remaining_pyramid_tickets - 1,
    )


def payout_given_roll(board, die_color, die_value, ticket_color):
    new_board = make_camel_move_with_pyramid_ticket(board, die_color, die_value)
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


board = init_board()
camels_in_order = get_camels_in_order(board.track)

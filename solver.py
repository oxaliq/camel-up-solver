import random
from collections import defaultdict
from itertools import chain

from models import TicketColor, Camel, Ticket, DiceColor, Board


def single_die_roll():
    return random.randint(1, 3)


def init_board():
    track = [[] for _ in range(16)]

    camel_colors = set(TicketColor)
    while camel_colors:
        camel_color = camel_colors.pop()
        position = single_die_roll()
        track[position].append(Camel(color=camel_color))

    tickets = defaultdict(list[Ticket])
    for ticket_color in TicketColor:
        this_ticket_list = list()
        for first_place_value in [2, 2, 3, 5]:
            this_ticket_list.append(
                Ticket(color=ticket_color, first_place_value=first_place_value)
            )
        tickets[ticket_color] = this_ticket_list

    return Board(tickets=tickets, remaining_dice_colors=set(DiceColor), track=track)


def get_camels_in_order(camel_positions):
    return list(chain.from_iterable(camel_positions))


def payout_given_roll(board, die_color, die_value, ticket_color):
    track_copy = board.track[:]
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

    camels_in_order = get_camels_in_order(track_copy)
    # print(camels_in_order)
    first_place = camels_in_order[-1]
    second_place = camels_in_order[-2]

    match ticket_color:
        case first_place.color:
            # TODO handle case where there are no tickets left
            ticket_value = board.tickets[ticket_color][-1].first_place_value
            return ticket_value
        case second_place.color:
            return 1
        case _:
            return -1


def calculate_simple_payouts_ignoring_chaos(board, chosen_ticket_color):
    total_payout = 0
    remaining_dice_count = len(board.remaining_dice_colors)
    for die_color in board.remaining_dice_colors:
        for die_value in [1, 2, 3]:
            total_payout += payout_given_roll(
                board, die_color, die_value, ticket_color=chosen_ticket_color
            )
    return total_payout / remaining_dice_count * 3


board = init_board()
camels_in_order = get_camels_in_order(board.track)
print(f"initial_board={camels_in_order}")

payout = payout_given_roll(board, DiceColor.RED, 3, TicketColor.RED)
print()
print(f"payout={payout}")
payout = calculate_simple_payouts_ignoring_chaos(board, TicketColor.RED)
print(f"red_payout={payout}")
payout = calculate_simple_payouts_ignoring_chaos(board, TicketColor.GREEN)
print(f"green_payout={payout}")
payout = calculate_simple_payouts_ignoring_chaos(board, TicketColor.BLUE)
print(f"blue_payout={payout}")
payout = calculate_simple_payouts_ignoring_chaos(board, TicketColor.YELLOW)
print(f"yellow_payout={payout}")

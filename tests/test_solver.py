from collections import defaultdict

from models import DiceColor, TicketColor, Board, Camel, CamelColor
from solver import init_board, take_betting_ticket_move, payout_given_roll
import pytest


def test_solver():
    total_payout = 0
    remaining_dice_colors = [DiceColor.RED, DiceColor.BLUE]
    remaining_dice_count = len(remaining_dice_colors)

    ticket_color = TicketColor.BLUE
    tickets = defaultdict(list)
    tickets[TicketColor.BLUE] = [2]
    track = [[] for _ in range(16)]
    track[0] = [Camel(color=CamelColor.BLUE), Camel(color=CamelColor.RED)]

    board = Board(
        tickets=tickets,
        remaining_dice_colors=remaining_dice_colors,
        track=track,
        remaining_pyramid_tickets=1,
    )

    for die_color in remaining_dice_colors:
        for die_value in [3]:
            total_payout += payout_given_roll(
                board, die_color, die_value, ticket_color=ticket_color
            )


def test_take_betting_ticket_move():
    board = init_board()

    test_cases = [[TicketColor.RED,5], [TicketColor.RED,3], [TicketColor.GREEN,5]]

    for test_case in test_cases:
        ticket_color = test_case[0]
        expected_value = test_case[1]

        board, result_ticket = take_betting_ticket_move(board, ticket_color)
        assert(result_ticket.first_place_value == expected_value)

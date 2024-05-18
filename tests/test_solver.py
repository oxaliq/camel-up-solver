from collections import defaultdict

from models import DiceColor, TicketColor, Board, Camel, CamelColor
from solver import payout_given_roll
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
        tickets=tickets, remaining_dice_colors=remaining_dice_colors, track=track
    )

    for die_color in remaining_dice_colors:
        for die_value in [3]:
            total_payout += payout_given_roll(
                board, die_color, die_value, ticket_color=ticket_color
            )

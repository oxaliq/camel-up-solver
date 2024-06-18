from collections import defaultdict

from models import DiceColor, TicketColor, Board, Camel, CamelColor, DieRoll
from solver import (
    init_random_board,
    take_betting_ticket_move,
    payout_given_roll,
    init_known_board,
    get_camels_in_order,
)


def test_solver():
    total_payout = 0
    remaining_dice_colors = [DiceColor.RED, DiceColor.BLUE]

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
    board = init_random_board()
    test_cases = [
        [TicketColor.RED, 5],
        [TicketColor.RED, 3],
        [TicketColor.RED, 2],
        [TicketColor.RED, 2],
        [TicketColor.GREEN, 5],
    ]
    for test_case in test_cases:
        ticket_color, expected_value = test_case
        board, result_ticket = take_betting_ticket_move(board, ticket_color)
        assert result_ticket.first_place_value == expected_value


def test_get_highest_probability_bet_from_known_board():
    game_history = [
        DieRoll(color=DiceColor.RED, value=3, print_color=None),
        DieRoll(color=DiceColor.YELLOW, value=1, print_color=None),
        DieRoll(color=DiceColor.GREEN, value=2, print_color=None),
        DieRoll(color=DiceColor.BLUE, value=2, print_color=None),
        DieRoll(color=DiceColor.PURPLE, value=2, print_color=None),
    ]
    board = init_known_board(game_history)
    camels = get_camels_in_order(board.track)
    print(camels)

    expected_camel_colors = [
        DiceColor.YELLOW,
        DiceColor.GREEN,
        DiceColor.BLUE,
        DiceColor.PURPLE,
        DiceColor.RED,
    ]
    for i, camel in enumerate(camels):
        assert camel.color == expected_camel_colors[i]

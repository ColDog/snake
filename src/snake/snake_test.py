import board
from .snake import move, _ideal_path


def test_weighted_mover():
    state = dict(
        id='1',
        snakes={
            '1': [(0, 2), (0, 1)],
            '2': [(4, 4), (4, 5)],
        },
        food=[(0, 3)],
        height=10,
        width=10,
        health=10,
        friendlies={'1': True, '2': False},
    )
    board.pretty_print(board.draw(**state))
    # Direction up because that's where the nearest food is.
    assert move(**state) == 'up'
    assert _ideal_path(**state) == [(0, 2), (0, 3)]


def test_weighted_move_around_snake():
    state = dict(
        id='1',
        snakes={
            '1': [(0, 2), (0, 1)],
            '2': [(1, 3), (0, 3)],
        },
        food=[(0, 9)],
        height=10,
        width=10,
        health=10,
        friendlies={'1': True, '2': False},
    )
    board.pretty_print(board.draw(**state))
    assert move(**state) == 'down'
    assert _ideal_path(**state)[:2] == [(0, 2), (0, 1)]

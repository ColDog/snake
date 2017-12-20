import grid
from .weighted import weighted_mover, _weights, _ideal_path, _pretty_print


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
    )
    _pretty_print(_weights(**state))
    grid.pretty_print(grid.draw(**state))
    # Direction up because that's where the nearest food is.
    assert weighted_mover(**state) == 'up'
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
    )
    _pretty_print(_weights(**state))
    grid.pretty_print(grid.draw(**state))
    # Direction up because that's where the nearest food is.
    assert weighted_mover(**state) == 'right'
    assert _ideal_path(**state) == [(0, 2), (1, 2)]

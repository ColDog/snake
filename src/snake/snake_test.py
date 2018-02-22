import board
import path
from .snake import move, _ideal_path, _play_forward, _weights, _safe_path


def test_move():
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


def test_move_around_snake():
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
    assert move(**state) == 'up'
    assert _ideal_path(**state)[:2] == [(0, 2), (0, 3)]


def test_forwarding():
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
    matrix = _weights(**state)
    head = state['snakes']['1'][0]
    target = (0, 9)
    route = path.walk(matrix, head, target)
    assert state == {
        'id': '1', 'snakes': {'1': [(0, 2), (0, 1)], '2': [(1, 3), (0, 3)]},
        'food': [(0, 9)], 'height': 10, 'width': 10}
    state = _play_forward(route, **state)
    assert state == {
        'id': '1', 'snakes': {'1': [(0, 9), (0, 2)], '2': [(1, 3), (0, 3)]},
        'food': [], 'height': 10, 'width': 10}
    head = state['snakes']['1'][0]
    tail = state['snakes']['1'][-1]
    assert _safe_path(head, tail, **state)

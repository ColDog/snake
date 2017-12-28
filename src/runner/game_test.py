import pytest

from .game import Game, Snake, MoveError
import path


def test_run_game():
    g = Game(
        width=10,
        height=10,
        snakes=[
            Snake(move=lambda **kwargs: path.MOVES.UP)
        ],
        food=[],
    )
    try:
        [s for s in g.run(5)]
    except MoveError:
        pass


def test_run_off_board_up():
    g = Game(
        width=10,
        height=10,
        snakes=[
            Snake(
                coords=[(0, 9)],
                move=lambda **kwargs: path.MOVES.UP,
            )
        ],
        food=[],
    )
    with pytest.raises(MoveError):
        next(iter(g.run()))


def test_run_off_board_down():
    g = Game(
        width=10,
        height=10,
        snakes=[
            Snake(
                coords=[(0, 0)],
                move=lambda **kwargs: path.MOVES.DOWN,
            )
        ],
        food=[],
    )
    with pytest.raises(MoveError):
        next(iter(g.run()))


def test_run_off_board_left():
    g = Game(
        width=10,
        height=10,
        snakes=[
            Snake(
                coords=[(0, 0)],
                move=lambda **kwargs: path.MOVES.LEFT,
            )
        ],
        food=[],
    )
    with pytest.raises(MoveError):
        next(iter(g.run()))


def test_run_off_board_right():
    g = Game(
        width=10,
        height=10,
        snakes=[
            Snake(
                coords=[(9, 0)],
                move=lambda **kwargs: path.MOVES.RIGHT,
            )
        ],
        food=[],
    )
    with pytest.raises(MoveError):
        next(iter(g.run()))


def test_eat_food():
    g = Game(
        width=10,
        height=10,
        snakes=[
            Snake(
                id='1',
                coords=[(0, 0)],
                move=lambda **kwargs: path.MOVES.UP,
            )
        ],
        food=[(0, 2)],
    )
    run = iter(g.run())
    state = next(run)
    assert state == {'id': '1', 'snakes': {'1': [(0, 1)]}, 'food': [(0, 2)],
                     'width': 10, 'height': 10, 'grow': False}
    state = next(run)
    assert state['snakes']['1'] == [(0, 2), (0, 1)]


def test_hit_snake():
    g = Game(
        width=10,
        height=10,
        snakes=[
            Snake(
                coords=[(0, 0)],
                move=lambda **kwargs: path.MOVES.RIGHT,
            ),
            Snake(
                coords=[(1, 1)],  # Will hit (1, 0).
                move=lambda **kwargs: path.MOVES.DOWN,
            ),
        ],
        food=[(0, 2)],
    )
    run = iter(g.run())  # Move snake 1 into pos.
    next(run)
    with pytest.raises(MoveError):
        next(run)  # Snake 2 hits snake 1.

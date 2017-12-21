import math

from .path import (
    matrix,
    default_cost_fn,
    pretty_print,
    cost,
    walk,
    direction,
)


def test_matrix():
    grid = matrix(
        10, 10, (0, 0), cost_fn=default_cost_fn)
    pretty_print(grid)


def test_cost():
    m = matrix(10, 10, (0, 0))
    assert cost(m, (0, 0), (0, 1)) == 1


def test_shortest_path():
    m = matrix(10, 10, (0, 0))
    assert walk(m, (0, 0), (0, 1)) == [(0, 0), (0, 1)]


def test_direction():
    d = direction((0, 0), (0, 1))
    assert d == "up"
    d = direction((0, 1), (0, 0))
    assert d == "down"
    d = direction((0, 0), (1, 0))
    assert d == "right"
    d = direction((1, 0), (0, 0))
    assert d == "left"


def test_matrix_cost():
    def cost_fn(cur, target):
        if target in [(4, 5), (4, 6), (4, 7), (4, 8)]:
            return math.inf
        return 1
    m = matrix(10, 10, (0, 0), cost_fn=cost_fn)
    pretty_print(m)

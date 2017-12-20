import math

import path
import grid
from .random import random_mover


def weighted_mover(id=None, snakes=None, food=None, height=None, width=None):
    head = snakes[id][0]
    matrix = _weights(id, snakes, food, height, width)
    targets = food

    target = None
    target_cost = math.inf
    for t in targets:
        cost = path.cost(matrix, head, t)
        if cost < target_cost:
            target_cost = cost
            target = t

    if target_cost == math.inf:
        return random_mover()

    route = path.walk(matrix, head, target)
    return path.direction(head, route[1])


def _weights(id=None, snakes=None, food=None, height=None, width=None):
    g = grid.draw(id=id, snakes=snakes, food=food, height=height, width=width)
    head = snakes[id][0]

    matrix = path.matrix(
        height=height,
        width=width,
        initial=head,
        cost_fn=_cost(g),
    )
    return matrix


def _cost(g):
    def cost_fn(current, candidate):
        x, y = candidate
        if g[x][y].type == grid.TYPES.EMPTY:
            return 2
        elif g[x][y].type == grid.TYPES.SNAKE:
            return math.inf
        elif g[x][y].type == grid.TYPES.FOOD:
            return 1
        else:
            raise Exception("Unknown board token")
    return cost_fn

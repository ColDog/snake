import math
import random

import path
import grid


def weighted_mover(id=None, snakes=None, food=None, height=None, width=None):
    route = _ideal_path(id, snakes, food, height, width)
    head = snakes[id][0]
    if route is None:
        return 'left'
    return path.direction(head, route[1])


def _ideal_path(id=None, snakes=None, food=None, height=None, width=None):
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
        return _safe_local(matrix, head)

    route = path.walk(matrix, head, target)
    return route


def _safe_local(matrix, head):
    x, y = head
    targets = [(x, y+1), (x+1, y), (x, y-1), (x-1, y)]
    random.shuffle(targets)

    for target in targets:
        if path.cost(matrix, head, target) <= 1:
            return [head, target]
    return None


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
        if g[y][x].type == grid.TYPES.EMPTY:
            return 1
        elif g[y][x].type == grid.TYPES.SNAKE:
            return math.inf
        elif g[y][x].type == grid.TYPES.FOOD:
            return 0
        else:
            raise Exception("Unknown board token")
    return cost_fn

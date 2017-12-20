import math

from .moves import MOVES


def default_cost_fn(*args):
    """ Default cost fn is the default useful for a graph. """
    return 1


def matrix(height, width, initial, cost_fn=None):
    """
    Matrix builds up a matrix from the initial node showing the cost to reach
    every node in the graph in an optimial path. This can be inspected by using
    the walk function.
    """
    if cost_fn is None:
        cost_fn = default_cost_fn

    grid = [[(None, math.inf)] * width for _ in range(height)]
    grid[initial[1]][initial[0]] = (None, 0)

    visited = set()

    cur = initial
    visited.add(cur)

    while True:
        nxt = None
        nxt_cost = math.inf
        cur_cost = grid[cur[1]][cur[0]][1]

        for n in _neighbours(cur, height, width):
            if n in visited:
                continue
            cost = grid[n[1]][n[0]][1]
            est_cost = cur_cost + cost_fn(cur, n)
            if cost > est_cost:
                cost = est_cost
                grid[n[1]][n[0]] = (cur, cost)
            if cost < nxt_cost:
                nxt = n
                nxt_cost = cost

        if nxt_cost == math.inf:
            return grid
        if nxt in visited:
            return grid

        cur = nxt
        visited.add(cur)


def walk(grid, initial, target):
    """
    Walk the matrix provided by the matrix function. This will return the
    optimal path and the cost of this path from initial to target.
    """
    prev, cost = grid[target[1]][target[0]]
    stack = [target, prev]

    while prev != initial:
        prev = grid[prev[1]][prev[0]][0]
        stack.append(prev)
    stack.reverse()
    return stack


def cost(grid, initial, target):
    """
    Cost provides the cost from initial to target.
    """
    if target[1] >= len(grid):
        return math.inf
    if target[0] >= len(grid[target[1]]):
        return math.inf
    _, cost = grid[target[1]][target[0]]
    return cost


def direction(initial, target):
    x1, y1 = initial
    x2, y2 = target
    if x1 == x2:
        return MOVES.UP if y2 > y1 else MOVES.DOWN
    elif y1 == y2:
        return MOVES.LEFT if x1 > x2 else MOVES.RIGHT


def _neighbours(current, height, width):
    x, y = current

    neighbours = []
    if y + 1 < height:
        neighbours.append((x, y+1))
    if y - 1 >= 0:
        neighbours.append((x, y-1))
    if x + 1 < width:
        neighbours.append((x+1, y))
    if x - 1 >= 0:
        neighbours.append((x-1, y))

    return neighbours

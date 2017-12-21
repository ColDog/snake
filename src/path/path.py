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

    # Grid is a 2d array with (prev, cost). It is indexed as grid[y][x] to be
    # more like a traditional graph.
    grid = [[(None, math.inf)] * width for _ in range(height)]
    grid[initial[1]][initial[0]] = (None, 0)

    # Unvisited is the tracking set of unvisited elements in the graph.
    unvisited = set([v for v in _each_vertex(width, height)])

    # Set the initial cost to 0.
    grid[initial[1]][initial[0]] = (None, 0)

    while len(unvisited) > 0:
        # Select the minimum value from the unvisited set.
        cur = next(iter(unvisited))
        cur_cost = grid[cur[1]][cur[0]][1]
        for x, y in unvisited:
            if grid[y][x][1] < cur_cost:
                cur = (x, y)
                cur_cost = grid[y][x][1]
        unvisited.remove(cur)

        # For all neighbours in the graph from the current vertex.
        for n in _neighbours(cur, height, width):
            # Calculate an alternate cost and compare this to the current cost
            # of this neighbour.
            alt = cur_cost + cost_fn(cur, n)
            if alt < grid[n[1]][n[0]][1]:
                grid[n[1]][n[0]] = (cur, alt)
    return grid


def walk(grid, initial, target):
    """
    Walk the matrix provided by the matrix function. This will return the
    optimal path and the cost of this path from initial to target.
    """
    prev, cost = grid[target[1]][target[0]]
    stack = [target, prev]

    while prev != initial:
        if prev is None:
            return None
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


def _each_vertex(width, height):
    for x in range(width):
        for y in range(height):
            yield (x, y)


def pretty_print(grid, cur=None):
    rev = list(grid)
    rev.reverse()
    print('')
    for row in rev:
        for col in row:
            tok = str(col[1])
            if tok == 'inf':
                tok = '∞'
            tok = _pad(tok, 2)

            print('|' + tok, end='')
        print('|')


def _pad(s, n):
    if len(s) < n:
        s += ' ' * (n - len(s))
    return s

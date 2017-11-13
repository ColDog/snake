import math


def default_cost_fn(*args):
    return 1


def matrix(height, width, initial, cost_fn=None):
    if cost_fn is None:
        cost_fn = default_cost_fn

    grid = [[(None, math.inf)] * width for _ in range(height)]
    grid[initial[0]][initial[1]] = (None, 0)

    visited = []

    cur = initial
    visited.append(cur)

    while True:
        nxt = None
        nxt_cost = math.inf
        cur_cost = grid[cur[0]][cur[1]][1]

        for n in _neighbours(cur, height, width):
            if n in visited:
                continue
            cost = grid[n[0]][n[1]][1]
            est_cost = cur_cost + cost_fn(cur, n)
            if cost > est_cost:
                cost = est_cost
                grid[n[0]][n[1]] = (cur, cost)
            if cost < nxt_cost:
                nxt = n
                nxt_cost = cost

        if nxt_cost == math.inf:
            return grid
        if nxt in visited:
            return grid

        cur = nxt
        visited.append(cur)


def walk(grid, initial, target):
    prev, cost = grid[target[0]][target[1]]
    stack = [target, prev]

    while prev != initial:
        prev = grid[prev[0]][prev[1]][0]
        stack.append(prev)
    stack.reverse()
    return stack, cost


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

import math
import random
import path
import grid


def weighted_mover(id=None, snakes=None, food=None, height=None, width=None):
    route = _ideal_path(id, snakes, food, height, width)
    head = snakes[id][0]
    if route is None:
        return 'left'
    move = path.direction(head, route[1])
    print('->', move)
    return move


def _ideal_path(id=None, snakes=None, food=None, height=None, width=None):
    head = snakes[id][0]
    tail = snakes[id][-1]
    matrix = _weights(id, snakes, food, height, width)
    targets = food  # + [tail]

    path.pretty_print(matrix, current=head)

    target = None
    target_cost = math.inf
    for t in targets:
        cost = path.cost(matrix, head, t)
        print('cost', t, cost)
        if cost < target_cost:
            target_cost = cost
            target = t

    if target_cost == math.inf:
        return _lowest_local(matrix, head)

    if target_cost == math.inf:
        return _safe_local(matrix, head)

    route = path.walk(matrix, head, target)
    return route


def _lowest_local(matrix, head):
    width, height = path.size(matrix)
    target = None
    target_cost = math.inf
    for (nx, ny) in path.neighbours(head, height, width):
        cost = path.cost(matrix, head, (nx, ny))
        if cost < target_cost:
            target_cost = cost
            target = (nx, ny)
    return [head, target]


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
        cost_fn=_cost(g, id),
    )
    return matrix


def _cost(g, self_id):
    w, h = path.size(g)

    def cost_fn(current, candidate):
        x, y = candidate
        if g[y][x].type == grid.TYPES.EMPTY or g[y][x].tail:
            cost = 2
            if path.at_edge(g, (x, y)):
                cost += 10
            for (nx, ny) in path.neighbours(candidate, h, w):
                n = g[ny][nx]
                if n.id != self_id and n.type == grid.TYPES.SNAKE:
                    return math.inf
                for (n2x, n2y) in path.neighbours((nx, ny), h, w):
                    n = g[n2y][n2x]
                    if n.id != self_id and n.type == grid.TYPES.SNAKE:
                        cost += 20
                    for (n3x, n3y) in path.neighbours((n2x, n2y), h, w):
                        n = g[n3y][n3x]
                        if n.id != self_id and n.type == grid.TYPES.SNAKE:
                            cost += 10
            return cost
        elif g[y][x].type == grid.TYPES.SNAKE:
            return math.inf
        elif g[y][x].type == grid.TYPES.FOOD:
            if y == h-1 or x == w-1:
                return 2
            return 1
        else:
            raise Exception("Unknown board token")
    return cost_fn

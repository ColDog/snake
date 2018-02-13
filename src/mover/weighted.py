import math
import random
import path
import grid


def weighted_mover(id=None, snakes=None, food=None, height=None, width=None,
                   health=None):
    route = _ideal_path(id, snakes, food, height, width, health)
    head = snakes[id][0]
    if route is None or route[1] is None:
        print('->', 'FAILED')
        return path.MOVES.UP
    move = path.direction(head, route[1])
    print('->', move)
    return move


def _ideal_path(id=None, snakes=None, food=None, height=None, width=None,
                health=None):
    head = snakes[id][0]
    tail = snakes[id][-1]
    matrix = _weights(id, snakes, food, height, width)

    path.pretty_print(matrix, current=head)

    target_tiers = []

    smallest = _smallest_snake(id, snakes, smaller_than=len(snakes[id]))

    # If needs to eat.
    if health < min((width, height)) * 2 or smallest is None:
        target_tiers.append(('food', food))

    # Found a snake we could eat.
    if smallest is not None:
        s = snakes[smallest]
        next_head = path.moved_position(s[0], path.direction(s[0], s[1]))
        target_tiers.append(('attack', [next_head]))

    # Add the tail to the tier always.
    target_tiers.append(('tail', [tail]))
    target_tiers.append(('corners', path.corners(height, width)))

    target = None
    target_cost = math.inf
    for name, tier in target_tiers:
        for t in tier:
            cost = path.cost(matrix, head, t)
            if cost < target_cost:
                target_cost = cost
                target = t
        if target_cost != math.inf and target_cost != 0:
            print('tier success', name, target_cost)
            break
        print('tier failed', name, target_cost)

    if target_cost == math.inf:
        print('safe local')
        return _safe_local(
            id=id,
            snakes=snakes,
            food=food,
            height=height,
            width=width,
        )
    route = path.walk(matrix, head, target)
    return route


def _safe_local(id=None, snakes=None, food=None, height=None, width=None):
    head = snakes[id][0]
    g = grid.draw(id=id, snakes=snakes, food=food, height=height, width=width)
    w, h = path.size(g)
    for (x, y) in path.neighbours(head, h, w):
        if g[y][x].type == grid.TYPES.EMPTY or g[y][x].type == grid.TYPES.FOOD:
            return [head, (x, y)]
    return None


def _weights(id=None, snakes=None, food=None, height=None, width=None):
    g = grid.draw(id=id, snakes=snakes, food=food, height=height, width=width)
    head = snakes[id][0]

    matrix = path.matrix(
        height=height,
        width=width,
        initial=head,
        cost_fn=_cost(g, id),
        poss_fn=_possibilities(g),
    )
    return matrix


def _cost(g, self_id):
    w, h = path.size(g)

    def cost_fn(current, candidate):
        x, y = candidate
        if g[y][x].type == grid.TYPES.SNAKE and not g[y][x].tail:
            return math.inf
        cost = 1
        if path.at_edge(g, (x, y)):
            cost += 100
        for (nx, ny) in path.neighbours(candidate, h, w):
            n = g[ny][nx]
            if n.id != self_id and n.type == grid.TYPES.SNAKE:
                cost += 300
        return cost
    return cost_fn


def _possibilities(g):
    w, h = path.size(g)

    def update_fn(target, cost):
        x, y = target
        if cost == math.inf:
            return cost
        impossible_neighbours = 0
        for (nx, ny) in path.neighbours_with_off_board((x, y), h, w):
            if (path.off_board(g, (nx, ny)) or
               g[ny][nx].type == grid.TYPES.SNAKE):

                impossible_neighbours += 1
        if impossible_neighbours >= 3:
            print('impossible', (x, y))
            return math.inf
        return cost
    return update_fn


def _smallest_snake(self_id, snakes, smaller_than=math.inf):
    smallest = None
    smallest_size = math.inf
    for (sid, snake) in snakes.items():
        if sid != self_id and len(snake) < smallest_size and \
           (len(snake) < smaller_than):
            smallest_size = len(snake)
            smallest = sid
    return smallest

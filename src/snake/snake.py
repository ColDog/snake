import math
import path
import board
import copy


class BEHAVIOURS:
    eat_only_when_hungy = False


def move(id=None, snakes=None, food=None, height=None, width=None,
         health=None, friendlies=None):
    route = _ideal_path(id, snakes, food, height, width, health, friendlies)
    head = snakes[id][0]
    if route is None or route[1] is None:
        print('->', 'FAILED')
        return path.MOVES.UP
    move = path.direction(head, route[1])
    print('->', move)
    return move


def _ideal_path(id=None, snakes=None, food=None, height=None, width=None,
                health=None, friendlies=None):
    head = snakes[id][0]
    tail = snakes[id][-1]
    size = len(snakes[id])
    matrix = _weights(id, snakes, food, height, width)

    target_tiers = []

    # Retrieves smallest non friendly snake.
    smallest, smallest_size = _smallest_snake(id, snakes, friendlies)

    # Eat if hungry.
    if health < min((width, height)) * 2:
        target_tiers.append(('food', food))

    # Found a snake we could eat that is smaller than ourselves.
    if smallest is not None and smallest_size < size:
        s = snakes[smallest]
        next_head = path.moved_position(s[0], path.direction(s[1], s[0]))
        if next_head == head:
            next_head = s[0]
        target_tiers.append(('attack', [next_head]))

    # Always add food at this level.
    target_tiers.append(('food', food))

    # Add the tail to the tier always.
    target_tiers.append(('tail', [tail]))

    # Add all corners on the board.
    target_tiers.append(('corners', path.corners(height, width)))

    target = None
    target_cost = math.inf
    for name, tier in target_tiers:
        for t in tier:
            cost = path.cost(matrix, head, t)
            if cost < target_cost:
                route = path.walk(matrix, head, t)
                if route:
                    forward_state = _play_forward(
                        route, id=id, snakes=copy.deepcopy(snakes),
                        food=food[:], height=height, width=width,
                    )
                    forward_head = forward_state['snakes'][id][0]
                    forward_tail = forward_state['snakes'][id][-1]
                    if _safe_path(forward_head, forward_tail, **forward_state):
                        target_cost = cost
                        target = t
                    else:
                        print('tier no safe path to tail', name, t)
        if target_cost != math.inf:
            print('tier success', name, target_cost)
            break
        print('tier failed', name, target_cost, tier)

    # Go for the lowest local cost.
    if target_cost == math.inf:
        print('local lowest')
        for t in path.neighbours(head, width, height):
            cost = path.cost(matrix, head, t)
            if cost < target_cost:
                target_cost = cost
                target = t

    # Go for a safe local square.
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
    g = board.draw(id=id, snakes=snakes, food=food, height=height, width=width)
    w, h = path.size(g)
    for (x, y) in path.neighbours(head, h, w):
        if g[y][x].type == board.TYPES.SNAKE:
            continue
        return [head, (x, y)]
    return None


def _weights(id=None, snakes=None, food=None, height=None, width=None):
    g = board.draw(id=id, snakes=snakes, food=food, height=height, width=width)
    head = snakes[id][0]

    matrix = path.matrix(
        height=height,
        width=width,
        initial=head,
        cost_fn=_cost(g, snakes, id),
    )
    return matrix


def _cost(g, snakes, self_id):
    """
    Returns a cost function with the following attributes:
    * If the square has only 1 exit between snakes and walls, it is an infinite
      cost.
    * If the square contains a snake it is an infinite square, unless it is a
      snakes tail and that snake can not eat in the next turn.
    * If the square is within range of a snake that is larger than itself.
    """
    w, h = path.size(g)
    self_size = len(snakes[self_id])

    def cost_fn(current, candidate):
        x, y = candidate
        n = g[y][x]
        if n.type == board.TYPES.SNAKE:
            if not n.tail:
                return math.inf
            if n.tail and _about_to_eat(g, snakes[n.id][0]) and \
               n.id != self_id:
                return math.inf
        cost = 1
        for (nx, ny) in path.neighbours(candidate, h, w):
            n = g[ny][nx]
            if n.head and n.size >= self_size and n.id != self_id:
                return math.inf
        return cost
    return cost_fn


def _smallest_snake(self_id, snakes, friendlies=None):
    smallest = None
    smallest_size = math.inf
    for (sid, snake) in snakes.items():
        if (sid != self_id and not friendlies[sid]
           and len(snake) < smallest_size):
            smallest_size = len(snake)
            smallest = sid
    return smallest, smallest_size


def _about_to_eat(g, head):
    w, h = path.size(g)
    for (nx, ny) in path.neighbours(head, h, w):
        if g[ny][nx].type == board.TYPES.FOOD:
            return True
    return False


def _play_forward(route, **state):
    id = state['id']
    snakes = state['snakes']
    food = state['food']
    snake = snakes[id]
    for move in route:
        if move in food:
            food.remove(move)
            snakes[id] = [move] + snake
        else:
            snakes[id] = [move] + snake[:-1]
    state['id'] = id
    state['snakes'] = snakes
    state['food'] = food
    return state


def _safe_path(initial, target, **state):
    matrix = _weights(**state)
    return path.cost(matrix, initial, target) != math.inf

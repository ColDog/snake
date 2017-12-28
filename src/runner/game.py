import random
import math

import path


class MoveError(Exception):
    def __init__(self, state, move):
        self.state = state
        self.move = move
        self.snake_id = state['id']

    def __str__(self):
        return '{}: {} to {} -- state={}'.format(
            self.__class__.__name__, self.state['id'],
            self.move,
            self.state,
        )


class HitSelfError(MoveError):
    pass


class HitSnakeError(MoveError):
    pass


class OffBoardError(MoveError):
    pass


class InvalidMoveError(MoveError):
    pass


class GameError(Exception):
    pass


class Snake:

    def __init__(self, id=None, coords=None, move=None):
        self.id = id
        self.coords = coords or []
        self.move = move


class Game:

    def __init__(self, width, height, snakes, food):
        self.id = None
        self.width = width
        self.height = height
        self.snakes = snakes
        self.food = food
        self.turns = 0

        self._initialize_snakes()
        self._initialize_food()

    def _game_state(self, snake=None, grow=None):
        out = {
            'snakes': {
                snake.id: list(snake.coords) for snake in self.snakes
            },
            'food': list(self.food),
            'width': self.width,
            'height': self.height,
        }
        if snake:
            out['id'] = snake.id
        if grow is not None:
            out['grow'] = grow
        return out

    def _move(self, snake):
        state = self._game_state(snake)
        move = snake.move(**state)

        head = snake.coords[0]
        if move == path.MOVES.UP:
            head = (head[0], head[1] + 1)
        elif move == path.MOVES.LEFT:
            head = (head[0] - 1, head[1])
        elif move == path.MOVES.RIGHT:
            head = (head[0] + 1, head[1])
        elif move == path.MOVES.DOWN:
            head = (head[0], head[1] - 1)
        else:
            raise InvalidMoveError(state, move)

        if (head[0] >= self.width or
           head[0] < 0 or
           head[1] >= self.height or
           head[1] < 0):
            raise OffBoardError(state, move)

        for other_snake in self.snakes:
            for coord in other_snake.coords:
                if coord == head:
                    if other_snake.id == snake.id:
                        raise HitSelfError(state, move)
                    else:
                        raise HitSnakeError(state, move)

        grow = False
        for idx, food in enumerate(self.food):
            if food == head:
                grow = True
                self.food.pop(idx)
                break

        if grow:
            self._initialize_food()

        if not grow:
            snake.coords.pop(-1)
        snake.coords.insert(0, head)
        return self._game_state(snake, grow)

    def _initialize_snakes(self):
        if self.snakes is None:
            raise GameError('No snakes provided')
        for idx, snake in enumerate(self.snakes):
            if not snake.id:
                snake.id = str(idx + 1)
            if len(snake.coords) > 0:
                continue
            x = random.randint(0, self.width-4)
            y = random.randint(0, self.height-4)
            snake.coords = [(x, y), (x, y + 1)]

    def _initialize_food(self):
        if self.food is None or len(self.food) > 0:
            return
        self.food = [
            (random.randint(0, self.width-1), random.randint(0, self.height-1)),
            (random.randint(0, self.width-1), random.randint(0, self.height-1))
        ]

    def run(self, turns=math.inf):
        while self.turns < turns:
            self.turns += 1
            for snake in self.snakes:
                yield self._move(snake)

    def turn(self, snake_id, move_func):
        state = None
        for snake in self.snakes:
            if snake.id == snake_id:
                snake.move = move_func
            state = self._move(snake)
        return state

    def state(self):
        return self._game_state()

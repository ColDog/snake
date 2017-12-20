import random
import math

import path


class MoveError(Exception):
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

    def _game_state(self, snake):
        return {
            'id': snake.id,
            'snakes': {
                snake.id: list(snake.coords) for snake in self.snakes
            },
            'food': list(self.food),
            'width': self.width,
            'height': self.height,
        }

    def _move(self, snake):
        move = snake.move(**self._game_state(snake))

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
            raise MoveError('Invalid move: {}'.format(move))

        if head[0] >= self.width:
            raise MoveError('Off board: {}'.format(head))
        if head[0] < 0:
            raise MoveError('Off board: {}'.format(head))
        if head[1] >= self.height:
            raise MoveError('Off board: {}'.format(head))
        if head[1] < 0:
            raise MoveError('Off board: {}'.format(head))

        for other_snake in self.snakes:
            for coord in other_snake.coords:
                if coord == head:
                    if other_snake.id == snake.id:
                        raise MoveError('Hit self at {}'.format(head))
                    else:
                        raise MoveError(
                            'Hit snake {} at {}'.format(other_snake.id, head)
                        )

        grow = False
        for idx, food in enumerate(self.food):
            if food == head:
                grow = True
                self.food.pop(idx)
                break

        if not grow:
            snake.coords.pop(-1)
        snake.coords.insert(0, head)
        return self._game_state(snake)

    def _initialize_snakes(self):
        if self.snakes is None:
            raise GameError('No snakes provided')
        for idx, snake in enumerate(self.snakes):
            if not snake.id:
                snake.id = str(idx + 1)
            if len(snake.coords) > 0:
                continue
            x = random.randint(0, self.width-1)
            y = random.randint(0, self.height-1)
            snake.coords = [(x, y), (x, y + 1)]

    def _initialize_food(self):
        if self.food is None or len(self.food) > 0:
            return
        self.food = [(
            random.randint(0, self.width-1),
            random.randint(0, self.height-1)
        )]

    def run(self, turns=math.inf):
        while self.turns < turns:
            self.turns += 1
            for snake in self.snakes:
                yield self._move(snake)

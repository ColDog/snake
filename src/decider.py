import random
import math

import path
import game


class Decider:
    UP = 'up'
    DOWN = 'down'
    LEFT = 'left'
    RIGHT = 'right'

    def __init__(self, game):
        self.game = game

    def decide(self):
        raise NotImplemented("Decide not implemented")


class RandomDecider(Decider):
    choices = [
        Decider.UP,
        Decider.DOWN,
        Decider.LEFT,
        Decider.RIGHT,
    ]

    def decide(self):
        return random.choice(self.choices)


class WeightedDecider(Decider):

    def _cost(self, current, candidate):
        x, y = candidate
        if self.game.grid[x][y].type == game.EMPTY:
            return 1
        elif self.game.grid[x][y].type == game.SNAKE:
            return math.inf
        elif self.game.grid[x][y].type == game.FOOD:
            return 1
        else:
            raise Exception("Unknown board token")

    def decide(self):
        grid = path.weights(
            height=self.game.height,
            width=self.game.width,
            initial=self.game.me.head,
            cost_fn=self._cost,
        )

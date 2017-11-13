import random
import math

import path
import game


class Decider:

    def __init__(self, game):
        self.game = game

    def decide(self):
        raise NotImplemented("Decide not implemented")


class RandomDecider(Decider):
    choices = [
        path.UP,
        path.DOWN,
        path.LEFT,
        path.RIGHT,
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

    def _targets(self):
        """ Retrieve a list of all targets as (x,y) """
        return self.game.food

    def decide(self):
        matrix = path.matrix(
            height=self.game.height,
            width=self.game.width,
            initial=self.game.head,
            cost_fn=self._cost,
        )
        targets = self._targets()

        target = None
        target_cost = math.inf
        for t in targets:
            cost = path.cost(matrix, self.game.head, t)
            print('cost', self.game.head, t, cost)
            if cost < target_cost:
                target_cost = cost
                target = t

        if target_cost == math.inf:
            print('matrix', matrix)
            return RandomDecider(self.game).decide()

        route = path.walk(matrix, self.game.head, target)
        print('route', self.game.head, route[1], target_cost)
        return path.direction(self.game.head, route[1])

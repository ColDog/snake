import gym
import runner
import mover
import grid

from gym.envs.registration import register
import numpy as np


class SnakeGame(gym.Env):
    MAPPINGS = {
        0: 'left',
        1: 'up',
        2: 'right',
        3: 'down',
    }
    RANGE = 4
    BOARD = 10 * 10  # 10 x 10 board.

    def __init__(self):
        self.game = None
        self.snake_id = None

    def _step(self, action):
        assert action in self.MAPPINGS

        reward = 1
        done = False
        error = None
        try:
            out = self.game.turn(
                self.snake_id,
                move_func=lambda *args, **kwargs: self.MAPPINGS[action],
            )
            # grid.pretty_print(grid.draw(**out))
            if out['grow']:
                reward = 2
        except Exception as e:
            if e.snake_id != self.snake_id:
                reward = 4
            reward = 0
            done = True
            error = e
        return self._state(), reward, done, {"error": error}

    def _reset(self):
        self.game = runner.Game(
            width=10,
            height=10,
            snakes=[
                runner.Snake(move=mover.MOVERS['weighted']),
                runner.Snake(move=mover.MOVERS['weighted']),
            ],
            food=[(0, 2), (0, 3)],
        )
        self.snake_id = self.game.snakes[0].id
        return self._state()

    def _state(self):
        board = grid.draw(**self.game.state())
        state = np.array([item.type for sublist in board for item in sublist])
        return state


register(
    id='SnakeGame-v0',
    entry_point='snake_env:SnakeGame',
)

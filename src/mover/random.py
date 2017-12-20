import random

import path


def random_mover(id=None, snakes=None, food=None, height=None, width=None):
    choices = [
        path.MOVES.UP,
        path.MOVES.DOWN,
        path.MOVES.LEFT,
        path.MOVES.RIGHT,
    ]
    return random.choice(choices)

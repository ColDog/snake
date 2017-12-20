"""
Mover implements mover functions that represent different algorithms applied to
the snake game. The mover functions have the following signature:

An example state passed in would look like:

mover(
    id=1',
    snakes={'1': [(0, 2), (0, 1)]},
    food=[(0, 1)],
    height=10,
    width=20,
)
"""

from .random import random_mover
from .weighted import weighted_mover

__all__ = ['random_mover', 'weighted_mover']

MOVERS = {
    'random': random_mover,
    'weighted': weighted_mover,
}

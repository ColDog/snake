import time

import runner
import mover
import grid

desc = runner.Game(
    width=10,
    height=10,
    snakes=[
        runner.Snake(move=mover.MOVERS['weighted']),
        runner.Snake(move=mover.MOVERS['weighted']),
    ],
    food=[(0, 2), (0, 3)],
)

for state in desc.run():
    print(state)
    grid.pretty_print(grid.draw(**state))
    time.sleep(1)

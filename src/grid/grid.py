
class TYPES:
    SNAKE = 'snake'
    FOOD = 'food'
    EMPTY = 'empty'


class BoardToken:

    def __init__(self, token_type, token_id=None):
        self.type = token_type
        self.id = token_id

    def data(self):
        return "{}({})".format(self.type, self.id or '')


def draw(id=None, snakes=None, food=None, width=None, height=None):
    """
    Takes a game state input and returns a board with the tokens at each
    position.
    """
    grid = [
        [BoardToken(TYPES.EMPTY) for _ in range(width)]
        for _ in range(height)
    ]

    for coord in food:
        x, y = coord
        grid[y][x] = BoardToken(TYPES.FOOD)

    for id, coords in snakes.items():
        for coord in coords:
            x, y = coord
            grid[y][x] = BoardToken(TYPES.SNAKE, id)

    return grid


def pretty_print(grid):
    rev = list(grid)
    rev.reverse()
    for row in rev:
        for col in row:
            tok = '_'
            if col.type == TYPES.SNAKE:
                tok = col.id
            elif col.type == TYPES.FOOD:
                tok = 'x'
            print('|' + tok, end='')
        print('|')

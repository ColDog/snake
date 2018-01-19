
class TYPES:
    EMPTY = 0
    FOOD = 1
    SNAKE = 2


class BoardToken:

    def __init__(self, token_type, token_id=None, token_head=False):
        self.type = token_type
        self.id = token_id
        self.head = token_head

    def data(self):
        return "{}({})".format(self.type, self.id or '')


def draw(id=None, snakes=None, food=None, width=None, height=None, **kwargs):
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
        head = True
        for coord in coords:
            x, y = coord
            grid[y][x] = BoardToken(TYPES.SNAKE, id, head)
            head = False

    return grid


def pretty_print(grid):
    rev = list(grid)
    rev.reverse()
    for row in rev:
        for col in row:
            tok = '_'
            if col.type == TYPES.SNAKE:
                if col.head:
                    tok = "\033[96m{}\033[0m".format(col.id)
                else:
                    tok = col.id
            elif col.type == TYPES.FOOD:
                tok = 'x'
            print('|' + tok, end='')
        print('|')

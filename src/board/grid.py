
class TYPES:
    EMPTY = 'Empty'
    FOOD = 'Food'
    SNAKE = 'Snake'


class BoardToken:

    def __init__(self, token_type, token_id=None, token_head=False,
                 token_tail=False, token_size=None):
        self.type = token_type
        self.id = token_id
        self.head = token_head
        self.tail = token_tail
        self.size = token_size

    def __str__(self):
        return f'{self.type}({self.id})'


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
        for idx, coord in enumerate(coords):
            head = idx == 0
            tail = idx == len(coords) - 1 and coord != coords[idx-1]
            size = len(coords)
            x, y = coord
            try:
                grid[y][x] = BoardToken(TYPES.SNAKE, id, head, tail, size)
            except IndexError:
                pass

    return grid


def pretty_print(board):
    rev = list(board)
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

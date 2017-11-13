
SNAKE = 'snake'
FOOD = 'food'
EMPTY = 'empty'


class BoardToken:

    def __init__(self, token_type, token_id=None):
        self.type = token_type
        self.id = token_id

    def data(self):
        return "{}({})".format(self.type, self.id or '')


class Game:

    def __init__(self, game_id=None, width=None, height=None, decider=None):
        self.id = game_id
        self.width = width
        self.height = height
        self.decider = decider(self)
        self.grid = None
        self.head = None
        self.me = None
        self.moves = []
        self.food = []

    def _trans(self, coord):
        return (coord[0], self.height - coord[1])

    def move(self, you=None, snakes=[], food=[]):
        self.me = you
        self.grid = [
            [BoardToken(EMPTY) for _ in range(self.width)]
            for _ in range(self.height)
        ]
        self.food = []

        for f in food:
            x, y = self._trans(f)
            self.grid[x][y] = BoardToken(FOOD)
            self.food.append((x, y))

        for s in snakes:
            if s['id'] == self.me:
                self.head = self._trans(s['coords'][0])
            for coord in s['coords']:
                x, y = self._trans(coord)
                self.grid[x][y] = BoardToken(SNAKE, s['id'])

        move = self.decider.decide()
        self.moves.append(move)
        return move

    def data(self):
        data = dict(self.__dict__)
        data['grid'] = [
            [i.type for i in row]
            for row in data['grid']
        ]
        data['decider'] = data['decider'].__class__.__name__
        return data

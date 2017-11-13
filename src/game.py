
SNAKE = 'snake'
FOOD = 'food'
EMPTY = 'empty'


class Food:

    def __init__(self, coord=None):
        self.coord = coord

    @property
    def x(self):
        return self.coord[1]

    @property
    def y(self):
        return self.coord[0]

    def at(self, x, y):
        return self.x == x and self.y == y


class Snake:

    def __init__(self, id=None, name=None,
                 taunt=None, health_points=None, coords=None):
        self.id = id
        self.name = name
        self.health_points = health_points
        self.coords = coords

    @property
    def head(self):
        return (
            self.coords[0][1],
            self.coords[0][0],
        )

    def at(self, x, y):
        for coord in self.coords:
            if coord[1] == x and coord[0] == y:
                return True
        return False

    def data(self):
        return dict(self.__dict__)


class BoardToken:
    def __init__(self, token_type, token_id=None):
        self.type = token_type
        self.id = token_id

    def data(self):
        return "{}({})".format(self.type, self.id or '')


class State:
    def __init__(self, you=None, game_id=None, turn=None,
                 food=None, snakes=None, dead_snakes=None, width=None,
                 height=None):
        self.id = game_id
        self.snake_id = you
        self.turn = turn
        self.food = [Food(f) for f in food]
        self.width = width
        self.height = height
        self.snakes = {}
        self.dead_snakes = {}
        self.move = None
        self.grid = [
            [BoardToken(EMPTY) for _ in range(self.width)]
            for _ in range(self.height)
        ]

        for f in self.food:
            self.grid[f.x][f.y] = BoardToken(
                FOOD, "{},{}".format(f.x, f.y),
            )

        self.snakes = {}
        for snake in snakes:
            s = Snake(**snake)
            self.snakes[snake['id']] = s
            for p in s.coords:
                self.grid[p[1]][p[0]] = BoardToken(SNAKE, s.id)

        self.dead_snakes = {}
        for snake in dead_snakes:
            self.dead_snakes[snake['id']] = Snake(**snake)

    def data(self):
        data = dict(self.__dict__)
        data["snakes"] = {
            snake.id: snake.data() for snake in self.snakes.values()
        }
        data["dead_snakes"] = {
            snake.id: snake.data() for snake in self.dead_snakes.values()
        }
        data["grid"] = [
            [col.data() if col else None for col in row]
            for row in data["grid"]
        ]
        return data


class Game:
    def __init__(self, game_id=None, width=None, height=None, decider=None):
        self.id = game_id
        self.width = width
        self.height = height
        self.states = []
        self.decider = decider(self)

    def move(self, **kwargs):
        state = State(**kwargs)
        self.states.append(state)
        state.move = self.decider.decide()
        return state.move

    @property
    def state(self):
        return self.states[-1]

    @property
    def grid(self):
        return self.state.grid

    @property
    def me(self):
        return self.state.snakes[self.state.snake_id]

    def data(self):
        data = dict(self.__dict__)
        data["states"] = [state.data() for state in self.states]
        data["decider"] = self.decider.__class__.__name__
        return data

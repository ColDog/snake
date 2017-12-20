import path


def test_matrix():
    grid = path.matrix(
        10, 10, (0, 0), cost_fn=path.default_cost_fn)
    print('')
    for row in grid:
        print(row)


def test_cost():
    matrix = path.matrix(10, 10, (0, 0))
    assert path.cost(matrix, (0, 0), (0, 1)) == 1


def test_shortest_path():
    matrix = path.matrix(10, 10, (0, 0))
    assert path.walk(matrix, (0, 0), (0, 1)) == [(0, 0), (0, 1)]


def test_direction():
    d = path.direction((0, 0), (0, 1))
    assert d == "up"
    d = path.direction((0, 1), (0, 0))
    assert d == "down"
    d = path.direction((0, 0), (1, 0))
    assert d == "right"
    d = path.direction((1, 0), (0, 0))
    assert d == "left"

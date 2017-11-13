import path


def test_matrix():
    grid = path.matrix(
        10, 10, (0, 0), cost_fn=path.default_cost_fn)
    print('')
    for row in grid:
        print(row)
    route, cost = path.walk(
        grid, (0, 0), (5, 5),
    )
    print('')
    print(cost)
    print(route)

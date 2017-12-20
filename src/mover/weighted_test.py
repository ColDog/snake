from .weighted import weighted_mover, _weights


def test_weighted_decider():
    state = dict(
        id='1',
        snakes={
            '1': [(0, 1), (0, 2)],
            '2': [(4, 4), (4, 5)],
        },
        food=[(0, 3)],
        height=10,
        width=10,
    )
    g = _weights(**state)
    _pretty_print(g)
    m = weighted_mover(**state)
    print(m)


def _pretty_print(grid):
    print('---')
    rev = list(grid)
    rev.reverse()
    for row in rev:
        for col in row:
            print('|' + _pad(str(col[1]), 3), end='')
        print('|')


def _pad(s, n):
    if len(s) < n:
        s += ' ' * (n - len(s))
    return s

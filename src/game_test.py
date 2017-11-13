import game
import decider


def test_game():
    g = game.Game(
        game_id='test',
        width=10,
        height=10,
        decider=decider.RandomDecider,
    )
    assert g.data() is not None


def test_game_move():
    g = game.Game(
        game_id='test',
        width=10,
        height=10,
        decider=decider.RandomDecider,
    )
    data = {
        "you": "2c4d4d70-8cca-48e0-ac9d-03ecafca0c98",
        "width": 10,
        "height": 10,
        "turn": 0,
        "food": [[0, 0]],
        "snakes": [{
            "id": "2c4d4d70-8cca-48e0-ac9d-03ecafca0c98",
            "name": "test",
            "coords": [[0, 0]],
        }],
        "dead_snakes": [{
            "id": "1c4d4d70-8cca-48e0-ac9d-03ecafca0c98",
            "name": "test",
            "coords": [[0, 0]],
        }]
    }
    g.move(**data)
    assert g.data() is not None


def test_snake():
    s = game.Snake(
        id='test',
        name='test',
        taunt=None,
        health_points=10,
        coords=[[1, 2]],
    )
    assert s.head == (2, 1)

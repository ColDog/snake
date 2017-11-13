import game
import decider


def test_game_move():
    g = game.Game(
        game_id='test',
        width=10,
        height=10,
        decider=decider.RandomDecider,
    )
    data = {
        "you": "2c4d4d70-8cca-48e0-ac9d-03ecafca0c98",
        "food": [[0, 0]],
        "snakes": [{
            "id": "2c4d4d70-8cca-48e0-ac9d-03ecafca0c98",
            "name": "test",
            "coords": [[0, 0]],
        }],
    }
    g.move(**data)
    print(g.__dict__)

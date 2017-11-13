from decider import WeightedDecider
from game import Game


def test_weighted_decider():
    g = Game(game_id='test', width=10, height=10, decider=WeightedDecider)
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

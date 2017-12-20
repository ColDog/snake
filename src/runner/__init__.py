from .game import Game, Snake, MoveError, GameError

__all__ = ['Game', 'Snake', 'MoveError', 'GameError']


def run(game):
    return [state for state in game.run()]

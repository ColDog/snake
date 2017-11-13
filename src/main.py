from flask import Flask, request, jsonify
from game import Game
from decider import RandomDecider

app = Flask(__name__)
games = {}


@app.route("/")
def index():
    return jsonify({
        "status": "ok",
        "games": {
            game.id: game.data() for game in games.values()
        },
    })


@app.route("/start", methods=["POST"])
def start():
    data = request.json
    data['decider'] = RandomDecider
    game = Game(**data)
    games[data['game_id']] = game
    return jsonify({"name": "test", "color": "#111"})


@app.route("/move", methods=["POST"])
def move():
    data = request.json
    game = games[data['game_id']]
    move = game.move(**data)
    return jsonify({"move": move})

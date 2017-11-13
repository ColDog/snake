from flask import Flask, request, jsonify

import decider
import game

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
    data['decider'] = decider.WeightedDecider
    current_game = game.Game(**data)
    games[data['game_id']] = current_game
    return jsonify({"name": "test", "color": "#111"})


@app.route("/move", methods=["POST"])
def move():
    data = request.json
    current_game = games[data['game_id']]
    move = current_game.move(
        you=data['you'],
        food=data['food'],
        snakes=data['snakes'],
    )
    return jsonify({"move": move})

import flask
import json
import snake
import util
import os

app = flask.Flask(__name__)


def snake_info():
    return {
        'name': f'coldog-{util.random_word()}-{util.random_word()}',
        'color': util.random_hex(),
        'head_type': 'bendr',
        'tail_type': 'curled',
        'secondary_color': util.random_hex(),
        'head_url': 'https://storage.googleapis.com/gopherizeme.appspot.com/gophers/d4990cb1e43574d3651384bb01e157aece51aad5.png',
    }


@app.route('/')
def index():
    return flask.jsonify(snake_info())


@app.route('/start', methods=['GET', 'POST'])
def start():
    return flask.jsonify(snake_info())


@app.route('/move', methods=['GET', 'POST'])
def move():
    state = flask.request.json
    board = state['board']
    convert = converter(board['width'], board['height'])
    game_state = game(
        id=state['you']['id'],
        width=board['width'],
        height=board['height'],
        food=[convert(f['x'], f['y']) for f in board['food']],
        snakes={
            s['id']: [
                convert(f['x'], f['y']) for f in s['body']
            ]
            for s in board['snakes']
        },
        health=state['you']['health'],
        friendlies={
            s['id']: s['name'].startswith('coldog-')
            for s in board['snakes']
        },
    )
    direction = snake.move(**game_state)
    return json.dumps({'move': direction})


def game(id=None, snakes=None, food=None, height=None, width=None,
         health=None, friendlies=None):
    return dict(id=id, snakes=snakes, food=food, height=height, width=width,
                health=health, friendlies=friendlies)


def converter(w, h):
    def convert(x, y):
        return (x, h-y-1)
    return convert


if __name__ == "__main__":
    port = os.environ.get("PORT", "8080")
    app.run(host='0.0.0.0', port=int(port), debug=True)

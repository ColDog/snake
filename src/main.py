import flask
import json
import snake
import util

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
    convert = converter(state['width'], state['height'])
    game_state = game(
        id=state['you']['id'],
        width=state['width'],
        height=state['height'],
        food=[convert(f['x'], f['y']) for f in state['food']['data']],
        snakes={
            s['id']: [
                convert(f['x'], f['y']) for f in s['body']['data']
            ]
            for s in state['snakes']['data']
        },
        health=state['you']['health'],
        friendlies={
            s['id']: s['name'].startswith('coldog-')
            for s in state['snakes']['data']
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
    app.run(host='0.0.0.0', port=8090, debug=True)

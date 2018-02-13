import flask
import json
import mover

app = flask.Flask(__name__)


@app.route('/start', methods=['GET', 'POST'])
def start():
    return flask.jsonify({
        'name': 'coldog-snake',
        'color': '#4286f4',
    })


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
    )
    direction = mover.weighted_mover(**game_state)
    return json.dumps({'move': direction})


def game(id=None, snakes=None, food=None, height=None, width=None,
         health=None):
    return dict(id=id, snakes=snakes, food=food, height=height, width=width,
                health=health)


def converter(w, h):
    def convert(x, y):
        return (x, h-y-1)
    return convert


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8090, debug=True)

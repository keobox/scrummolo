
"""API for scrummolo web."""

import flask
import settings

app = flask.Flask(__name__)

configs = {
        'team': settings.TEAM,
        'duration': settings.DURATION,
        'resources': settings.RESOURCES[0],
        'gameOverImage': settings.GAME_OVER_IMAGE,
        'gameOverSound' : settings.GAME_OVER_SOUND
    }

@app.route('/scrummolo/api/v1.0/configs', methods=['GET'])
def get_configs():
    """Returns a configs object to js."""
    return flask.jsonify({'configs': configs})

@app.errorhandler(404)
def not_found(error):
    return flask.make_response(flask.jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run(debug=True)
from flask import make_response


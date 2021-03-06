"""API for scrummolo web."""

import flask
import settings

app = flask.Flask(__name__)

resource_path = settings.RESOURCES[0].split("/")[-1]

configs = [
    {
        "id": 1,
        "team": settings.TEAM,
        "duration": settings.DURATION,
        "resources": resource_path,
        "gameOverImage": resource_path + "/" + settings.GAME_OVER_IMAGE,
        "gameOverSound": resource_path + "/" + settings.GAME_OVER_SOUND,
        "gameOverText": settings.GAME_OVER_TEXT,
        "questions": settings.QUESTIONS,
    }
]


@app.route("/")
@app.route("/index")
def index():
    """Main page."""
    return flask.render_template("scrummolo/index.html")


@app.route("/<path:path>")
def resources(path):
    return flask.send_from_directory("static/scrummolo/resources", path)


@app.route("/scrummolo/api/v1/configs", methods=["GET"])
def get_configs():
    """Returns a configs object."""
    return flask.jsonify({"configs": configs})


@app.route("/scrummolo/api/v1/configs/<int:config_id>", methods=["GET"])
def get_config(config_id):
    """Returns a configs object given an id:int."""
    # assuming the list ordered by id.
    try:
        return flask.jsonify({"config": configs[config_id - 1]})
    except IndexError:
        flask.abort(404)


@app.errorhandler(404)
def not_found(error):
    """Returns a not found as json response."""
    return flask.make_response(flask.jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    app.run(debug=True)

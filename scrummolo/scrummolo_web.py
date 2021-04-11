"""API for scrummolo web."""

import flask
import settings

app = flask.Flask(__name__)

resource_path = settings.RESOURCES[0].split("/")[-1]

teams = [
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
    return flask.send_from_directory("static/scrummolo", "index.html")


@app.route("/<path:path>")
def resources(path):
    return flask.send_from_directory("static/scrummolo/resources", path)


@app.route("/teams", methods=["GET"])
def get_teams():
    """Returns a configs object."""
    return {"teams": teams}


@app.route("/team/<int:team_id>", methods=["GET"])
def get_team(team_id):
    """Returns a configs object given an id:int."""
    # assuming the list is ordered by id.
    try:
        return {"team": teams[team_id - 1]}
    except IndexError:
        flask.abort(404)


@app.errorhandler(404)
def not_found(error):
    """Returns a not found as json response."""
    return flask.make_response(flask.jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    app.run(debug=True)

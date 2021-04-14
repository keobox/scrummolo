"""API for scrummolo web."""

import flask

app = flask.Flask(__name__)

assets_path = "cards"

teams = [
    {
        "id": 1,
        "team": ["Paolo", "Christian", "Marco"],
        "duration": 30,
        "assets": assets_path,
        "atlas": "cards",
        "gameOverImage": assets_path + "/" + "gameover.png",
        "gameOverSound": assets_path + "/" + "gameover.wav",
        "gameOverText": "That's all Folks, Thank You!",
        "questions": [
            "On what I worked yesterday?",
            "On what I will work today?",
            "Do I have any blocker?",
        ],
    }
]


@app.route("/")
@app.route("/index")
def index():
    """Main page."""
    return flask.send_from_directory("static/scrummolo", "index.html")


@app.route("/<path:path>")
def assets(path):
    """Images and sounds."""
    return flask.send_from_directory("static/scrummolo/assets", path)


@app.route("/teams", methods=["GET"])
def get_teams():
    """Returns a team resources."""
    return {"teams": teams}


@app.route("/team/<int:team_id>", methods=["GET"])
def get_team(team_id):
    """Returns a team resource given an id:int."""
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

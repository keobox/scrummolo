"""API for scrummolo web."""

import flask
import json

app = flask.Flask(__name__)

with open("scrummolo/static/scrummolo/js/config.json") as cfg:
    teams = json.load(cfg)


@app.route("/teams/<string:user>", methods=["GET"])
def get_teams(user):
    """Returns a team resources."""
    return {"teams": [team for team in teams['teams'] if team['user'] == user]}


@app.route("/team/<int:team_id>", methods=["GET"])
def get_team(team_id):
    """Returns a team resource given an id:int."""
    # assuming the list is ordered by id.
    try:
        return {"team": teams["teams"][team_id - 1]}
    except IndexError:
        flask.abort(404)


@app.errorhandler(404)
def not_found(error):
    """Returns a not found as json response."""
    return flask.make_response(flask.jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    app.run(debug=True)

"""API for scrummolo web."""

import json
import uuid

import flask

from scrummolo.repository.mem_repository import MemRepository
from scrummolo.requests.team_request import TeamRequest
from scrummolo.use_cases.find_teams_by_user_use_case import find_teams_by_user
from scrummolo.use_cases.find_team_by_id_use_case import find_team_by_id

app = flask.Flask(__name__)
data = [
    {
        "team_id": str(uuid.uuid4()),
        "duration": 25,
        "name": "jeeg",
        "skin": "mecha",
        "user": "nagai",
        "questions": [
            "Can you launch the components?",
            "Can you squash that Haniwa monster?",
        ],
        "players": ["Hiroshi", "Miwa"],
    }
]
db = MemRepository(data)


@app.route("/teams/<string:user>", methods=["GET"])
def get_teams(user):
    """Returns a team resources."""
    teams = find_teams_by_user(db, user)
    return {"teams": teams}


@app.route("/team/<string:team_id>", methods=["GET"])
def get_team(team_id):
    """Returns a team resource given an id."""
    try:
        team = find_team_by_id(db, team_id)
        return {"team": team}
    except IndexError:
        flask.abort(404)


@app.errorhandler(404)
def not_found(error):
    """Returns a not found as json response."""
    return flask.make_response(flask.jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    app.run(debug=True)

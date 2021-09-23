"""API for scrummolo web."""

import dataclasses
import uuid

from flask import Flask, request, make_response
from pydantic import ValidationError

from scrummolo.repository.mem_repository import MemRepository
from scrummolo.requests.team_request import TeamRequest
from scrummolo.use_cases.add_team_use_case import add_team
from scrummolo.use_cases.find_team_by_id_use_case import find_team_by_id
from scrummolo.use_cases.find_teams_by_user_use_case import find_teams_by_user

app = Flask(__name__)
db = MemRepository(None)


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
        return {"message": "Not found"}, 404


@app.route("/team", methods=["POST"])
def create_team():
    """Creates a team resource."""
    try:
        req = request.json
        req["team_id"] = str(uuid.uuid4())
        parsed_req = TeamRequest(**req)
        parsed_dict = dataclasses.asdict(parsed_req)
        add_team(db, parsed_dict)
        return {"team": parsed_dict}, 201
    except TypeError as te:
        return {"message": str(te)}, 400
    except ValidationError as ve:
        return {"message": str(ve)}, 400
    except ValueError as ve:
        return {"message": str(ve)}, 403


@app.errorhandler(404)
def not_found(error):
    """Returns a not found as json response."""
    return make_response({"error": "Not found"}, 404)


if __name__ == "__main__":
    app.run(debug=True)

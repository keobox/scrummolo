import dataclasses
import uuid

import pydantic
import pytest

from scrummolo.domain.team import Team
from scrummolo.requests.team_request import TeamRequest


def test_team_request_accepted():
    data = {
        "team_id": uuid.uuid4(),
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
    team_request = TeamRequest(**data)
    valid_data = dataclasses.asdict(team_request)
    team = Team(**valid_data)
    assert team.to_dict() == data


def test_team_request_missing_field():
    data = {
        "team_id": uuid.uuid4(),
        "duration": 25,
        "name": "Mazinger Z",
        "user": "nagai",
        "questions": ["Where doc Hell is?"],
        "players": ["Koji", "Sayaka"],
    }
    with pytest.raises(TypeError) as ex:
        TeamRequest(**data)
    assert ex


def test_team_request_invalid_data():
    data = {
        "team_id": uuid.uuid4(),
        "duration": "twenty",
        "name": "Mazinger Z",
        "skin": "mecha",
        "user": "nagai",
        "questions": ["Where doc Hell is?"],
        "players": ["Koji", "Sayaka"],
    }
    with pytest.raises(pydantic.ValidationError) as ex:
        TeamRequest(**data)
    assert ex


def test_team_request_coercion():
    data = {
        "team_id": uuid.uuid4(),
        "duration": "30",
        "name": "Mazinger Z",
        "skin": "mecha",
        "user": "nagai",
        "questions": ["Where doc Hell is?"],
        "players": ["Koji", "Sayaka"],
    }
    team_request = TeamRequest(**data)
    assert team_request.duration == 30

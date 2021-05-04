import json

import pytest

from scrummolo_api import app, db


@pytest.fixture(scope="session", autouse=True)
def do_something():
    db.add_team(
        {
            "team_id": "uuid-uuid",
            "duration": 25,
            "name": "jeeg",
            "skin": "mecha",
            "user": "user",
            "questions": ["How are you?"],
            "players": ["PlayerA", "PlayerB"],
        }
    )


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_get_team(client):
    resp = client.get("/team/uuid-uuid")
    assert resp.status_code == 200


def test_get_team_404(client):
    resp = client.get("/team/nonce")
    assert resp.status_code == 404


def test_get_teams(client):
    resp = client.get("/teams/user")
    assert resp.status_code == 200


def test_get_teams_404(client):
    resp = client.get("/teams/nonce")
    data = json.loads(resp.data)
    assert resp.status_code == 200
    assert len(data["teams"]) == 0


def test_create_team(client):
    resp = client.post(
        "/team",
        data=json.dumps(
            {
                "duration": 15,
                "name": "jeeg2",
                "skin": "mecha",
                "user": "user",
                "questions": ["How are you?"],
                "players": ["Player1", "Player2"],
            }
        ),
        headers={"Content-Type": "application/json"},
    )
    assert resp.status_code == 201


def test_create_team_coercion_on_duration(client):
    resp = client.post(
        "/team",
        data=json.dumps(
            {
                "duration": "20",
                "name": "jeeg2",
                "skin": "mecha",
                "user": "user1",
                "questions": ["How are you?"],
                "players": ["Player1", "Player2"],
            }
        ),
        headers={"Content-Type": "application/json"},
    )
    assert resp.status_code == 201
    data = json.loads(resp.data)
    assert data["team"]["duration"] == 20


def test_create_team_missing_field(client):
    # skin removed
    resp = client.post(
        "/team",
        data=json.dumps(
            {
                "duration": "20",
                "name": "jeeg2",
                "user": "user2",
                "questions": ["How are you?"],
                "players": ["Player1", "Player2"],
            }
        ),
        headers={"Content-Type": "application/json"},
    )
    assert resp.status_code == 400


def test_create_team_validation_on_duration(client):
    resp = client.post(
        "/team",
        data=json.dumps(
            {
                "duration": "2x",
                "name": "jeeg2",
                "skin": "mecha",
                "user": "user3",
                "questions": ["How are you?"],
                "players": ["Player1", "Player2"],
            }
        ),
        headers={"Content-Type": "application/json"},
    )
    assert resp.status_code == 400

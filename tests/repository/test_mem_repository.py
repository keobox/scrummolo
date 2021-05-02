import uuid

import pytest

from scrummolo.domain.team import Team
from scrummolo.repository.mem_repository import MemRepository


@pytest.fixture
def data_for_repo():
    return [
        {
            "team_id": uuid.uuid4(),
            "duration": 25,
            "name": "x",
            "skin": "skin",
            "user": "k",
            "questions": ["Q?", "P?"],
            "players": ["Ace", "Dice"],
        },
        {
            "team_id": uuid.uuid4(),
            "duration": 20,
            "name": "y",
            "skin": "skin",
            "user": "k",
            "questions": ["Z?", "Y?"],
            "players": ["A", "B"],
        },
        {
            "team_id": uuid.uuid4(),
            "duration": 20,
            "name": "z",
            "skin": "skin",
            "user": "j",
            "questions": ["Z?", "Y?"],
            "players": ["A", "B"],
        },
    ]


def test_find_team_by_user(data_for_repo):
    repo = MemRepository(data_for_repo)
    entities = repo.find_teams_by_user("k")
    assert isinstance(entities[0], Team)
    assert len(entities) == 2
    assert len(repo.list()) == 3


def test_find_team_by_id(data_for_repo):
    repo = MemRepository(data_for_repo)
    team_id = data_for_repo[0]["team_id"]
    team = repo.find_team_by_id(team_id)
    assert team.team_id == team_id


def test_add_team():
    repo = MemRepository([])
    repo.add_team(
        {
            "team_id": uuid.uuid4(),
            "duration": 20,
            "name": "z",
            "skin": "skin",
            "user": "j",
            "questions": ["Z?", "Y?"],
            "players": ["A", "B"],
        }
    )
    assert len(repo.list()) == 1

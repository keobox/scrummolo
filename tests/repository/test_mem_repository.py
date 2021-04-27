import uuid

from scrummolo.domain.team import Team
from scrummolo.repository.mem_repository import MemRepository


def test_find_team_by_user():
    data = [
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
    repo = MemRepository(data)
    entities = repo.find_teams_by_user("k")
    assert isinstance(entities[0], Team)
    assert len(entities) == 2
    assert len(repo.list()) == 3


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

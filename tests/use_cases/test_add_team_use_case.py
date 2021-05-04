import uuid
from unittest import mock

import pytest

from scrummolo.domain.team import Team
from scrummolo.use_cases.add_team_use_case import add_team


def test_add_team_use_case():
    team_dict = {
        "team_id": uuid.uuid4(),
        "duration": 25,
        "name": "daitarn",
        "skin": "mecha",
        "user": "nakajima",
        "questions": ["How many meganoids can we destroy?", "Should we go on mars?"],
        "players": ["Banjo", "Beauty", "Reika", "Toppy"],
    }
    repo = mock.Mock()
    repo.find_teams_by_user.return_value = []
    repo.add_team.return_value = Team.from_dict(team_dict)
    team = add_team(repo, team_dict)
    repo.add_team.assert_called_with(team_dict)
    assert team == Team.from_dict(team_dict)


def test_add_team_max_number_of_teams_reached():
    teams = [
        {
            "team_id": uuid.uuid4(),
            "duration": 25,
            "name": "maginger z",
            "skin": "mecha",
            "user": "nagai",
            "questions": ["Where doc Hell is?", "Should we attack?"],
            "players": ["Koji", "Sayaka"],
        },
        {
            "team_id": uuid.uuid4(),
            "duration": 25,
            "name": "goldrake",
            "skin": "mecha",
            "user": "nagai",
            "questions": ["Should we attack the moon?"],
            "players": ["Actarus", "Koji", "Venusia"],
        },
    ]
    repo = mock.Mock()
    repo.find_teams_by_user.return_value = [Team(**d) for d in teams]
    new_team = {
        "team_id": uuid.uuid4(),
        "duration": 25,
        "name": "great mazinger",
        "skin": "mecha",
        "user": "nagai",
        "questions": ["Should we attack Mikenes?"],
        "players": ["Tetsuya", "Jun"],
    }
    with pytest.raises(ValueError) as ve:
        add_team(repo, new_team)
        assert str(ve) == "Max number of teams reached"


def test_add_team_max_number_of_players_reached():
    repo = mock.Mock()
    repo.find_teams_by_user.return_value = []
    new_team = {
        "team_id": uuid.uuid4(),
        "duration": 20,
        "name": "great mazinger",
        "skin": "mecha",
        "user": "nagai",
        "questions": ["Should we attack Mikenes?"],
        "players": ["Tetsuya", "Jun", "a", "b", "c", "d", "e", "f", "g"],
    }
    with pytest.raises(ValueError) as ve:
        add_team(repo, new_team)
        assert str(ve) == "Max number of players reached"

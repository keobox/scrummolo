import uuid
from unittest import mock

from scrummolo.domain.team import Team
from scrummolo.use_cases.add_team_use_case import add_team


def test_add_team_use_case():
    team_dict = {
        "team_id": uuid.uuid4(),
        "duration": 25,
        "name": "daitarn",
        "skin": "mecha",
        "user": "nakajima",
        "questions": ["How many meganoids can we destroy", "Should we go on mars?"],
        "players": ["Banjo", "Beauty", "Reika", "Toppy"]
    }
    repo = mock.Mock()
    repo.add_team.return_value = Team.from_dict(team_dict)
    team = add_team(repo, team_dict)
    repo.add_team.assert_called_with(team_dict)
    assert team == Team.from_dict(team_dict)

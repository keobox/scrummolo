import pytest
import uuid
from unittest import mock

from scrummolo.domain.team import Team
from scrummolo.use_cases.find_teams_by_user_use_case import find_teams_by_user
from scrummolo.use_cases.find_team_by_id_use_case import find_team_by_id


@pytest.fixture
def domain_teams():
    team_1 = Team(
        team_id=uuid.uuid4(),
        duration=20,
        name="pirates",
        skin="jolly_roger",
        user="the_queen",
        questions=["How many gold doubloons yesterday?", "Do you have Grog today?"],
        players=["Bellamy", "England", "Taylor"],
    )
    team_2 = Team(
        team_id=uuid.uuid4(),
        duration=15,
        name="apple",
        skin="computers",
        user="jobs",
        questions=[
            "Did you buy the mother board?",
            "Did you said is all about design?",
        ],
        players=["Steve Jobs", "Steve Wozniak"],
    )
    team_3 = Team(
        team_id=uuid.uuid4(),
        duration=30,
        name="pixar",
        skin="translucent",
        user="jobs",
        questions=[
            "How many play hours yesterday?",
            "Should we invent a new game today?",
        ],
        players=["Woody", "Buzz", "Andy"],
    )
    return [team_1, team_2, team_3]


def test_find_by_user(domain_teams):
    repo = mock.Mock()
    expected_result = [t for t in domain_teams if t.user == "jobs"]
    repo.find_teams_by_user.return_value = expected_result
    result = find_teams_by_user(repo, "jobs")
    assert result == expected_result


def test_find_by_id(domain_teams):
    repo = mock.Mock()
    expected_result = domain_teams[0]
    team_id = expected_result.team_id
    repo.find_team_by_id.return_value = expected_result
    result = find_team_by_id(repo, team_id)
    assert result == expected_result

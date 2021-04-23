import uuid
from scrummolo.domain.team import Team

questions_list = [
    "On what I worked yesterday?",
    "On what I will work today?",
    "Do I have any blocker?",
]
players_list = ["Ace", "Jack", "Queen", "King", "Ten"]


def test_team_model_init():
    id_ = uuid.uuid4()
    team = Team(
        team_id=id_,
        duration=20,
        name="alice",
        questions=questions_list,
        skin="cards",
        players=players_list,
        user="carrol",
    )
    assert team.team_id == id_
    assert team.duration == 20
    assert team.name == "alice"
    assert team.questions == questions_list
    assert team.skin == "cards"
    assert team.players == players_list
    assert team.user == "carrol"


def test_team_model_from_dict():
    id_ = uuid.uuid4()
    init_dict = {
        "team_id": id_,
        "duration": 15,
        "name": "white rabbit",
        "questions": questions_list,
        "skin": "cards",
        "players": players_list,
        "user": "lewis",
    }
    team = Team.from_dict(init_dict)
    assert team.to_dict() == init_dict

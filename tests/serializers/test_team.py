import json
import uuid

from scrummolo.serializers.team import TeamJsonEncoder
from scrummolo.domain.team import Team


def test_serialize_domain_team():
    id_ = uuid.uuid4()
    questions_list = ["Are we ready?", "Where's  Rivendell?"]
    players_list = ["Frodo", "Sam", "Gandalf", "Aragorn"]
    team = Team(
        team_id=id_,
        duration=30,
        name="Fellowship of the Ring",
        skin="arda",
        user="J. R. R. Tolkien",
        questions=questions_list,
        players=players_list
    )
    expected_json_d = team.to_dict()
    expected_json_d["team_id"] = str(expected_json_d["team_id"])
    expected_json = json.dumps(expected_json_d)
    json_team = json.dumps(team, cls=TeamJsonEncoder)
    assert json.loads(json_team) == json.loads(expected_json)

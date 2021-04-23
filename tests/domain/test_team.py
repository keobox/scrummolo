import uuid
from scrummolo.domain.team import Team

def test_team_model_init():
    id_ = uuid.uuid4()
    questions_list = [
        'On what I worked yesterday?',
        'On what I will work today?',
        'Do I have any blocker?'
    ]
    players_list = ['Ace', 'Jack', 'Queen', 'King', 'Ten']
    team = Team(
        id=id_,
        duration=20,
        name='team 1',
        questions=questions_list,
        skin="cards",
        players=players_list,
        user='the_user_id'
    )
    assert team.id == id_
    assert team.duration == 20
    assert team.name == 'team 1'
    assert team.questions == questions_list
    assert team.skin == 'cards'
    assert team.players == players_list
    assert team.user == 'the_user_id'
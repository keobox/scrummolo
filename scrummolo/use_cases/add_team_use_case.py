MAX_TEAMS_NUMBER = 2
MAX_PLAYERS_NUMBER = 8


def add_team(repo, team_dict):
    # TODO check max number of questions here?
    user = team_dict['user']
    teams = repo.find_teams_by_user(user)
    if len(teams) >= MAX_TEAMS_NUMBER:
        raise ValueError("Max number of teams reached")
    if len(team_dict['players']) > MAX_PLAYERS_NUMBER:
        raise ValueError("Max number of players reached")
    return repo.add_team(team_dict)

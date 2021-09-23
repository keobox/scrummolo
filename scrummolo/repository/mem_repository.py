from scrummolo.domain.team import Team


class MemRepository:
    def __init__(self, data):
        if data:
            self.data = data
        else:
            self.data = []

    def find_teams_by_user(self, user):
        return [Team(**t) for t in self.data if t["user"] == user]

    def find_team_by_id(self, team_id):
        teams = [Team(**t) for t in self.data if t["team_id"] == team_id]
        return teams[0]

    def add_team(self, team_doc):
        self.data.append(team_doc)

    def list(self):
        return list(self.data)

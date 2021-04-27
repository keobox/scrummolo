from scrummolo.domain.team import Team


class MemRepository:

    def __init__(self, data):
        if data:
            self.data = data
        else:
            self.data = []

    def find_teams_by_user(self, user):
        return [Team(**t) for t in self.data if t["user"] == user]

    def add_team(self, data_doc):
        t = Team(**data_doc)
        self.data.append(t)
        return t

    def list(self):
        return list(self.data)

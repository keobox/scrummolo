import json


class TeamJsonEncoder(json.JSONEncoder):
    def default(self, o):
        try:
            to_serialize = {
                "team_id": str(o.team_id),
                "duration": o.duration,
                "name": o.name,
                "skin": o.skin,
                "user": o.user,
                "questions": o.questions,
                "players": o.players,
            }
            return to_serialize
        except AttributeError:
            return super().default(o)

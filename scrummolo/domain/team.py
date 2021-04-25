import dataclasses
import typing


def default_questions_list():
    return [
        "On what I worked yesterday?",
        "On what I will work today?",
        "Do I have any blocker?",
    ]


@dataclasses.dataclass
class Team:
    team_id: typing.Any
    duration: int
    name: str
    skin: str
    user: str
    questions: typing.List[str] = dataclasses.field(default_factory=default_questions_list)
    players: typing.List[str] = dataclasses.field(default_factory=list)

    @classmethod
    def from_dict(cls, d):
        return cls(**d)

    def to_dict(self):
        return dataclasses.asdict(self)

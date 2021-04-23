import dataclasses
import typing


@dataclasses.dataclass
class Team:
    team_id: typing.Any
    duration: int
    name: str
    skin: str
    user: str
    questions: list = dataclasses.field(default_factory=list)
    players: list = dataclasses.field(default_factory=list)

    @classmethod
    def from_dict(cls, d):
        return cls(**d)

    def to_dict(self):
        return dataclasses.asdict(self)

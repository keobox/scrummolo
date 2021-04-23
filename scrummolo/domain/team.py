import dataclasses

@dataclasses.dataclass
class Team:
    id: 'typing.Any'
    duration: int
    name: str
    skin: str
    user: str
    questions: list = dataclasses.field(default_factory=list)
    players: list = dataclasses.field(default_factory=list)

    
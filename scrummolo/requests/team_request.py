import pydantic

from scrummolo.domain.team import Team

# TeamRequest is just a decorated domain data class
TeamRequest = pydantic.dataclasses.dataclass(Team)

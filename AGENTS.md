# Scrummolo

Scrummolo is a "talking stick" web application for standup meetings. It cycles through team members, presenting each one with timed standup questions in a fun, game-like interface.

## Architecture

The backend follows **Clean Architecture** (Robert C. Martin). Each layer lives in its own package under `scrummolo/`:

```
scrummolo/
  domain/         # Entities - pure data, no dependencies
  use_cases/      # Business logic - depends only on domain + repository interface
  requests/       # Input validation (Pydantic) - boundary between API and use cases
  serializers/    # Output formatting - boundary between use cases and API
  repository/     # Data access - currently in-memory, swappable
```

**Dependency rule**: inner layers never import outer layers. Domain knows nothing about Flask, Pydantic, or persistence. Use cases know about domain and repository interfaces but not about HTTP or serialization.

The Flask app (`scrummolo_api.py`) is a thin adapter that wires everything together. It is not the application - it is a delivery mechanism.

## Current state

- **Backend**: Flask REST API with 3 endpoints (`POST /team`, `GET /team/<id>`, `GET /teams/<user>`). In-memory repository (no database yet). Target deployment is AWS Lambda, Flask is used for local development.
- **Frontend**: Phaser 3.54.0 game (ES6 modules, no build step, no Node.js). Lives in `static/src/`.
- **Legacy PoC**: Original Pyglet desktop app in `scrummolo.py`, runnable via `poc.sh`.

## How to extend the backend

### Adding a new domain entity

1. Create `scrummolo/domain/<entity>.py` with a `@dataclasses.dataclass` class.
2. Include `from_dict()` and `to_dict()` methods for serialization round-trips.
3. Keep the entity free of framework imports - no Flask, no Pydantic, no database code.
4. Write tests in `tests/domain/test_<entity>.py` verifying init and dict conversion.

Example - the existing `Team` entity (`scrummolo/domain/team.py`):

```python
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
```

### Adding a new use case

Use cases are plain functions that receive a repository and input data, apply business rules, and return domain entities.

1. Create `scrummolo/use_cases/<action>_use_case.py`.
2. The function signature should be `def <action>(repo, ...)`.
3. Put business rules here (validation limits, authorization checks, etc.), not in the repository or the API layer.
4. Raise `ValueError` for business rule violations.
5. Write tests in `tests/use_cases/test_<action>_use_case.py` using `unittest.mock.Mock()` for the repository.

Example - the existing `add_team` use case (`scrummolo/use_cases/add_team_use_case.py`):

```python
MAX_TEAMS_NUMBER = 2
MAX_PLAYERS_NUMBER = 8

def add_team(repo, team_dict):
    user = team_dict['user']
    teams = repo.find_teams_by_user(user)
    if len(teams) >= MAX_TEAMS_NUMBER:
        raise ValueError("Max number of teams reached")
    if len(team_dict['players']) > MAX_PLAYERS_NUMBER:
        raise ValueError("Max number of players reached")
    return repo.add_team(team_dict)
```

### Testing a use case

Mock the repository. Verify the use case calls the repository correctly and enforces business rules. See `tests/use_cases/test_add_team_use_case.py` for the pattern:

```python
def test_add_team_use_case():
    team_dict = { ... }
    repo = mock.Mock()
    repo.find_teams_by_user.return_value = []
    repo.add_team.return_value = Team.from_dict(team_dict)
    team = add_team(repo, team_dict)
    repo.add_team.assert_called_with(team_dict)
    assert team == Team.from_dict(team_dict)
```

Test the happy path, then test each business rule violation separately with `pytest.raises(ValueError)`.

### Adding a new repository method

1. Add the method to `scrummolo/repository/mem_repository.py`.
2. The repository stores raw dictionaries and returns domain entities.
3. Write tests in `tests/repository/test_mem_repository.py`.

### Adding request validation

1. Create or extend a Pydantic model in `scrummolo/requests/`.
2. This layer validates and coerces input at the API boundary (e.g., string `"30"` to int `30` for duration).
3. Write tests in `tests/requests/` covering valid input, missing fields, and type mismatches.

### Adding a new API endpoint

1. Add the Flask route in `scrummolo_api.py`.
2. The route should only: parse input, call the request validator, call the use case, serialize the response.
3. Map exceptions to HTTP status codes: `TypeError`/`ValidationError` to 400, `ValueError` to 403, `IndexError` to 404.
4. Write integration tests in `tests/flask_integration/test_flask_integration.py`.

### Running tests

```bash
pytest
```

Dev dependencies are in `requirements_dev.txt` (pytest, pytest-flask, black).

## How to extend the frontend

The frontend is a Phaser 3 game in `static/src/`. No build tools, no Node.js, no bundler - just ES6 modules loaded directly by the browser.

### Structure

```
static/src/
  index.html                   # Entry point
  js/
    main.js                    # Bootstrap: fetch config, create game
    config/game-config.js      # Phaser game configuration factory
    game/
      GameScene.js             # Phaser Scene: rendering, input, UI
      GameState.js             # State machine: players, questions, timer
    utils/
      array-utils.js           # Fisher-Yates shuffle
      image-utils.js           # Aspect-ratio image resizing
```

### Guidelines

- **No Node.js, no npm, no bundler**. Load Phaser from a script tag or local copy. Use ES6 `import`/`export` for modules.
- **Keep dependencies minimal**. The only external dependency is Phaser. Do not add more libraries unless absolutely necessary.
- **GameState** owns the game logic (who plays next, what question, timer). **GameScene** owns the rendering and input. Keep this separation.
- Assets (sprites, sounds, images) go in the `static/` directory alongside `src/`.

## Future features (not yet implemented)

- **Team management**: add a development team by choosing member names and avatar images.
- **Authentication**: sign-up and sign-in via Amazon Cognito (frontend integration, backend delegates to Cognito).

# Frontend Missing Bits

## 1. Missing: `config.json`

**Location**: `static/src/js/config.json`

The frontend expects this file to be served at `/js/config.json`. It is fetched by `main.js` and must contain:

```json
{
  "config": {
    "assets": "<path-to-assets>",
    "gameOverImage": "<game-over-image.png>",
    "gameOverSound": "<game-over-sound.mp3>",
    "gameOverText": "Game Over!"
  },
  "teams": [
    {
      "team_id": "...",
      "duration": 1,
      "name": "Team Name",
      "skin": "default",
      "user": "username",
      "questions": ["Question 1?", "Question 2?"],
      "players": ["Player1", "Player2"]
    }
  ]
}
```

## 2. Missing: Assets Directory

**Expected location**: `static/src/js/assets/` (or wherever `config.assets` points)

The GameScene (`GameScene.js:17-34`) loads these assets:

| Asset | Expected Path |
|-------|---------------|
| Sprite Atlas Image | `{assets}/{skin}/{skin}.png` |
| Sprite Atlas JSON | `{assets}/{skin}/{skin}.json` |
| Game Over Image | `{assets}/{config.gameOverImage}` |
| Game Over Sound | `{assets}/{config.gameOverSound}` |

Example for `skin: "default"`:
- `assets/default/default.png`
- `assets/default/default.json`
- `assets/gameover.png`
- `assets/gameover.mp3`

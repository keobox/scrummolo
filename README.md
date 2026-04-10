# Scrummolo
A standup meeting talking stick.

Purpose:
- Use during a stand up meeting for
- Having fun
- Icebreaking
- Keeping focus

## Local AI assisted
Using opencode in a container and ollama on a Mac M4 48 GB RAM.

### Configuration
```shell
# Create a hidden config folder in your current project
mkdir .opencode

# Create the config file locally
cat <<EOF > .opencode/opencode.json
{
  "provider": {
    "ollama": {
      "npm": "@ai-sdk/openai-compatible",
      "options": {
        "baseURL": "http://host.containers.internal:11434/v1"
      },
      "models": {
        "qwen3.5:latest": { "name": "qwen3.5:latest" }
      }
    }
  },
  "instructions": "Always use 'uv run' to execute python scripts. Use 'uv add' to install new dependencies."
}
EOF
```

### To build the container
```shell
podman build -t opencode-python .
```

### To run in a container
```shell
alias opencode='podman run -it --rm \
  -p 5000:5000 \
  -v "$(pwd)":/app \
  -w /app \
  -e OPENCODE_CONFIG_DIR=/app/.opencode \
  -e FLASK_APP=scrummolo_api.py \
  opencode-python'

  opencode
```

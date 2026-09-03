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
  "$schema": "https://opencode.ai/config.json",
  "model": "ollama-host/hf.co/unsloth/Qwen3.8-27B-GGUF:UD-Q6_K",
  "compaction": {
    "auto": true,
    "prune": true,
    "reserved": 10000
  },
  "provider": {
    "ollama": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "Ollama (container)",
      "options": {
        "baseURL": "http://host.containers.internal:11434/v1"
      },
      "models": {
        "hf.co/unsloth/Qwen3.8-27B-GGUF:UD-Q6_K": { "name": "hf.co/unsloth/Qwen3.8-27B-GGUF:UD-Q6_K" }
      }
    },
    "ollama-host": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "Ollama (local)",
      "options": {
        "baseURL": "http://localhost:11434/v1"
      },
      "models": {
        "hf.co/unsloth/Qwen3.8-27B-GGUF:UD-Q6_K": { "name": "hf.co/unsloth/Qwen3.8-27B-GGUF:UD-Q6_K" }
      }
    }
  }
}
EOF
```

NOTE: "Ollama (container)" provider is for the containerized opencode while "Ollama (local)" is for opencode installed on the host.
I did this because the containerized opencode does not work great in the Mac terminal.

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

## Using pi-harness
Opencode didn't look OK in the containerized environment, so I decided to give Pi a try.
Look at `Containerfile.pi`

### Configuration

pi-config/models.json
```shell
{
  "providers": {
    "ollama": {
      "baseUrl": "http://host.docker.internal:11434/v1",
      "api": "openai-completions",
      "apiKey": "not-needed",
      "models": [
        {
          "id": "hf.co/unsloth/Qwen3.8-27B-GGUF:UD-Q6_K",
          "name": "Qwen3.8 27B (Q6_K, 22GB)",
          "reasoning": false,
          "input": ["text"],
          "contextWindow": 128000,
          "maxTokens": 16384
        }
      ]
    }
  }
}
```

pi-config/settings.json
```shell
{
  "defaultProvider": "ollama",
  "defaultModel": "hf.co/unsloth/Qwen3.8-27B-GGUF:UD-Q6_K",
  "defaultAgent": "coder"
}
```

### To build the container
```shell
podman build -t pi-harness -f Containerfile.pi .
```

### To run in a container
```shell
# host.docker.internal resolves to your host (where Ollama runs)
podman run --rm -it \
  -v "$PWD:/workspace" \
  -v "$PWD/pi-config:/root/.pi/agent" \
  pi-harness
```

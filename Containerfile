# Start with the official OpenCode image
FROM ghcr.io/anomalyco/opencode

# Switch to root to install system tools
USER root

# 1. Install uv (Copy the static binary)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# 2. Install Python 3 and build essentials using Alpine's manager (apk)
# Note: In Alpine, the pip package is usually included or named py3-pip
RUN apk add --no-cache python3 py3-pip build-base

# 3. Set environment variables for uv
ENV UV_PROJECT_ENVIRONMENT=/app/.venv
ENV PATH="/app/.venv/bin:$PATH"

# Set the working directory to your mounted project
WORKDIR /app

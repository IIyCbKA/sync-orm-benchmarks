#!/usr/bin/env bash
set -euo pipefail

if command -v docker-compose >/dev/null 2>&1; then
  DC=("docker-compose")
elif command -v docker >/dev/null 2>&1 && docker compose version >/dev/null 2>&1; then
  DC=("docker" "compose")
else
  echo "ERROR: neither 'docker-compose' nor 'docker compose' found in PATH." >&2
  exit 1
fi

if [ -f "docker-compose.yaml" ]; then
  COMPOSE_FILE="docker-compose.yaml"
else
  echo "ERROR: compose file not found in current dir." >&2
  exit 2
fi

echo "Following logs for runner service..."
"${DC[@]}" -f "$COMPOSE_FILE" logs -f runner

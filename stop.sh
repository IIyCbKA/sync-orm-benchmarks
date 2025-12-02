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

declare -A MAP=(
  ["pony"]="benchmarks/pony_bench/docker-compose.yml"
)

NAME="${1:-}"
if [ -z "$NAME" ]; then
  echo "Usage: $0 <solution-name>"
  echo "Available: ${!MAP[@]}"
  exit 1
fi

COMPOSE_FILE="${MAP[$NAME]:-}"
if [ -z "$COMPOSE_FILE" ]; then
  echo "ERROR: unknown solution name: '$NAME'. Available: ${!MAP[@]}" >&2
  exit 2
fi

if [ ! -f "$COMPOSE_FILE" ]; then
  echo "ERROR: compose file not found: $COMPOSE_FILE" >&2
  exit 3
fi

echo ">>> Stopping and removing '${NAME}' using compose file: $COMPOSE_FILE"
echo ">>> Command: ${DC[*]} -f $COMPOSE_FILE down -v --remove-orphans"

"${DC[@]}" -f "$COMPOSE_FILE" down -v --remove-orphans

echo ">>> Done: containers, networks and declared volumes removed for '$NAME'."

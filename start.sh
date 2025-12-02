#!/usr/bin/env bash
set -euo pipefail

DC=""
if command -v docker-compose >/dev/null 2>&1; then
  DC="docker-compose"
elif command -v docker >/dev/null 2>&1 && docker compose version >/dev/null 2>&1; then
  DC="docker compose"
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
  echo "Please adjust the PATH in start.sh MAP or run from repo root." >&2
  exit 3
fi

echo "Using compose command: $DC"
echo "Starting '$NAME' using $COMPOSE_FILE ..."

$DC -f "$COMPOSE_FILE" up -d --build

echo
echo "Done. To follow logs: $DC -f $COMPOSE_FILE logs -f"
echo "To stop and remove containers+volumes: ./stop.sh $NAME"

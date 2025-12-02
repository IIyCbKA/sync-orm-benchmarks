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

if [ "$#" -ne 1 ]; then
  echo "Usage: $0 <solution>"
  echo "Available: ${!MAP[@]}"
  exit 1
fi

NAME="$1"
COMPOSE_FILE="${MAP[$NAME]:-}"

if [ -z "$COMPOSE_FILE" ]; then
  echo "ERROR: unknown solution name: '$NAME'. Available: ${!MAP[@]}" >&2
  exit 2
fi

if [ ! -f "$COMPOSE_FILE" ]; then
  echo "ERROR: compose file not found: $COMPOSE_FILE" >&2
  echo "Run from repo root or update MAP in logs.sh" >&2
  exit 3
fi

echo "Following logs for '$NAME' (runner service)..."
"${DC[@]}" -f "$COMPOSE_FILE" logs -f runner

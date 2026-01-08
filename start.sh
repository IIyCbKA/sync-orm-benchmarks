#!/usr/bin/env bash
set -euo pipefail

if [ ! -f .env ]; then
  echo "ERROR: .env not found in $(pwd)." >&2
  exit 1
fi

set -a
source .env
set +a
echo ">>> Loaded .env"

: "${POSTGRES_DB:?ERROR: POSTGRES_DB not set in .env}"
: "${POSTGRES_USER:?ERROR: POSTGRES_USER not set in .env}"
: "${POSTGRES_PASSWORD:?ERROR: POSTGRES_PASSWORD not set in .env}"
: "${POSTGRES_RUN_VOLUME:?ERROR: POSTGRES_RUN_VOLUME not set in .env}"
: "${POSTGRES_GOLDEN_VOLUME:?ERROR: POSTGRES_GOLDEN_VOLUME not set in .env}"

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
  ["django"]="./benchmarks/django_bench"
  ["pony"]="./benchmarks/pony_bench"
  ["sqlalchemy"]="./benchmarks/sqlalchemy_bench"
  ["sql"]="./benchmarks/sql_bench"
)

declare -A MODES_MAP=(
  ["django"]="sync async"
  ["pony"]="sync"
  ["sqlalchemy"]="sync async"
  ["sql"]="sync async"
)

NAME="${1:-}"
MODE="${2:-sync}"
if [ -z "$NAME" ]; then
  echo "Usage: $0 <solution-name>"
  exit 1
fi

CONTEXT="${MAP[$NAME]:-}"
if [ -z "$CONTEXT" ]; then
  echo "ERROR: unknown solution name: '$NAME'. Available: ${!MAP[@]}" >&2
  exit 2
fi

ALLOWED="${MODES_MAP[$NAME]:-sync}"

ok=0
for m in $ALLOWED; do
  if [ "$m" = "$MODE" ]; then
    ok=1
    break
  fi
done

if [ "$ok" -ne 1 ]; then
  echo "ERROR: unknown mode: '$MODE' for solution '$NAME'. Available: $ALLOWED" >&2
  exit 3
fi

export RUNNER_BUILD_CONTEXT="$CONTEXT"
export RUNNER_NAME="$NAME"
export RUNNER_COMMAND="$MODE"

ensure_golden_volume() {
  if docker volume inspect "$POSTGRES_GOLDEN_VOLUME" >/dev/null 2>&1; then
    echo ">>> Golden volume exists: $POSTGRES_GOLDEN_VOLUME"
    return 0
  fi

  echo ">>> Creating golden volume: $POSTGRES_GOLDEN_VOLUME"
  docker volume create "$POSTGRES_GOLDEN_VOLUME" >/dev/null

  echo ">>> Initializing golden DB from image..."
  local init_ctr="init-golden"

  docker rm -f "$init_ctr" >/dev/null 2>&1 || true
  docker run -d --name "$init_ctr" \
    -e POSTGRES_DB="${POSTGRES_DB}" \
    -e POSTGRES_USER="${POSTGRES_USER}" \
    -e POSTGRES_PASSWORD="${POSTGRES_PASSWORD}" \
    -v "$POSTGRES_GOLDEN_VOLUME":/var/lib/postgresql/data:rw \
    denistred/sql-orm-bench-db:latest >/dev/null

  echo ">>> Waiting for restore log line..."

  local ok=0
  for _ in $(seq 1 1200); do
    if docker logs "$init_ctr" 2>&1 | grep -q "Restore finished."; then
      ok=1
      break
    fi
    sleep 1
  done

  if [ "$ok" -ne 1 ]; then
    echo "ERROR: golden init did not confirm restore." >&2
    docker logs "$init_ctr" >&2 || true
    docker stop "$init_ctr" >/dev/null 2>&1 || true
    docker rm "$init_ctr" >/dev/null 2>&1 || true
    exit 4
  fi

  docker stop "$init_ctr" >/dev/null
  docker rm "$init_ctr" >/dev/null

  echo ">>> Golden volume initialized."
}


recreate_run_volume_from_golden() {
  echo ">>> Preparing run volume: $POSTGRES_RUN_VOLUME"

  if docker volume inspect "$POSTGRES_RUN_VOLUME" >/dev/null 2>&1; then
    echo ">>> Removing existing run volume: $POSTGRES_RUN_VOLUME"
    docker volume rm "$POSTGRES_RUN_VOLUME" >/dev/null
  fi

  docker volume create "$POSTGRES_RUN_VOLUME" >/dev/null

  echo ">>> Copying data golden -> run (fast clone)..."
  docker run --rm \
    -v "$POSTGRES_GOLDEN_VOLUME":/from:ro \
    -v "$POSTGRES_RUN_VOLUME":/to:rw \
    alpine:3.20 sh -c \
    "cd /from && tar cf - . | (cd /to && tar xpf -)" >/dev/null

  echo ">>> Run volume populated."
}


echo "Using compose command: $DC"
echo "Starting '$NAME' (mode: $MODE) with context '$CONTEXT' ..."
echo "Golden volume: $POSTGRES_GOLDEN_VOLUME"
echo "Run volume: $POSTGRES_RUN_VOLUME"

ensure_golden_volume
recreate_run_volume_from_golden

$DC -f docker-compose.yaml up -d --build

echo
echo "Done. To follow logs: ./logs.sh"
echo "To stop and remove containers+run volumes: ./stop.sh"

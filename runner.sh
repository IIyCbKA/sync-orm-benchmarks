#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

if [ ! -f .env ]; then
  echo "ERROR: .env not found in $(pwd)." >&2
  exit 1
fi

if [ ! -f docker-compose.yaml ]; then
  echo "ERROR: compose file not found in current dir." >&2
  exit 2
fi
COMPOSE_FILE="docker-compose.yaml"

set -a
source .env
set +a
echo ">>> Loaded .env"

: "${POSTGRES_DB:?ERROR: POSTGRES_DB not set in .env}"
: "${POSTGRES_USER:?ERROR: POSTGRES_USER not set in .env}"
: "${POSTGRES_PASSWORD:?ERROR: POSTGRES_PASSWORD not set in .env}"
: "${POSTGRES_RUN_VOLUME:?ERROR: POSTGRES_RUN_VOLUME not set in .env}"
: "${POSTGRES_GOLDEN_VOLUME:?ERROR: POSTGRES_GOLDEN_VOLUME not set in .env}"

if command -v docker-compose >/dev/null 2>&1; then
  DC=("docker-compose")
elif command -v docker >/dev/null 2>&1 && docker compose version >/dev/null 2>&1; then
  DC=("docker" "compose")
else
  echo "ERROR: neither 'docker-compose' nor 'docker compose' found in PATH." >&2
  exit 1
fi

ALL_ORMS=(django peewee pony sqlalchemy sqlmodel)

CYCLES="${1:-}"

if [ "$#" -lt 1 ]; then
  echo "Usage: $0 <cycles> [orm-name ...]" >&2
  echo "       One cycle runs every ORM one after another, so all of them see" >&2
  echo "       comparable I/O conditions. Without a list the default order is:" >&2
  echo "       ${ALL_ORMS[*]}" >&2
  exit 1
fi

if ! [[ "$CYCLES" =~ ^[1-9][0-9]*$ ]]; then
  echo "ERROR: cycles must be a positive integer, got: '$CYCLES'." >&2
  exit 2
fi

shift

if [ "$#" -gt 0 ]; then
  ORMS=("$@")
else
  ORMS=("${ALL_ORMS[@]}")
fi

for orm in "${ORMS[@]}"; do
  case "$orm" in
    django|peewee|pony|sqlalchemy|sqlmodel) ;;
    *)
      echo "ERROR: unknown ORM name: '$orm'. Available: ${ALL_ORMS[*]}" >&2
      exit 2
      ;;
  esac
done

LOG_FILE="$SCRIPT_DIR/logs.txt"
: > "$LOG_FILE"

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
    -v "$POSTGRES_GOLDEN_VOLUME":/var/lib/postgresql:rw \
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
    exit 3
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

CLEANUP_REQUIRED=0

stop_and_remove() {
  echo ">>> Stopping and removing"
  echo ">>> Command: ${DC[*]} -f $COMPOSE_FILE down -v --remove-orphans"

  "${DC[@]}" -f "$COMPOSE_FILE" down -v --remove-orphans
  CLEANUP_REQUIRED=0

  echo ">>> Done: containers, networks and declared volumes removed."
}

cleanup_on_exit() {
  local status=$?
  trap - EXIT

  if [ "$CLEANUP_REQUIRED" -eq 1 ]; then
    echo ">>> Cleaning up after interrupted or failed iteration..." >&2
    "${DC[@]}" -f "$COMPOSE_FILE" down -v --remove-orphans || true
  fi

  exit "$status"
}

trap cleanup_on_exit EXIT
trap 'exit 130' INT
trap 'exit 143' TERM

echo "Using compose command: ${DC[*]}"
echo "Running $CYCLES cycle(s) over: ${ORMS[*]}"
echo "Golden volume: $POSTGRES_GOLDEN_VOLUME"
echo "Run volume: $POSTGRES_RUN_VOLUME"
echo "Log file: $LOG_FILE"

ensure_golden_volume

for ((iteration = 1; iteration <= CYCLES; iteration++)); do
  echo
  echo ">>> Iteration $iteration of $CYCLES"

  if [ "$iteration" -gt 1 ]; then
    printf '\n' >> "$LOG_FILE"
  fi
  printf 'iteration %d\n' "$iteration" | tee -a "$LOG_FILE"

  for orm in "${ORMS[@]}"; do
    echo
    echo ">>> [$iteration/$CYCLES] $orm"

    # Every ORM starts from an identical copy of the golden database.
    export RUNNER_DOCKERFILE="benchmarks/${orm}_bench/Dockerfile"

    CLEANUP_REQUIRED=1
    recreate_run_volume_from_golden

    "${DC[@]}" -f "$COMPOSE_FILE" up -d --build

    echo ">>> Following logs for runner service..."
    "${DC[@]}" -f "$COMPOSE_FILE" logs -f runner 2>&1 | tee -a "$LOG_FILE"

    stop_and_remove
  done
done

echo
echo ">>> Completed $CYCLES cycle(s). Logs saved to $LOG_FILE"
# ─────────────────────────────── Build ────────────────────────────────────────
FROM python:3.12-slim-bookworm AS builder

ENV PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends  \
      build-essential  \
      libpq-dev && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --upgrade pip && \
    pip wheel --no-cache-dir --wheel-dir /wheels -r requirements.txt && \


# ─────────────────────────────── Runtime ──────────────────────────────────────
FROM python:3.12-slim-bookworm

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      libpq5 && \
    rm -rf /var/lib/apt/lists/*

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY --from=builder /wheels /wheels
COPY requirements.txt ./
RUN pip install --no-cache-dir --no-index --find-links /wheels \
      -r requirements.txt && \
    rm -rf /wheels

COPY . .

RUN printf '%s\n' '#!/bin/sh' \
    'set -e' \
    '' \
    'exec ./run-tests.sh' > /entrypoint.sh \
&& chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
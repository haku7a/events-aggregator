FROM python:3.12-slim AS builder

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-install-project --no-dev

FROM python:3.12-slim

RUN addgroup --system --gid 1000 appuser && \
    adduser --system --uid 1000 --ingroup appuser appuser

WORKDIR /app

COPY --from=builder /app/.venv /app/.venv

COPY --chown=appuser:appuser app/ ./app/

ENV PATH="/app/.venv/bin:$PATH"

USER appuser

CMD ["python", "app/main.py"]


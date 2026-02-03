# syntax=docker/dockerfile:1
FROM python:3.12-slim AS build

# Copy uv binary dari official image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Environment variables penting
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy

# Copy dependency files dulu untuk layer caching
COPY pyproject.toml uv.lock ./

# Install dependencies dengan cache mount
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev

# Copy application code
COPY . .

# Install project
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# Runtime stage - image lebih kecil
FROM python:3.12-slim

# Create non-root user untuk security
RUN useradd -m -u 1000 app && \
    mkdir -p /app && \
    chown -R app:app /app

WORKDIR /app

# Copy virtual environment dan app dari build stage
COPY --from=build --chown=app:app /app /app

# Activate virtual environment
ENV PATH="/app/.venv/bin:$PATH"

USER app

CMD ["python", "-m", "app.main"]

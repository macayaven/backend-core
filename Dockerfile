# syntax=docker/dockerfile:1

# Base image with Python and Poetry
FROM python:3.12-slim AS python-base

# Python/Poetry environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.7.1 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"

# Add Poetry and venv to PATH
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

# Builder image
FROM python-base AS builder

# Install system dependencies
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Set up working directory
WORKDIR $PYSETUP_PATH

# Copy dependency files
COPY poetry.lock pyproject.toml ./

# Install dependencies
RUN poetry install --no-root --only main

# Copy application code
COPY backend_core ./backend_core
COPY alembic.ini ./

# Development image
FROM builder AS development

# Set development environment
ENV FASTAPI_ENV=development \
    PYTHONPATH=/opt/pysetup

# Install development dependencies
RUN poetry install --no-root && \
    poetry run pip install pytest pytest-cov

# Copy development files
COPY . .

# Verify pytest installation
RUN poetry run python -m pytest --version

# Production image
FROM python-base AS production

# Set production environment
ENV FASTAPI_ENV=production

# Copy only what's needed from builder
COPY --from=builder $PYSETUP_PATH/.venv $PYSETUP_PATH/.venv
COPY --from=builder $PYSETUP_PATH/backend_core $PYSETUP_PATH/backend_core
COPY --from=builder $PYSETUP_PATH/alembic.ini ./

# Set working directory
WORKDIR $PYSETUP_PATH

# Create and switch to non-root user
RUN useradd -m -u 1000 appuser \
    && chown -R appuser:appuser $PYSETUP_PATH

USER appuser

# Start command
CMD ["uvicorn", "backend_core.main:app", "--host", "0.0.0.0", "--port", "8000"]

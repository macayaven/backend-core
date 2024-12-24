# syntax=docker/dockerfile:1

# Base image with Python and Poetry
FROM python:3.12-slim

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
    PYSETUP_PATH="/app" \
    VENV_PATH="/app/.venv" \
    DOCKER_CONTAINER=1

# Add Poetry and venv to PATH
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

# Set up working directory
WORKDIR $PYSETUP_PATH

# Install system dependencies and Poetry
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/* \
    && curl -sSL https://install.python-poetry.org | python3 -

# Copy dependency files
COPY pyproject.toml poetry.lock ./

# Install all dependencies including test dependencies
RUN poetry install --no-root

# Copy application code
COPY backend_core backend_core/
COPY alembic alembic/
COPY alembic.ini ./
COPY tests tests/
COPY tasks.py ./

# Install the project itself
RUN poetry install

# Start command
ENTRYPOINT ["poetry", "run"]
CMD ["uvicorn", "backend_core.main:app", "--host", "0.0.0.0", "--port", "8000"]

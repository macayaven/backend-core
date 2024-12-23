FROM python:3.12-slim AS base

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.8.2

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

# Set working directory
WORKDIR /app

# Copy dependency files
COPY poetry.lock pyproject.toml /app/

# Define build argument for environment
ARG TARGET=production

# Install dependencies with Poetry
RUN poetry config virtualenvs.create false \
    && if [ "$TARGET" = "production" ]; then \
        poetry install --no-dev --no-interaction --no-ansi; \
    else \
        poetry install --no-interaction --no-ansi; \
    fi

# Copy application code
COPY . /app

# Create a non-root user and group
RUN groupadd app && useradd -m -g app appuser

# Adjust file permissions
RUN chown -R appuser:app /app
USER appuser

# Expose application port
EXPOSE 8000

# Set default command
CMD ["uvicorn", "backend_core.main:app", "--host", "0.0.0.0", "--port", "8000"]
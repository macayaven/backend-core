"""Docker-related tasks."""

import time
from typing import Optional

from invoke.context import Context
from invoke.runners import Result

from tasks_modules.common import task as invoke_task


@invoke_task
def build_docker(c: Context, target: str = "production", tag: str = "latest") -> None:
    """
    Build Docker images for the specified target.

    Args:
        c (Context): Invoke context.
        target (str): Target to build ('production' or 'development').
        tag (str): Tag for the Docker image.
    """
    clean_docker(c)

    # Build with appropriate target and tag
    c.run(
        f"docker build --target {target} " f"-t macayaven/backend-core:{tag}-{target} " f"--build-arg TARGET={target} ."
    )


@invoke_task
def push_docker(c: Context, target: str = "production", tag: str = "latest") -> None:
    """
    Push Docker image to registry.

    Args:
        c (Context): Invoke context.
        target (str): Target to push ('production' or 'development').
        tag (str): Tag for the Docker image.
    """
    # Push the image to registry
    c.run(f"docker push macayaven/backend-core:{tag}-{target}")


@invoke_task
def up_docker(c: Context, target: str = "development") -> None:
    """
    Start Docker containers.

    Args:
        c (Context): Invoke context.
        target (str): Target to run ('production' or 'development').
    """
    # Build if needed
    build_docker(c, target=target)
    c.run(f"TARGET={target} docker compose up -d")


@invoke_task
def down_docker(c: Context) -> None:
    """Stop Docker containers."""
    c.run("docker compose down --remove-orphans")


@invoke_task
def logs_docker(c: Context) -> None:
    """View Docker container logs."""
    c.run("docker compose logs -f")


@invoke_task
def test_docker(c: Context) -> None:
    """Run tests inside Docker container."""
    # Build development image
    build_docker(c, target="development")

    # Run tests using poetry in development image with Docker-specific database host
    c.run(
        "docker compose run --rm "
        "-e DOCKER_POSTGRES_SERVER=postgres "  # Set Docker-specific database host
        "-e ENV_FILE=.env.test "  # Use test environment file
        "backend bash -c '"
        "poetry install --no-root && "
        "poetry run pytest tests/ "
        "--cov=backend_core --cov-report=xml --cov-report=html "
        "--cov-fail-under=80 --junitxml=pytest.xml'"
    )


@invoke_task
def restart_docker(c: Context, target: str = "development") -> None:
    """
    Restart Docker containers.

    Args:
        c (Context): Invoke context.
        target (str): Target to run ('production' or 'development').
    """
    down_docker(c)
    up_docker(c, target=target)


@invoke_task
def up_db(c: Context) -> None:
    """Start only the database container and wait until it's healthy."""
    # Start the database container
    c.run("docker compose up -d postgres")

    # Wait for the database to be ready
    max_retries = 30
    retry_interval = 1  # seconds

    for _ in range(max_retries):
        try:
            # Check if the container is healthy
            result: Optional[Result] = c.run("docker compose ps postgres", hide=True)
            if result is not None and "healthy" in result.stdout:
                print("Database is ready!")
                return
        except Exception:
            pass

        print("Waiting for database to be ready...")
        time.sleep(retry_interval)

    raise Exception("Database failed to become ready in time")


@invoke_task
def down_db(c: Context) -> None:
    """Stop the database container."""
    c.run("docker compose stop postgres")
    c.run("docker compose rm -f postgres")


@invoke_task
def clean_docker(c: Context) -> None:
    """Clean up Docker containers and images."""
    c.run("docker compose down --remove-orphans")
    c.run("docker builder prune -f")

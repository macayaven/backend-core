from invoke.context import Context

from tasks_modules.common import task
from tasks_modules.docker import down_db, up_db


@task
def test(c: Context, docker: bool = False) -> None:
    """Run tests either locally or in Docker.

    Args:
        docker (bool): If True, run tests in Docker container
    """
    if docker:
        test_docker(c)
        return

    # Start the postgres service
    down_db(c)
    up_db(c)

    try:
        # Run the tests
        c.run(
            "poetry run pytest tests/ --cov=backend_core --cov-report=xml \
              --cov-report=html --cov-fail-under=80 --junitxml=pytest.xml"
        )
    finally:
        # Stop the postgres service
        down_db(c)


@task
def test_docker(c: Context) -> None:
    """Run tests in Docker container."""
    # Build development image if needed
    c.run("docker compose build --build-arg TARGET=development")

    # Run tests in container
    c.run(
        "docker compose run --rm api pytest tests/ --cov=backend_core \
          --cov-report=xml --cov-report=html --cov-fail-under=80 \
          --junitxml=pytest.xml"
    )

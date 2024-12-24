# backend_core/tasks.py
"""Tasks for invoke command line utility."""
import os
import shutil
from pathlib import Path

from invoke import Context, Result, task


@task
def install(ctx: Context) -> None:
    """Install project dependencies using Poetry."""
    print("Installing project dependencies...")
    ctx.run("poetry lock --no-update", warn=True)
    ctx.run("poetry install")


@task
def format(ctx: Context) -> None:
    """Format code using black and isort."""
    ctx.run("black .")
    ctx.run("isort .")


@task
def check_format(ctx: Context) -> None:
    """Check code formatting without making changes."""
    print("Checking code formatting...")
    ctx.run("black --check .")
    ctx.run("isort --check-only .")


@task
def lint(ctx: Context) -> None:
    """Run linting tools."""
    ctx.run("ruff check .")
    ctx.run("mypy .")


@task
def check(ctx: Context) -> None:
    """Run all code quality checks."""
    check_format(ctx)
    lint(ctx)


@task
def test(ctx: Context) -> None:
    """Run tests."""
    if os.environ.get("DOCKER_CONTAINER"):
        # Inside Docker, run pytest directly
        ctx.run("pytest tests/ -v --cov=backend_core --cov-report=xml")
    else:
        # Outside Docker, use docker-compose
        # First ensure the db service is up and healthy
        ctx.run("docker compose up -d db")
        # Wait for db to be healthy using docker compose
        wait_script = """
from time import sleep
from backend_core.db.utils import verify_database
while not verify_database():
    sleep(1)
"""
        ctx.run(f"docker compose run --rm api python -c '{wait_script}'")
        # Run the tests
        ctx.run("docker compose run --rm api poetry run pytest tests/ -v --cov=backend_core --cov-report=xml")


@task
def clean(ctx: Context) -> None:
    """Remove all build artifacts, temporary files, and docker resources."""
    # List of patterns to remove
    patterns = [
        ".venv",
        ".coverage",
        ".pytest_cache",
        ".mypy_cache",
        ".ruff_cache",
        "**/__pycache__",
        "**/*.pyc",
        "**/*.pyo",
        "**/*.pyd",
        "**/.DS_Store",
    ]

    print("Cleaning temporary files...")
    root = Path(".")
    for pattern in patterns:
        for path in root.glob(pattern):
            if path.is_file():
                path.unlink()
            elif path.is_dir():
                shutil.rmtree(path)

    print("\nCleaning Docker resources...")

    # Stop all containers
    ctx.run("docker compose down", warn=True)

    # Get project name from docker-compose
    project_name = Path.cwd().name.lower()

    # Find and remove project containers
    result: Result = ctx.run("docker ps -a --format '{{.Names}}'", hide=True, warn=True)  # type: ignore
    if result and result.ok:
        containers = result.stdout.splitlines()
        project_containers = [c for c in containers if project_name in c.lower()]
        if project_containers:
            print("Removing project containers...")
            ctx.run(f"docker rm -f {' '.join(project_containers)}", warn=True)

    # Find and remove project images
    result = ctx.run("docker images --format '{{.Repository}}:{{.Tag}}'", hide=True, warn=True)  # type: ignore
    if result and result.ok:
        images = result.stdout.splitlines()
        project_images = [i for i in images if project_name in i.lower()]
        if project_images:
            print("Removing project images...")
            ctx.run(f"docker rmi -f {' '.join(project_images)}", warn=True)

    # Find and remove project volumes
    result = ctx.run("docker volume ls --format '{{.Name}}'", hide=True, warn=True)  # type: ignore
    if result and result.ok:
        volumes = result.stdout.splitlines()
        project_volumes = [v for v in volumes if project_name in v.lower()]
        if project_volumes:
            print("Removing project volumes...")
            ctx.run(f"docker volume rm -f {' '.join(project_volumes)}", warn=True)

    # Find and remove project networks
    result = ctx.run("docker network ls --format '{{.Name}}'", hide=True, warn=True)  # type: ignore
    if result and result.ok:
        networks = result.stdout.splitlines()
        project_networks = [n for n in networks if project_name in n.lower() and n != "bridge" and n != "host"]
        if project_networks:
            print("Removing project networks...")
            ctx.run(f"docker network rm {' '.join(project_networks)}", warn=True)

    print("\nCleanup complete!")

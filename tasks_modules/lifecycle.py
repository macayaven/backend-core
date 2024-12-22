from invoke.context import Context

from tasks_modules.common import task
from tasks_modules.docker import clean_docker


@task
def uninstall(c: Context) -> None:
    """
    Clean build artifacts, caches, and virtual environments.

    Args:
        c (Context): Invoke context.
    """
    print("Cleaning up build artifacts, caches, and virtual environments...")

    # Remove standard build and Python cache directories/files
    c.run("rm -rf build/ dist/ *.egg-info .mypy_cache poetry.lock .venv .pytest_cache .ruff_cache htmlcov .coverage")

    # Find and remove Python bytecode files and cache directories
    c.run("find . -type d -name '__pycache__' -exec rm -rf {} +")
    c.run("find . -type f -name '*.pyc' -delete")
    c.run("find . -type f -name '*.pyo' -delete")

    # Remove Docker-related artifacts and containers
    clean_docker(c)

    # Optional: Clean up `.tox` if you are using Tox for testing
    c.run("rm -rf .tox")

    # Optional: Clean up generated Sphinx documentation if applicable
    c.run("rm -rf docs/_build")

    print("Cleanup complete!")


@task
def install(c: Context) -> None:
    """
    Clean the environment and install dependencies using Poetry.

    Args:
        c (Context): Invoke context.
    """
    print("Installing dependencies with Poetry...")
    uninstall(c)
    c.run("poetry install")
    print("Installation complete!")

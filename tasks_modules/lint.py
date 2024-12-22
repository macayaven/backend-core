from invoke.context import Context

from tasks_modules.common import task


@task
def lint(c: Context) -> None:
    """Run linting checks."""
    c.run("poetry run mypy . --config-file pyproject.toml")


@task
def format(c: Context) -> None:
    """Format code."""
    c.run("poetry run black .")
    c.run("poetry run isort .")
    c.run("poetry run ruff check . --fix")

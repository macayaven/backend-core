from invoke.context import Context

from tasks_modules.common import task


@task
def check_format(c: Context) -> None:
    """Check code formatting without modifying files."""
    # Check for unused imports
    c.run("poetry run autoflake --check --recursive .", warn=True)
    # Check import sorting
    c.run("poetry run isort --check-only --diff .", warn=True)
    # Check code formatting
    c.run("poetry run black --check --diff .", warn=True)


@task
def format(c: Context) -> None:
    """Format code using black, isort, and autoflake."""
    # Remove unused imports
    c.run("poetry run autoflake --in-place --recursive --remove-all-unused-imports .")
    # Sort imports
    c.run("poetry run isort .")
    # Format code
    c.run("poetry run black .")

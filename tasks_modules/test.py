from invoke.context import Context

from tasks_modules.common import task
from tasks_modules.docker import down_db, up_db


@task
def test(c: Context) -> None:
    """Run tests."""

    # Start the postgres service
    up_db(c)

    try:
        # Run the tests
        c.run("poetry run pytest tests/")
    finally:
        # Stop the postgres service
        down_db(c)

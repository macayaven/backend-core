import time

from invoke.context import Context

from tasks_modules.common import task as invoke_task


@invoke_task
def build_docker(c: Context, target: str = "production") -> None:
    """
    Build Docker images for the specified target.

    Args:
        c (Context): Invoke context.
        target (str): Target to build ('production' or 'development').
    """
    clean_docker(c)
    c.run(f"docker compose build --build-arg TARGET={target}")


@invoke_task
def up_docker(c: Context) -> None:
    """
    Start Docker containers.

    Args:
        c (Context): Invoke context.
    """
    c.run("docker compose up -d")


@invoke_task
def down_docker(c: Context) -> None:
    """
    Stop Docker containers.

    Args:
        c (Context): Invoke context.
    """
    c.run("docker compose down")


@invoke_task
def logs_docker(c: Context) -> None:
    """
    View Docker container logs.

    Args:
        c (Context): Invoke context.
    """
    c.run("docker compose logs -f")


@invoke_task
def test_docker(c: Context) -> None:
    """
    Run tests inside the Docker container targeted for development.
    """
    # Set built target
    build_docker(c, target="development")
    down_docker(c)

    # Run the backend service in test mode
    c.run("docker compose run --rm --user $(id -u):$(id -g) backend sh -c 'POSTGRES_SERVER=postgres pytest'")

    # Optionally bring down the containers after tests
    down_docker(c)


@invoke_task
def restart_docker(c: Context) -> None:
    """
    Restart Docker containers.

    Args:
        c (Context): Invoke context.
    """
    down_docker(c)
    up_docker(c)


@invoke_task
def up_db(c: Context) -> None:
    """
    Start only the database container and wait until it's healthy.

    Args:
        c (Context): Invoke context.
    """
    # Start the PostgreSQL container
    c.run("docker compose up -d postgres")

    # Wait for the PostgreSQL container to become healthy
    while True:
        result = c.run(
            "docker inspect -f '{{ .State.Health.Status }}' $(docker compose ps -q postgres)",
            hide=True,
            warn=True,
        )
        if result and result.stdout:
            status = result.stdout.strip()
        else:
            raise RuntimeError("Failed to inspect PostgreSQL container status.")

        if status == "healthy":
            print("PostgreSQL is healthy!")
            break
        elif status == "unhealthy":
            raise RuntimeError("PostgreSQL failed to become healthy.")
        else:
            print(f"PostgreSQL status: {status}. Waiting...")
            time.sleep(2)


@invoke_task
def down_db(c: Context) -> None:
    """
    Stop the database container.

    Args:
        c (Context): Invoke context.
    """
    c.run("docker compose down postgres")


@invoke_task
def clean_docker(c: Context) -> None:
    """
    Clean up Docker containers and images.

    Args:
        c (Context): Invoke context.
    """
    c.run("docker compose down --remove-orphans")
    c.run("docker compose down -v --rmi all --remove-orphans")

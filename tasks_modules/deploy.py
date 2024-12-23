from invoke import Context, task


@task
def deploy(ctx: Context) -> None:
    """Deploy the application to production"""
    # Build and tag the Docker image
    ctx.run("docker build -t macayaven/backend-core:latest .")

    # Push to Docker Hub
    ctx.run("docker push macayaven/backend-core:latest")

    # Deploy using docker-compose
    with ctx.cd("/opt/backend-core"):
        ctx.run("docker compose pull")
        ctx.run("docker compose down")
        ctx.run("docker compose up -d")
        ctx.run("docker system prune -f")


@task
def rollback(ctx: Context, version: str) -> None:
    """Rollback to a specific version

    Args:
        version: The version to rollback to (e.g., v1.0.0)
    """
    # Pull the specified version
    ctx.run(f"docker pull macayaven/backend-core:{version}")

    # Deploy the old version
    with ctx.cd("/opt/backend-core"):
        ctx.run("docker compose down")
        ctx.run(f'echo "IMAGE_TAG={version}" > .env')
        ctx.run("docker compose up -d")
        ctx.run("docker system prune -f")

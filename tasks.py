# tasks.py
from invoke import Collection

from tasks_modules.docker import build_docker, clean_docker, down_docker, logs_docker, test_docker, up_db, up_docker
from tasks_modules.format import check_format, format
from tasks_modules.lint import lint
from tasks_modules.test import test

# Create collections
docker = Collection("docker")
docker.add_task(build_docker, "build")
docker.add_task(clean_docker, "clean")
docker.add_task(up_docker, "up")
docker.add_task(down_docker, "down")
docker.add_task(logs_docker, "logs")
docker.add_task(test_docker, "test")
docker.add_task(up_db, "up-db")

# Create namespace
ns = Collection()
ns.add_collection(docker)

# Add standalone tasks
ns.add_task(format, "format")
ns.add_task(check_format, "check-format")
ns.add_task(lint, "lint")
ns.add_task(test, "test")

# tasks.py
from invoke import Collection

from tasks_modules import (
    build_docker,
    clean_docker,
    down_docker,
    format,
    install,
    lint,
    logs_docker,
    test,
    test_docker,
    uninstall,
    up_docker,
    check_format,
)

# Create the root namespace
ns = Collection()

# Add all tasks to the namespace
ns.add_task(install)
ns.add_task(uninstall)
ns.add_task(format)
ns.add_task(check_format)
ns.add_task(lint)
ns.add_task(test)
ns.add_task(test_docker)
ns.add_task(up_docker)
ns.add_task(down_docker)
ns.add_task(logs_docker)
ns.add_task(build_docker)
ns.add_task(clean_docker)

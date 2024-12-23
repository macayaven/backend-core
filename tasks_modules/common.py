from functools import wraps
from typing import Any, Callable, TypeVar

from invoke import Task

F = TypeVar("F", bound=Callable[..., Any])


def task(func: F) -> Task:
    """Wrap invoke.task to preserve type information."""

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        return func(*args, **kwargs)

    return Task(wrapper)

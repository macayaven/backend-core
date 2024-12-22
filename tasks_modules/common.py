from typing import Callable, TypeVar

from invoke import Task
from invoke import task as _task
from typing_extensions import ParamSpec

P = ParamSpec("P")
R = TypeVar("R")


def task(f: Callable[P, R]) -> Task[Callable[P, R]]:
    """Type-annotated wrapper for invoke's task decorator."""
    return _task(f)  # type: ignore[return-value]

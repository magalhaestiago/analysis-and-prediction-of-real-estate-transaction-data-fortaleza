from collections.abc import Callable
from functools import wraps
from typing import Any

from document_relayout.core.backend.types.box import Box


def postprocess(steps: list[Callable[[list[Box]], list[Box]]]):
    def apply_steps(func: Callable[[Any], list[Box]]):
        @wraps(func)
        def wrapper(*args, **kwargs):
            boxes = func(*args, **kwargs)

            for step in steps:
                boxes = step(boxes)
            return boxes

        return wrapper

    return apply_steps

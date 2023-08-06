import os
from contextlib import contextmanager
from typing import Generator, Union, Type, TypeVar
import shutil

import pytest

PathLike = Union[str, "os.PathLike[str]"]


ErrSubclass = TypeVar("ErrSubclass", bound=BaseException)


@contextmanager
def raises(error_class: Type[ErrSubclass], message: str) -> Generator[None, None, None]:
    try:
        yield
    except error_class:
        pass
    else:
        pytest.fail(message)


def require_tool(name: str) -> None:
    if shutil.which(name) is None:
        pytest.skip(f"tool {name} not found in PATH")

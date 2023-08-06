import os
from . import PathLike


def access(
    path: PathLike,
    mode: int,
) -> bool:
    """
    This function exists so that we can monkeypatch this and unittest mount_workdir.
    """
    return os.access(
        path,
        mode,
    )

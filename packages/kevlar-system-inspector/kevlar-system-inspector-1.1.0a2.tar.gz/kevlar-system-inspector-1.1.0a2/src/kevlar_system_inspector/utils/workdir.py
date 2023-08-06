from contextlib import contextmanager
import os
from pathlib import Path
import tempfile
import textwrap
from typing import Generator, List, ContextManager
import warnings

import pytest

from . import PathLike
from .mount import get_mountinfo, mount, umount, MNT_DETACH, MountEntry
from .access import access


@contextmanager
def get_workdir(
    tmp_path_factory: "pytest.TempPathFactory",
) -> Generator[Path, None, None]:
    """Create a working directory:

    1) Writable
    2) Not no-exec
    3) Not nodev

    """

    candidate_paths: List[PathLike] = [
        tmp_path_factory.getbasetemp(),
        tempfile.gettempdir(),
        "/tmp",
        "/dev/shm",
        "/run",
    ]

    def is_valid(path: PathLike, mountinfo: MountEntry) -> bool:
        if "ro" in mountinfo.options:
            return False
        if "noexec" in mountinfo.options:
            return False
        if "nodev" in mountinfo.options:
            return False

        # check DAC/MAC
        if not os.access(path, os.W_OK):
            return False
        return True

    workdir: ContextManager[PathLike]
    for path in candidate_paths:
        info = get_mountinfo(path)
        if info is None:
            continue
        if is_valid(path, info):
            workdir = tempfile.TemporaryDirectory(dir=path)
            break
    else:
        workdir = mount_workdir()

    with workdir as dir_name:
        yield Path(dir_name)


@contextmanager
def mount_workdir() -> Generator[str, None, None]:
    mounted = True
    try:
        tmpdir = tempfile.TemporaryDirectory()
        try:
            mount("tmpfs", tmpdir.name, "tmpfs", 0, None)
        except OSError as e:
            if access(tmpdir.name, os.W_OK):
                # If we fail to mount but our tmpdir creation succeeded and we
                # can write then continue. We might be under allowlisting
                # so mount may not succeed.
                mounted = False
                pass
            else:
                # We will need to write to this temp dir so we should fail now
                raise e
    except OSError:
        # Don't give them a clean bill of health: spit out a warning. Note that
        # even if we are run as a regular user or in a very locked down read-only
        # system, it would be still possible to enter into a user/mount namespace
        # to make a tmpfs. So we can still try harder if we need to.
        warnings.warn(
            textwrap.dedent(
                """\
            Could not run allowlisting tests, likely because we were not run as root.
            """
            )
        )
        pytest.skip("Could not set up workdir")

    with tmpdir:
        try:
            yield tmpdir.name
        finally:
            if mounted:
                umount(tmpdir.name, MNT_DETACH)

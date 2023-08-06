"""
------------------------
Application Allowlisting
------------------------

An immutable system should not allow the introduction of new code, even by a
root user. The technique of denying the execution of code that was not
originally part of the system is called application allowlisting.

For more information, see :kevlar-code:`200`.
"""

import warnings
import shutil
import os
import subprocess
from pathlib import Path
import errno
import glob
import re
import stat
from typing import Optional

import pytest

from .utils.elf import ELF, ELFError
from .utils import raises
from .decorators import full_version_only, merge_tests


def copy_elf(src: Path, dst: Path) -> Path:
    shutil.copy2(src, dst, follow_symlinks=True)
    ELF(dst)  # raise ELFError if it's not an ELF
    return Path(dst)


def resolve_system_lib(lib_name: str) -> Optional[Path]:
    paths = ["/lib", "/lib64", "/lib/*", "/usr/lib", "/usr/lib64", "/usr/lib/*"]
    for path in paths:
        pattern = os.path.join(path, lib_name)
        files = glob.glob(pattern)
        for file in files:
            # On a development machine, we might find both
            # /usr/lib/x86_64-linux-gnu/<lib> and
            # /usr/lib/aarch64-linux-gnu/<lib>, where the latter is for cross
            # compiling.
            try:
                elf = ELF(file)
                if elf.is_native():
                    return Path(file)
            except ELFError:
                pass
    return None


@pytest.fixture
def cat(workdir: Path) -> Path:
    """A cat-like non-system binary"""
    exename = "cat"
    exepath = shutil.which(exename)
    if not exepath:
        warnings.warn(f"Could not find ``{exename}`` on this system for testing.")
        pytest.skip()

    src = Path(exepath)
    dst = workdir / exename

    try:
        return copy_elf(src, dst)
        if not (os.stat(dst).st_mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)):
            raise PermissionError(errno.EPERM, "Copy has wrong DAC permissions")
    except (OSError, ELFError) as e:
        warnings.warn("Could not copy suitable ELF binary for testing.")
        pytest.skip(str(e))


@pytest.fixture
def dynamic_cat(cat: Path) -> Path:
    """Ensure that 'cat' is dynamically linked."""
    elf = ELF(cat)
    if not elf.libraries():
        warnings.warn("Could not find suitable dynamically-lined binary for testing.")
        pytest.skip()
    return cat


@pytest.fixture
def libc(workdir: Path, cat: Path) -> Path:
    """A copy of libc in a non-system location"""

    # find it by examining the binary
    elf = ELF(cat)
    libs = elf.libraries()
    for lib in libs:
        if re.match(r"libc(\..*)?\.so(\..*)?$", lib):
            libc_name = lib
            break
    else:
        warnings.warn(
            f"Could not determine suitable library for testing. (Is {cat} statically linked?)"
        )
        pytest.skip()

    libc_src = resolve_system_lib(libc_name)
    if libc_src is None:
        warnings.warn(f"Could not resovle {libc_name} for testing on this system.")
        pytest.skip()

    libc_dst = workdir / libc_name
    try:
        return copy_elf(libc_src, libc_dst)
    except (OSError, ELFError) as e:
        warnings.warn("Could not copy suitable ELF library for testing.")
        pytest.skip(str(e))

    return libc_dst


@merge_tests
class TestRunUnauthorizedBinary:
    """
    Attackers should not be able to introduce and execute binaries on a running system.
    ===================================================================================

    Only authorized binaries should be able to execute.
    """

    def test_attempt_to_run_unauthorized_binary(self, cat: Path) -> None:
        with raises(PermissionError, "An unauthorized binary was able to run."):
            subprocess.run([cat], stdin=subprocess.DEVNULL)

    @full_version_only
    def test_attempt_to_run_new_binary(self) -> None:
        ...


def test_attempt_to_run_unauthorized_copied_binary(cat: Path) -> None:
    """
    Attackers should not able able to execute a copied binary.
    ==========================================================

    Copied binaries should not be authorized to execute.
    """

    with raises(PermissionError, "An unauthorized copied binary was able to run."):
        subprocess.run([cat], stdin=subprocess.DEVNULL)


@full_version_only
def test_attempt_to_load_library(libc: Path) -> None:
    """
    Attackers should not be able to introduce shared libraries.
    ===========================================================

    Only authorized shared libraries should be loadable.
    """
    ...


@full_version_only
def test_inject_via_env_var(dynamic_cat: Path, libc: Path, workdir: Path) -> None:
    """
    Attackers should not be able to inject code with environment variables.
    =======================================================================

    Environment variables should not facilitate injecting of arbitrary code
    into a process.
    """
    ...


@full_version_only
def test_attempt_to_overwrite_system_binary() -> None:
    """
    Attackers should not be able to modify protected locations.
    ===========================================================

    Locations such as /bin or /etc that can influence system execution or
    integrity should be read-only, even as root.
    """
    ...

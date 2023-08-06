# Call modules, potentially with low level commands

import subprocess
import shutil
from typing import List, Any
import warnings

from . import PathLike


def _run_kmod(
    cmdline: List[PathLike], **kwargs: Any
) -> "subprocess.CompletedProcess[Any]":
    utility = cmdline[0]

    exe = shutil.which(utility) or "kmod"
    try:
        return subprocess.run(cmdline, executable=exe, **kwargs)
    except FileNotFoundError:
        # Mimic shell return code for not found
        return subprocess.CompletedProcess(cmdline, 127)
    except OSError:
        # Is a directory, permission denied
        return subprocess.CompletedProcess(cmdline, 126)


def run_kmod(
    cmdline: List[PathLike], **kwargs: Any
) -> "subprocess.CompletedProcess[Any]":
    check = kwargs.pop("check", False)
    result = _run_kmod(cmdline, **kwargs)
    if check:
        result.check_returncode()
    return result


def modules_disabled() -> bool:
    modules_file = "/proc/sys/kernel/modules_disabled"
    try:
        with open(modules_file, "r") as fp:
            return bool(int(fp.read()))
    except FileNotFoundError:
        return True  # Not enabled in the kernel
    except OSError as e:
        warnings.warn(
            f"Could not open {modules_file} to determine module loading status: {e}"
        )
        return False  # Probably not enabled
    except ValueError as e:
        # Should be 0 or 1 only...but take "0" to be the only 'off' value
        warnings.warn(
            f"Could not parse {modules_file} to determine module loading status: {e}"
        )
        return True

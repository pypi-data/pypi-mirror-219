"""
---------------------
Application Integrity
---------------------

Attackers will often attempt to introduce malicious code on a system before the
system runs. This approach means that the attacker does not have to contend
with runtime protections. Application Integrity is a security layer for
preventing this offline tampering.

See :kevlar-code:`500`
"""

from typing import Dict
from dataclasses import dataclass
import subprocess
import os
import re

import pytest


@dataclass(frozen=True)
class BlockDevInfo:
    has_encryption: bool
    has_integrity: bool


def get_str_device(dev: int) -> str:
    major = os.major(dev)
    minor = os.minor(dev)
    return f"{major}:{minor}"


def get_mapper_devices() -> Dict[str, str]:
    root = "/dev/mapper"
    mapper_devices = {}
    for name in os.listdir(root):
        path = os.path.join(root, name)
        info = os.stat(path)
        dev = get_str_device(info.st_rdev)
        mapper_devices[dev] = name
    return mapper_devices


def inspect_mountpoint(path: str) -> BlockDevInfo:
    has_encryption = False
    has_integrity = False

    info = os.stat(path)
    mapper_devs = get_mapper_devices()
    devices = [get_str_device(info.st_dev)]

    while devices:
        device = devices.pop()
        if device not in mapper_devs:
            continue

        name = mapper_devs[device]

        try:
            table = subprocess.run(
                ["dmsetup", "table", name],
                check=True,
                text=True,
                stdout=subprocess.PIPE,
            ).stdout
        except (OSError, subprocess.CalledProcessError):
            pytest.fail(f"Cannot run dmsetup to inspect device {name}.")

        _start, _end, kind, *fields = table.split()
        if kind in ("verity", "integrity"):
            has_integrity = True
        elif kind == "crypt":
            has_encryption = True

        # Rather than try to understand all of the various tables, like raid or
        # dm-crypt, we will just scan for things that look like devices.
        for field in fields:
            if re.fullmatch(r"\d{1,3}:\d{1,3}", field):
                devices.append(field)

    return BlockDevInfo(has_encryption=has_encryption, has_integrity=has_integrity)


def test_root_filesystem_has_integrity() -> None:
    """
    The root filesystem should be protected at the block level from offline modification.
    =====================================================================================

    The integrity of system binaries and configuration files in the root
    filesystem should be evaluated using the stronger block-based scheme vs a
    file-based scheme.
    """

    info = inspect_mountpoint("/")
    assert (
        info.has_integrity
    ), "Root file system is unprotected from offline modification at the block level."

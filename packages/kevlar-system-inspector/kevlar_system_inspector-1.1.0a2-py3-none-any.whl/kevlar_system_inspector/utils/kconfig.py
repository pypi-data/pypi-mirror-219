import gzip
from typing import Set, Optional, TextIO, List, Union
import shlex
import os
import re
import warnings
import subprocess
import platform
from dataclasses import dataclass

from .modules import run_kmod

KconfigSet = Set[str]


def _open_ikconfig() -> Optional[TextIO]:
    ikconfig = "/proc/config.gz"
    if not os.path.exists(ikconfig):
        run_kmod(["modprobe", "configs"], stderr=subprocess.DEVNULL)
    if os.path.exists(ikconfig):
        try:
            return gzip.open(ikconfig, "rt")
        except OSError as e:
            warnings.warn(f"Found {ikconfig}, but couldn't open it: {e}")
            return None
    return None


def _open_boot_config(is_gzipped: bool) -> Optional[TextIO]:
    suffix = ".gz" if is_gzipped else ""

    config = f"/boot/config-{platform.release()}{suffix}"
    if os.path.exists(config):
        try:
            if is_gzipped:
                return gzip.open(config, "rt")
            else:
                return open(config, "r")
        except OSError as e:
            warnings.warn(f"Found {config}, but couldn't open it: {e}")
            return None
    return None


def _open_src_config() -> Optional[TextIO]:
    kver = platform.release()
    paths = [
        f"/usr/src/linux-headers-{kver}/.config",  # debian
        f"/usr/src/kernel/{kver}/.config",  # red hat
        f"/usr/lib/modules/{kver}/build/.config",  # arch
    ]

    for config in paths:
        if os.path.exists(config):
            try:
                return open(config, "r")
            except OSError as e:
                warnings.warn(f"Found {config}, but couldn't open it: {e}")
                return None
    return None


def get_kconfig() -> Optional[KconfigSet]:
    """Find the kernel configuration"""
    # From most to least reliable.
    cfgfile = (
        _open_ikconfig()
        or _open_boot_config(is_gzipped=False)
        or _open_boot_config(is_gzipped=True)
        or _open_src_config()
    )
    if cfgfile is None:
        return None

    pattern = re.compile(r"CONFIG_[A-Za-z0-9_]*=.*|# CONFIG_[A-Za-z0-9_]* is not set")

    kconfig = set()
    for line in cfgfile:
        line = line.strip()
        if pattern.fullmatch(line):
            kconfig.add(line)
    return kconfig


def get_kernel_cmdline() -> List[str]:
    # If needed: In case we don't have permissions, we could try looking in
    # journalctl or the other log files that get placed around the system.
    with open("/proc/cmdline", "r") as fp:
        return shlex.split(fp.read())


@dataclass(frozen=True)
class KernelVersion:
    """Mostly so we can compare versions without a dependency outside stdlib"""

    major: int
    minor: int

    @classmethod
    def fromstring(cls, version: str) -> "KernelVersion":
        release = version.split(".")
        try:
            return cls(major=int(release[0]), minor=int(release[1]))
        except (ValueError, IndexError):
            raise ValueError(f"Cannot interpret kernel version {release!r}") from None

    @classmethod
    def current(cls) -> "KernelVersion":
        return cls.fromstring(platform.release())

    def __str__(self) -> str:
        return f"{self.major}.{self.minor}"

    def cmp(self, other: Union[str, "KernelVersion"]) -> int:
        if isinstance(other, str):
            other = self.fromstring(other)
        return ((self.major > other.major) - (self.major < other.major)) or (
            (self.minor > other.minor) - (self.minor < other.minor)
        )

    def __lt__(self, other: Union[str, "KernelVersion"]) -> bool:
        return self.cmp(other) < 0

    def __le__(self, other: Union[str, "KernelVersion"]) -> bool:
        return self.cmp(other) <= 0

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, (str, KernelVersion)):
            return False
        return self.cmp(other) == 0

    def __ne__(self, other: object) -> bool:
        if not isinstance(other, (str, KernelVersion)):
            return True
        return self.cmp(other) != 0

    def __ge__(self, other: Union[str, "KernelVersion"]) -> bool:
        return self.cmp(other) >= 0

    def __gt__(self, other: Union[str, "KernelVersion"]) -> bool:
        return self.cmp(other) > 0

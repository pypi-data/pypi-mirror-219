"""
Misc utilities
"""

import ctypes
import os
from collections import ChainMap
from dataclasses import dataclass
from typing import Optional, Mapping, Iterable, List, Union

from . import PathLike

_libc = ctypes.CDLL(None, use_errno=True)
_mount = _libc.mount
_mount.argtypes = [
    ctypes.c_char_p,
    ctypes.c_char_p,
    ctypes.c_char_p,
    ctypes.c_ulong,
    ctypes.c_char_p,
]
_mount.restype = ctypes.c_int
_umount2 = _libc.umount2
_umount2.argtypes = [ctypes.c_char_p, ctypes.c_int]
_umount2.restype = ctypes.c_int

MNT_FORCE = 1
MNT_DETACH = 2

OptionDict = Mapping[str, Optional[str]]


@dataclass(frozen=True)
class MountEntry:
    mount_id: int
    parent_id: int
    device: int
    root: str
    mountpoint: str
    per_mount_options: OptionDict
    fields: OptionDict
    fstype: str
    source: str
    superblock_options: OptionDict

    @property
    def options(self) -> OptionDict:
        return ChainMap(self.per_mount_options, self.superblock_options)  # type: ignore


def iter_mounts(whose: str = "self") -> Iterable[MountEntry]:
    def parse_options(options: str) -> OptionDict:
        fields = options.split(",")
        result = {}
        for field in fields:
            if "=" in field:
                name, value = field.split("=", 1)
            else:
                name = field
                value = None
            result[name] = value
        return result

    def parse_fields(fields: List[str]) -> OptionDict:
        result = {}
        for tag in fields:
            if ":" in tag:
                name, value = tag.split(":", 1)
            else:
                name = tag
                value = None
            result[name] = value
        return result

    with open(f"/proc/{whose}/mountinfo", "r") as mounts:
        for entry in mounts:
            items = entry.split()
            mount_id = int(items[0])
            parent_id = int(items[1])
            major, minor = items[2].split(":")
            device = os.makedev(int(major), int(minor))
            root = items[3]
            mountpoint = items[4]
            per_mount_options = parse_options(items[5])

            sep = items.index("-", 6)
            fields = parse_fields(items[6:sep])
            fstype = items[sep + 1]
            source = items[sep + 2]
            superblock_options = parse_options(items[sep + 3])

            yield MountEntry(
                mount_id=mount_id,
                parent_id=parent_id,
                device=device,
                root=root,
                mountpoint=mountpoint,
                per_mount_options=per_mount_options,
                fields=fields,
                fstype=fstype,
                source=source,
                superblock_options=superblock_options,
            )


def get_mountinfos(paths: Iterable[PathLike]) -> Iterable[MountEntry]:
    devices = set(os.stat(p).st_dev for p in paths)
    for entry in iter_mounts():
        if entry.device in devices:
            yield entry


def get_mountinfo(path: PathLike) -> Optional[MountEntry]:
    stat = os.stat(path)
    for entry in iter_mounts():
        if stat.st_dev == entry.device:
            return entry
    return None


def mount(
    source: PathLike,
    target: PathLike,
    fstype: Union[str, bytes],
    flags: int = 0,
    data: Optional[str] = None,
) -> None:
    """
    Wrapper around mount() system call.
    """
    source_enc = os.fsencode(source)
    target_enc = os.fsencode(target)
    fstype_enc = os.fsencode(fstype)
    data_enc = os.fsencode(data) if data is not None else None

    res = _mount(source_enc, target_enc, fstype_enc, flags, data_enc)
    if res < 0:
        e = ctypes.get_errno()
        raise OSError(e, os.strerror(e))


def umount(target: PathLike, flags: int = 0) -> None:
    target_enc = os.fsencode(target)
    res = _umount2(target_enc, flags)
    if res < 0:
        e = ctypes.get_errno()
        raise OSError(e, os.strerror(e))

"""
Very basic ELF handling.

If we ever need more than this, it might we worth brining in a dependency.
"""

from typing import Any, List
import sys

from elftools.elf.elffile import ELFFile  # type: ignore
from elftools.common.exceptions import ELFError  # type: ignore

from . import PathLike


class ELF(ELFFile):  # type: ignore
    def __init__(self, path: PathLike):
        stream = open(path, "rb")
        super().__init__(stream)
        self.path = path

    def __del__(self) -> None:
        self.stream.close()

    def get_dynamic(self) -> Any:
        for segment in self.iter_segments():
            if segment.header.p_type == "PT_DYNAMIC":
                return segment
        return None

    def libraries(self) -> List[str]:
        dynamic = self.get_dynamic()
        if dynamic is None:
            return []

        libraries = []
        for tag in dynamic.iter_tags():
            if tag.entry.d_tag == "DT_NEEDED":
                libraries.append(tag.needed)
        return libraries

    def is_native(self) -> bool:
        python = ELF(sys.executable)
        if self.header.e_machine == python.header.e_machine:
            return True
        else:
            return False


# Explicily re-exprt ELFError
__all__ = [ELF, ELFError]

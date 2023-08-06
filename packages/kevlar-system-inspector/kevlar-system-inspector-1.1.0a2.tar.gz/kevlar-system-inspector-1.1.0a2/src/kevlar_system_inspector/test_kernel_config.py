"""
----------------
Kernel Hardening
----------------

The Linux kernel should be configured to minimize the potential attack surface
and provide exploit mitigations where possible. There are many configuration
options that can be addressed in the Linux kernel that can provide extra
security or have subtle security implications.

See :kevlar-code:`300`.
"""

from collections import defaultdict
from typing import Optional, List, Tuple, Dict

import pytest

from .decorators import merge_tests, full_version_only
from .utils.kconfig import KconfigSet


KconfigCheckRow = Tuple[str, Optional[str], List[str], str]

KCONFIG_SIMPLE_CHECKS: List[KconfigCheckRow] = [
    # Each row:
    #   1. Config name
    #   1. String value, or NOT_PRESENT
    #   2. Dependencies. If they aren't all satisfied, this check is skipped.
    #   3. Description.
    #
    # The config to check can appear multiple times. This is useful if there
    # are OR conditions in the dependencies like (X86_64 || X86_PAE).
    (
        "CONFIG_BUG_ON_DATA_CORRUPTION",
        "y",
        [],
        """
        The CONFIG_BUG_ON_DATA_CORRUPTION option will generate a BUG when data
        corruption is detected, rather than letting it pass with a warning.
        """,
    ),
    (
        "CONFIG_PAGE_POISONING",
        "y",
        [],
        """
        The CONFIG_PAGE_POISONING option will take proactive measures to mark
        freed memory pages as "poisoned" to mitigate a common class of
        vulnerabilities.
        """,
    ),
    (
        "CONFIG_SLAB_FREELIST_RANDOM",
        "y",
        [],
        """
        The CONFIG_SLAB_FREELIST_RANDOM option ensures that memory allocation is
        randomized to mitigate a common class of vulnerabilities.
        """,
    ),
    (
        "CONFIG_SLAB_FREELIST_HARDENED",
        "y",
        [],
        """
        The CONFIG_SLAB_FREELIST_HARDENED option adds additional consistency
        checks to memory allocation to mitigate a common class of
        vulnerabilities.
        """,
    ),
    (
        "CONFIG_PROC_KCORE",
        None,
        [],
        """
        The CONFIG_PROC_KCORE option controls the inclusion of the potentially
        dangerous /proc/kcore file.
        """,
    ),
    (
        "CONFIG_MODIFY_LDT_SYSCALL",
        None,
        ["CONFIG_X86=y"],
        """
        The CONFIG_MODIFY_LDT_SYSCALL option is meant for legacy 16-bit code,
        but provides attackers with an increased attack surface.
        """,
    ),
    (
        "CONFIG_DEVMEM",
        None,
        [],
        """
        The CONFIG_DEVMEM option controls whether userspace programs can
        directly access physical memory.
        """,
    ),
    (
        "CONFIG_DEBUG_CREDENTIALS",
        "y",
        ["CONFIG_DEBUG_KERNEL=y"],
        """
        The CONFIG_DEBUG_CREDENTIALS option enables additional consistency
        checking of process credentials, a common target of attackers.
        """,
    ),
]


def _make_kconfig_ids() -> List[str]:
    seen: Dict[str, int] = defaultdict(int)
    ids = []
    for row in KCONFIG_SIMPLE_CHECKS:
        row = getattr(row, "values", row)  # normalize pytest.param entries
        name = row[0]
        id_val = name
        suffix = seen[name]
        if suffix:
            id_val = f"{id_val}-{suffix}"
        seen[name] += 1
        ids.append(id_val)
    return ids


KCONFIG_SIMPLE_IDS = _make_kconfig_ids()


@pytest.mark.parametrize(
    ["name", "value", "dependencies", "description"],
    KCONFIG_SIMPLE_CHECKS,
    ids=KCONFIG_SIMPLE_IDS,
)
def test_configuration_items(
    kconfig: KconfigSet,
    name: str,
    value: Optional[str],
    dependencies: List[str],
    description: Optional[str],
) -> None:
    """
    {{ name }} should be {{ 'enabled' if value else 'disabled' }}.
    ==============================================================

    {{description | dedent}}
    """

    if not value:
        config = f"# {name} is not set"
        message = f"{name} is **not** disabled."
    else:
        config = f"{name}={value}"
        message = f"{name} is **not** enabled"

    for dep in dependencies:
        if dep not in kconfig:
            pytest.skip(f"Dependency {dep} not met for {config}")

    assert config in kconfig, message


@full_version_only
def test_slub_debug_params(
    flag: str, reason: str, kernel_cmdline: List[str], kconfig: KconfigSet
) -> None:
    """
    Kernel heap checks should be enabled.
    =====================================

    Kernel heap checks ensure the system detects and responds to memory
    corruption events involving the kernel heap.
    """
    ...


@full_version_only
def test_shadow_call_stack_enabled() -> None:
    """
    Shadow Call Stack should be enabled.
    ====================================

    The shadow call stack is a feature that prevents stack based buffer
    overflow vulnerabilities from being exploited.
    """


@full_version_only
def test_devices_not_enabled_via_standard_path() -> None:
    """
    Device path ``{{device_path}}`` should not be present.
    ==============================================================

    The ``{{device_path}}`` device enables a means of accessing physical memory
    of the system.
    """
    ...


@full_version_only
def test_devices_via_nonstandard_path() -> None:
    """
    ``{{device_path}}`` should be inaccessible even through indirect means.
    ============================================================================

    Deleting a device file path is not enough to render a device inaccessible.
    It needs to be removed from the kernel entirely.
    """
    ...


@full_version_only
def test_has_module_signing() -> None:
    """
    Kernel module signatures should be enabled.
    ===========================================

    The Linux kernel will check the integrity of loaded modules to guard
    against corruption and malware.
    """
    ...


@full_version_only
def test_has_strict_module_signing() -> None:
    """
    Unsigned kernel modules should not load.
    ========================================

    Unsigned modules should not be loadable, to guard against malware and
    corruption.
    """
    ...


@full_version_only
def test_has_strong_module_signing_hash() -> None:
    """
    Kernel module signatures should use strong hash functions.
    ==========================================================

    Only modern, cryptographically strong hash functions should be used to sign
    kernel modules.
    """
    ...


@merge_tests
class TestModulesUnsigned:
    """
    All kernel modules should be validly signed.
    ============================================

    All kernel modules found in a running Linux system should have valid
    signatures.

    .. note::

       This test looks for the presence of a signature and validates its
       parameters, but it does not cryptographically verify the signature.
    """

    @full_version_only
    def test_any_modules_unsigned(self) -> None:
        ...

    @full_version_only
    def test_validate_module_signatures(self) -> None:
        ...


@full_version_only
def test_kernel_refuses_to_load_unsigned() -> None:
    """
    Kernel modules with stripped signatures should not load.
    ========================================================

    Attackers should not be able to strip signatures from existing modules.
    """
    ...


@merge_tests
class TestKernelRefusesToLoadCorrupted:
    """
    Corrupted kernel modules should not load.
    =========================================

    If a kernel module has been tampered with or modified, it should not load.
    """

    @full_version_only
    def test_kernel_refuses_to_load_corrupted_data(self) -> None:
        ...

    @full_version_only
    def test_kernel_refuses_to_load_corrupted_sig(self) -> None:
        ...

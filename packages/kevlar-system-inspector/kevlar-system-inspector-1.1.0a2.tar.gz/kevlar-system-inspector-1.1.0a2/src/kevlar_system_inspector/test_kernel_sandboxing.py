"""
-----------------
Kernel Sandboxing
-----------------

Kernel sandboxing is the process of isolating kernel subsystems from other
kernel subsystems.


See :kevlar-code:`800`.
"""

import pytest

from .utils.kconfig import KconfigSet


def test_clang_cfi_enabled(kconfig: KconfigSet) -> None:
    """
    Kernel sandboxing should be enabled.
    ====================================

    Kernel sandboxing support should be compiled into the kernel.
    """

    if "CONFIG_ARCH_SUPPORTS_CFI_CLANG=y" not in kconfig:
        pytest.skip("N/A for this architecture")

    assert "CONFIG_CFI_CLANG=y" in kconfig, "Kernel sandboxing is not enabled!"

"""
----------------------
Application Sandboxing
----------------------

Application sandboxing is the process of isolating applications from the rest
of the system to prevent rogue applications from accessing or modifying
sensitive resources. Attackers will attempt to use a vulnerable application to
escalate privileges and/or execute malicious code. Such actions tend to be
abnormal, i.e., they do not fit a model of how an application normally
executes. Application sandboxing attempts to create a model of normal
(different techniques are possible) and then detect deviation from the model.

Application sandboxing should be applied to systemd. Systemd services
constitute the userspace core of a running system and as such are primary
targets for attackers. Applying application sandboxing can mitigate the impact
of a compromised systemd service.

See :kevlar-code:`700`.
"""

import subprocess

import pytest

from .decorators import full_version_only
from .utils.systemd import is_system_using_systemd

# Skip on non-systemd systems
pytestmark = pytest.mark.skipif(
    not is_system_using_systemd(), reason="Not using systemd on this system"
)


def test_systemd_has_seccomp_enabled() -> None:
    """
    Systemd should be built with application sandboxing support.
    ============================================================

    Systemd support for application sandboxing is a compile-time option that
    should be enabled.
    """

    result = subprocess.run(
        ["systemctl", "--version"], text=True, stdout=subprocess.PIPE
    )
    assert "+SECCOMP" in result.stdout, "Systemd was not compiled with seccomp support."


@full_version_only
def test_has_filter_installed() -> None:
    """
    The systemd-resolved service should be protected with application sandboxing.
    ===============================================================================================

    Application sandboxing is available for this service, and it should be enabled.
    """
    ...

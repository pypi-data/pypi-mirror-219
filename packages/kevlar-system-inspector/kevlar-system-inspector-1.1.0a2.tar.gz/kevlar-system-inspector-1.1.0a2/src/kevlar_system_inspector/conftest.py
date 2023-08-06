import sys
import os
import textwrap
from typing import Generator
from pathlib import Path
import warnings
from typing import List
import site
import sysconfig

import pytest

import kevlar_system_inspector
from .version import VERSION
from .utils.kconfig import get_kconfig, get_kernel_cmdline, KconfigSet
from .utils import require_tool


def pytest_configure(config: "pytest.Config") -> None:
    config.addinivalue_line(
        "markers", "requires_root: Fails the test if we aren't root"
    )

    config.addinivalue_line(
        "markers", "full_version_only: Implemented in kevlar-system-inspector-extras"
    )

    config.addinivalue_line(
        "markers", "requires_tool: Requires a binary tool to be installed"
    )


def pytest_runtest_setup(item: pytest.Item) -> None:
    for mark in item.iter_markers(name="requires_tool"):
        require_tool(*mark.args, **mark.kwargs)

    if any(item.iter_markers(name="requires_root")):
        assert os.geteuid() == 0, "Test skipped: requires root."


def pytest_sessionstart() -> None:
    # Workaround for running under `su` on Debian. This does not clear environment variables,
    # so getpass.getuser() will return the username that we were before rather than "root".
    # This causes a sanity check in pytest to fail when getting a temporary directory.
    # Remove the envionment variables that could cause problems so that getpass is forced
    # to use the passwd database and our current uid.
    for env in ["LOGNAME", "USER", "LNAME", "USERNAME"]:
        os.environ.pop(env, None)


def is_user_install() -> bool:
    """
    Does it appear that we got installed to $HOME/.local/bin or similar?

    The actual test is: would the wrapper script be able to find this package
    if run via sudo?
    """

    if os.getuid() == 0:
        return False  # Clearly they got it working.

    # Get all the non-user places that will apply when run via sudo
    lib_paths = set(site.getsitepackages())
    lib_paths.add(sysconfig.get_path("stdlib"))
    lib_paths.add(sysconfig.get_path("platstdlib"))
    lib_paths.add(sysconfig.get_path("purelib"))
    lib_paths.add(sysconfig.get_path("platlib"))

    # Process .pth files as the site module would. Useful in development so we
    # don't get warnings when using an editable install in a virtualenv.
    pth_additions = set()
    for path in lib_paths:
        try:
            files = os.listdir(path)
        except OSError:
            continue  # Not all of them exist

        for filename in files:
            if not filename.endswith(".pth"):
                continue
            pth_file = os.path.join(path, filename)
            with open(pth_file) as pth:
                for line in pth:
                    line = line.strip()
                    if (
                        not line
                        or line.startswith("#")
                        or line.startswith("import ")
                        or line.startswith("import\t")
                    ):
                        continue
                    pth_additions.add(os.path.join(path, line))
    lib_paths.update(pth_additions)

    # Also allow the module to be next to the script (standalone)
    lib_paths.add(os.path.dirname(sys.argv[0]))

    def is_subpath_of(filename: str, base: str) -> bool:
        return not os.path.relpath(filename, base).startswith("../")

    for path in lib_paths:
        if is_subpath_of(kevlar_system_inspector.__file__, path):
            return False

    return True


@pytest.fixture(scope="session", autouse=True)
def check_session() -> None:
    if os.getuid() != 0:
        warnings.warn(
            textwrap.dedent(
                """\
                **Kevlar System Inspector should be run as root.**

                Kevlar System Inspector performs in-depth checks, including
                those intended to guard against compromised system programs and
                insider threats. Many of these tests will be skipped if Kevlar
                System Inspector is run as a regular user.
                """
            )
        )

    if is_user_install():
        warnings.warn(
            textwrap.dedent(
                """\
                **Kevlar System Inspector should not be installed to your home
                directory**

                This makes it inconvenient to run kevlar-system-inspector as
                root. Instead, we recommend a virtual environment:

                .. code-block:: console

                    $ python3 -m venv kevlar-venv
                    $ ./kevlar-venv/bin/pip install kevlar-system-inspector
                    $ sudo ./kevlar-venv/bin/kevlar-system-inspector

                You can also install kevlar-system-inspector system wide:

                .. code-block:: console

                    $ sudo python3 -m pip install kevlar-system-inspector
                    $ sudo kevlar-system-inspector

                """
            )
        )

    try:
        from kevlar_system_inspector_extras.version import VERSION as EXTRAS_VERSION
    except ImportError:
        pass
    else:
        if EXTRAS_VERSION != VERSION:
            warnings.warn(
                textwrap.dedent(
                    f"""\
                    **Full tests version mismatch detected**

                    The version of kevlar-system-inspector-extras
                    ({EXTRAS_VERSION}) differs from the base installed version
                    of kevlar-system-inspector ({VERSION}).

                    Please ensure you have installed the correct package(s), or
                    contact `Star Lab`__ for an updated package.

                    .. __: https://www.starlab.io/contact-us-kevlar-system-inspector-user
                    """
                )
            )


@pytest.fixture(scope="module")
def workdir(tmp_path_factory: "pytest.TempPathFactory") -> Generator[Path, None, None]:
    from .utils.workdir import get_workdir

    with get_workdir(tmp_path_factory) as path:
        yield path


@pytest.fixture(scope="session")
def kconfig() -> KconfigSet:
    config = get_kconfig()
    if config is None:
        pytest.fail("Could not find kconfig!")
    return config


@pytest.fixture(scope="session")
def kernel_cmdline() -> List[str]:
    return get_kernel_cmdline()

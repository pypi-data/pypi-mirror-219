import sys
import os
import argparse
import shlex
from typing import List, Any
import platform

"""
A security inspector for embedded systems.
"""


# Set up vendored dependencies, if they exist.  This must come before 3rd party
# imports
_THIS_DIR = os.path.abspath(os.path.dirname(__file__))
_VENDOR_ZIP = os.path.join(_THIS_DIR, "_vendor.zip")
sys.path.insert(0, _VENDOR_ZIP)

import pytest

from .console import ConsoleProgress
from .report import KevlarReporter
from .output import (
    HtmlReporter,
    RstReporter,
    ConsoleReporter,
    TextReporter,
    SummaryReporter,
)
from .version import get_version

DEFAULT_OUTPUT_FILE = "kevlar-system-inspector-report.txt"


class Tweaks:
    """Misc things to get around the fact that we are disabling default plugins"""

    def pytest_configure(self, config: "pytest.Config") -> None:
        # These are usually set by terminal plugin. Various bits of pytest expect them to
        # be set. Mostly an issue only when we want to break into pdb.
        config.option.color = "yes"
        config.option.code_highlight = "yes"
        config.option.verbose = False


def system_check() -> None:
    """Is this a supported version of Python?"""
    if sys.hexversion < 0x03070000:
        sys.stderr.write(f"Detected Python version: {platform.python_version()}\n")
        sys.stderr.write(
            "This version is END-OF-LIFE and unsupported by Kevlar System Inspector.\n"
        )
        sys.exit(1)

    if sys.platform != "linux":
        sys.stderr.write(f"Detected platform: {sys.platform}\n")
        sys.stderr.write(
            "While we appreciate such an intrepid use of our software, Kevlar "
            "System Inspector is, unfortunately Linux-only.\n"
        )
        sys.exit(1)


def main() -> None:
    system_check()
    parser = argparse.ArgumentParser(description=__doc__)
    output = parser.add_argument_group("Output Options")
    output.add_argument(
        "--output",
        action="store",
        help=f"""
             Print plaint text report to a file. This is the default, unless
             any of the other --ouput-* options are given. The default file
             name is {DEFAULT_OUTPUT_FILE!r}.
             """,
    )
    output.add_argument(
        "--output-console",
        action="store_true",
        help="""
             Print formatted console output.
             """,
    )
    output.add_argument(
        "--output-html",
        action="store",
        help="Write an HTML output report to the given file.",
    )
    output.add_argument(
        "--output-rst",
        action="store",
        help="""
             Write a reStructuredText output report to the given file. This
             file may be converted into many different formats using a tool
             such as pandoc or docutils.
             """,
    )

    parser.add_argument(
        "--terminal-color",
        action="store",
        choices=["auto", "always", "never"],
        default="auto",
        help="""
             Control fancy output formatting for any output to the terminal.
             The default 'auto' will print formatted output to the console, but
             will print plain output when redirected to a file or pipe. The
             value 'always' will always print formatted output, and 'never'
             will always print plain output.
             """,
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"Kevlar System Inspector: {get_version()}",
    )

    # Undocumented options:
    #   --debug: turn on regular pytest output
    #   --pytest: Pass arbitrary args to pytest
    #   --debug-coverate: Generate code coverage info
    parser.add_argument("--debug", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument("--pytest", action="store", help=argparse.SUPPRESS)
    parser.add_argument("--debug-coverage", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument("--force-fail-all", action="store_true", help=argparse.SUPPRESS)

    args = parser.parse_args()

    if args.terminal_color == "always":
        os.environ["FORCE_COLOR"] = "1"
    elif args.terminal_color == "never":
        os.environ["TERM"] = "unknown"

    if not any([args.output, args.output_console, args.output_html, args.output_rst]):
        # Default: text report only
        args.output = DEFAULT_OUTPUT_FILE

    # To isolate from any conftest.py or directories with test_*.py in them,
    # use path rather than --pyargs, and explicitly set the root directory.
    pytest_args = [_THIS_DIR, "--rootdir", _THIS_DIR]
    plugins: List[Any] = [
        Tweaks(),
        KevlarReporter(force_fail=args.force_fail_all),
        ConsoleProgress(),
    ]
    if args.output:
        plugins.append(TextReporter(args.output))
    if args.output_html:
        plugins.append(HtmlReporter(args.output_html))
    if args.output_rst:
        plugins.append(RstReporter(args.output_rst))
    if args.output_console:
        plugins.append(ConsoleReporter())
    else:
        plugins.append(SummaryReporter())

    if args.debug_coverage:
        try:
            import pytest_cov  # type: ignore # noqa: 401
        except ImportError:
            parser.error("ptest-cov module not installed. Cannot generate coverage.")
        pytest_args.extend(
            [
                "--cov=kevlar_system_inspector",
                "--cov=kevlar_system_inspector_extras",
                "--cov-report=",
            ]
        )

    if not args.debug:
        # Normally we will disable all normal pytest reporting
        pytest_args.extend(["-p", "no:terminal"])
    else:
        # Show passed tests in the debug summary too: false passes are
        # something we'll be debugging a lot.
        pytest_args.append("-rA")
        if args.debug_coverage:
            pytest_args.append("--cov-report=term")
    pytest_args.extend(shlex.split(args.pytest or ""))

    exit = pytest.main(args=pytest_args, plugins=plugins)
    sys.exit(exit)

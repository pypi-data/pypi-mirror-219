"""
Output of reports in various formats, as pytest plugins
"""

import os

import docutils.core
from rich.console import Console

from . import templates
from .report import TestReport
from .console import print_document


class HtmlReporter:
    def __init__(self, filename: str):
        self.filename = filename

    def pytest_kevlar_report(self, report: TestReport) -> None:
        templates_dir = os.path.dirname(templates.__file__)
        template = os.path.join(templates_dir, "html5-template.txt")
        stylesheet = os.path.join(templates_dir, "starlab.css")

        with open(self.filename, "wb") as fp:
            fp.write(
                docutils.core.publish_from_doctree(
                    report.document,
                    self.filename,
                    writer_name="html5",
                    settings_overrides={
                        "stylesheet_path": stylesheet,
                        "template": template,
                    },
                )
            )

        console = Console()
        console.print(f"Printed detailed report (HTML) to '{self.filename}'")


class RstReporter:
    def __init__(self, filename: str):
        self.filename = filename

    def pytest_kevlar_report(self, report: TestReport) -> None:
        console = Console()
        with open(self.filename, "w") as fp:
            fp.write(report.document_source)
        console.print(
            f"Printed detailed report (reStructuredText) to '{self.filename}'"
        )


class ConsoleReporter:
    def pytest_kevlar_report(self, report: TestReport) -> None:
        print_document(report.document)


class TextReporter:
    def __init__(self, filename: str):
        self.filename = filename

    def pytest_kevlar_report(self, report: TestReport) -> None:
        with open(self.filename, "w") as fp:
            print_document(report.document, file=fp, width=80)
        console = Console()
        console.print(f"Printed detailed report (plain text) to '{self.filename}'")


class SummaryReporter:
    """
    Stuff that gets printed in lieu of the full report, when we write to a file.
    """

    def pytest_kevlar_report(self, report: TestReport) -> None:
        print_document(report.summary)
        print()

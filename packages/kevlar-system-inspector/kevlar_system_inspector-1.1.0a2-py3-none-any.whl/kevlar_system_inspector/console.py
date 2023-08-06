"""
Plugin to print progress as we go
"""

import copy
import re
from typing import Set, Optional, List, Any, Generator, Union, Callable, TextIO

from docutils.nodes import NodeVisitor, SkipNode
import docutils.nodes
import pytest
from rich.console import Console, Group, ConsoleOptions
from rich.errors import MissingStyle
from rich.padding import Padding
from rich.panel import Panel
from rich.progress import Progress
from rich.rule import Rule
from rich.style import Style
from rich.syntax import Syntax
from rich.table import Table
from rich.text import Text
from rich.theme import Theme
from pygments.lexers import LEXERS

ALL_LEXERS: Set[str] = set()
for lexers in LEXERS.values():
    ALL_LEXERS.update(lexers[1])

THEME = Theme(
    {
        "h1": Style(bold=True),
        "h2": Style(bold=True, underline=True),
        "h3": Style(bold=True, italic=True),
        "h4": Style(bold=True, dim=True),
        "h5": Style(underline=True),
        "h6": Style(italic=True),
        "h7": Style(italic=True, dim=True),
        "a": Style(color="bright_blue"),
        "a.href": Style(color="blue"),
        "emphasis": Style(italic=True),
        "strong": Style(bold=True),
        "underline": Style(underline=True),
        "literal": Style(reverse=True),
        "warning.border": Style(color="dark_orange", bold=True),
        "caution.border": Style(color="dark_orange", bold=True),
        "admonition-issue.border": Style(bold=True),
        "term": Style(bold=True),
    }
)


class ConsoleProgress:
    def __init__(self) -> None:
        self.total = 0
        self.curr_weight = 0
        self.console = Console(theme=THEME)
        self.progress = Progress(console=self.console)
        self.task: Any = None  # opaque value

    def pytest_itemcollected(self, item: "pytest.Function") -> None:
        self.total += getattr(item.function, "weight", 1)

    @pytest.hookimpl(hookwrapper=True)
    def pytest_runtestloop(
        self, session: "pytest.Session"
    ) -> Generator[None, None, None]:
        self.started = True
        self.task = self.progress.add_task("Inspecting system", total=self.total)
        with self.progress:
            yield

    def pytest_enter_pdb(self) -> None:
        if self.task is not None:
            self.progress.stop()

    def pytest_leave_pdb(self) -> None:
        if self.task is not None:
            self.progress.start()

    def pytest_runtest_setup(self, item: "pytest.Function") -> None:
        self.curr_weight = getattr(item.function, "weight", 1)

    def pytest_runtest_logfinish(self) -> None:
        self.progress.update(self.task, advance=self.curr_weight, refresh=True)


class PrinterContext:
    def __init__(self) -> None:
        self.elements: List[Any] = []
        self.level = 0
        self.style_names: List[str] = []
        self.title: Optional[Text] = None
        self.table: Optional[Table] = None

    def make_group(self) -> Group:
        return Group(*self.elements)


class ConsolePrinter(NodeVisitor):
    def __init__(self, document: docutils.nodes.document):
        super().__init__(document)
        self.context_stack: List[PrinterContext] = []
        self._console: Optional[Console] = None

    def __rich_console__(
        self, console: Console, _options: ConsoleOptions
    ) -> Generator[Any, None, None]:
        """Implements console.print()"""
        self._console = console
        self.context_stack = [PrinterContext()]
        self.document.walkabout(self)
        assert len(self.context_stack) == 1, "Uneven push/pop"
        yield from self.elements

    # Context helpers
    ##############################

    @property
    def console(self) -> Console:
        assert self._console
        return self._console

    @property
    def context(self) -> PrinterContext:
        return self.context_stack[-1]

    @property
    def elements(self) -> List[Any]:
        return self.context_stack[-1].elements

    @property
    def level(self) -> int:
        return self.context_stack[-1].level

    @level.setter
    def level(self, value: int) -> None:
        self.context_stack[-1].level = value

    @property
    def style_names(self) -> List[str]:
        return self.context_stack[-1].style_names

    def get_style(self, suffix: str = "") -> Style:
        for style_name in reversed(self.style_names):
            try:
                return self.console.get_style(style_name + suffix)
            except MissingStyle:
                continue
        return Style()

    def push_context(self) -> None:
        ctx = copy.copy(self.context_stack[-1])
        ctx.elements = []
        ctx.style_names = ctx.style_names.copy()
        ctx.title = None
        self.context_stack.append(ctx)

    def pop_context(self) -> PrinterContext:
        ctx = self.context_stack.pop()
        assert self.context_stack, "Unbalanced push/pops!"
        return ctx

    def pop_as_group(self) -> Group:
        """Pop all elements. Return them as a group"""
        ctx = self.pop_context()
        return ctx.make_group()

    def pop_as_text(self) -> Text:
        text = Text(style=self.get_style())
        ctx = self.pop_context()
        for elem in ctx.elements:
            text.append(elem)
        return text

    # Formatting helpers
    #######################################

    def insert_line_break(self) -> None:
        """Add a line break after the final element, if needed."""

        needs_break = False
        if self.elements:
            prev = self.elements[-1]
            if isinstance(prev, (Text, str)):
                prev_text = str(prev)
                if prev_text and not prev_text.endswith("\n"):
                    needs_break = True
            else:
                needs_break = True

        if needs_break:
            self.elements.append(Text(""))

    # Generic visitors
    ######################################

    def skip_node(self, node: docutils.nodes.Node) -> None:
        """Don't process this node or its children"""
        raise SkipNode()

    def container_visit(self, node: docutils.nodes.Element) -> None:
        """For things with sub-elements. Push a context and set the style."""
        self.push_context()
        self.style_names.append(node.tagname)
        self.style_names.extend(node["classes"])

    def styled_text_depart(self, node: docutils.nodes.Element) -> None:
        """Turn all sub-elements into a Text object."""
        text = self.pop_as_text()
        self.elements.append(text)

    def container_depart(self, node: docutils.nodes.Element) -> None:
        """Turn all sub-elements into a Group"""
        ctx = self.pop_context()
        self.elements.append(Group(*ctx.elements))

    # Ignored nodes
    ####################################

    # Nodes we don't care about. They will be skipped, but their children will not be
    optional = {
        "document",
        "colspec",
        "tgroup",
        "thead",
        "tbody",
        "definition_list",
        "definition_list_item",
    }

    # More nodes we don't care about. This skips all child nodes as well.
    visit_docinfo = skip_node
    visit_topic = skip_node  # No table of contents
    visit_target = skip_node
    visit_system_message = skip_node
    visit_comment = skip_node
    visit_field_list = skip_node
    visit_meta = skip_node

    # Document structure
    #####################################

    def visit_section(self, node: docutils.nodes.section) -> None:
        self.push_context()
        self.level += 1

    def depart_section(self, node: docutils.nodes.section) -> None:
        context = self.pop_context()
        title = context.title
        assert title is not None
        contents = context.make_group()
        self.insert_line_break()
        self.elements.append(title)
        self.insert_line_break()
        self.elements.append(Padding(contents, pad=(0, 0, 0, 4)))

    def visit_title(self, node: docutils.nodes.title) -> None:
        self.push_context()
        if isinstance(node.parent, (docutils.nodes.section, docutils.nodes.document)):
            level = max(self.level, 1)
            self.style_names.append(f"h{level}")

    def depart_title(self, node: docutils.nodes.title) -> None:
        # Since titles are structural, we don't add elements. We just add the
        # renderable to the context and the parent can deal with it however it
        # needs to.
        text = self.pop_as_text()
        self.context.title = text

        # The top level title gets printed immediately
        if isinstance(node.parent, docutils.nodes.document):
            self.elements.append(text)

    def visit_transition(self, node: docutils.nodes.transition) -> None:
        self.elements.append(Rule())

    def depart_transition(self, node: docutils.nodes.transition) -> None:
        pass

    def visit_reference(self, node: docutils.nodes.reference) -> None:
        self.push_context()
        self.style_names.append("a")

    def depart_reference(self, node: docutils.nodes.reference) -> None:
        self.styled_text_depart(node)

        # Append more text to the link text. Console clickable links are a
        # thing, but not universally supported, and easy to miss.  We only
        # handle external links. Internal links have refid instead.
        uri = node.get("refuri")
        if uri:
            text = self.elements[-1]
            text.append(" (")
            text.append(uri, style="a.href")
            text.append(")")
            text.stylize(Style(link=uri))

    # Basic text
    #####################################

    def visit_Text(self, node: docutils.nodes.Text) -> None:
        # The ultimate leaf node.
        text = re.sub(r"\s+", " ", str(node))
        self.elements.append(Text(text, style=self.get_style()))

    def depart_Text(self, node: docutils.nodes.Text) -> None:
        pass

    visit_paragraph = container_visit

    def depart_paragraph(self, node: docutils.nodes.paragraph) -> None:
        text = self.pop_as_text()
        self.insert_line_break()
        self.elements.append(text)

    visit_emphasis = container_visit
    depart_emphasis = styled_text_depart
    visit_strong = container_visit
    depart_strong = styled_text_depart
    visit_inline = container_visit
    depart_inline = styled_text_depart
    visit_literal = container_visit
    depart_literal = styled_text_depart
    visit_line_block = container_visit
    depart_line_block = container_depart

    def visit_literal_block(self, node: docutils.nodes.literal_block) -> None:
        possible_lexers = [cls for cls in node["classes"] if cls in ALL_LEXERS]
        lexer = possible_lexers[0] if possible_lexers else None
        self.insert_line_break()
        self.elements.append(Syntax(node.astext(), theme="default", lexer=lexer))
        # self.elements.append("")
        # Not using any internal elements, because Pygments does our syntax
        # highlighting. Skip sub-elements and depart_literal_block()
        raise SkipNode

    def visit_problematic(self, node: docutils.nodes.problematic) -> None:
        self.elements.append(node.astext())
        raise SkipNode

    # Admonitions
    ####################################

    def make_admonition(self, title: Optional[Union[str, Text]]) -> None:
        style = self.get_style()
        border_style = self.get_style(suffix=".border")
        context = self.pop_context()
        if title is None:
            title = context.title
        contents = context.make_group()

        self.insert_line_break()
        self.elements.append(
            Panel(
                contents,
                title=title,
                style=style,
                border_style=border_style,
                title_align="left",
            )
        )

    visit_admonition = container_visit

    def depart_admonition(self, node: docutils.nodes.admonition) -> None:
        self.make_admonition(None)

    visit_warning = container_visit

    def depart_warning(self, node: docutils.nodes.warning) -> None:
        self.make_admonition("Warning!")

    visit_attention = container_visit

    def depart_attention(self, node: docutils.nodes.attention) -> None:
        self.make_admonition("Attention!")

    visit_caution = container_visit

    def depart_caution(self, node: docutils.nodes.caution) -> None:
        self.make_admonition("Caution!")

    visit_danger = container_visit

    def depart_danger(self, node: docutils.nodes.danger) -> None:
        self.make_admonition("Danger!")

    visit_error = container_visit

    def depart_error(self, node: docutils.nodes.error) -> None:
        self.make_admonition("Error!")

    visit_hint = container_visit

    def depart_hint(self, node: docutils.nodes.hint) -> None:
        self.make_admonition("Hint")

    visit_important = container_visit

    def depart_important(self, node: docutils.nodes.important) -> None:
        self.make_admonition("Important!")

    visit_note = container_visit

    def depart_note(self, node: docutils.nodes.note) -> None:
        self.make_admonition("Note")

    visit_tip = container_visit

    def depart_tip(self, node: docutils.nodes.tip) -> None:
        self.make_admonition("Tip")

    # Format block quotes like an admonition with no title.
    visit_block_quote = visit_admonition
    depart_block_quote = depart_admonition

    # Lists
    ##################################

    def make_list(self, get_marker: Callable[[], Text], items: List[Any]) -> Table:
        table = Table.grid()
        table.add_column()  # marker
        table.add_column()  # item
        for item in items:
            table.add_row(get_marker(), item)
        return table

    def visit_bullet_list(self, node: docutils.nodes.bullet_list) -> None:
        self.push_context()

    def depart_bullet_list(self, node: docutils.nodes.bullet_list) -> None:
        ctx = self.pop_context()

        bullet_style = self.console.get_style("item.bullet", default="none")
        bullet = Text(" • ", bullet_style)

        def get_marker() -> Text:
            return bullet

        elem = self.make_list(get_marker, ctx.elements)
        self.insert_line_break()
        self.elements.append(elem)

    def visit_enumerated_list(self, node: docutils.nodes.enumerated_list) -> None:
        self.push_context()

    def depart_enumerated_list(self, node: docutils.nodes.enumerated_list) -> None:
        ctx = self.pop_context()

        n = 1
        marker_style = self.console.get_style("item.number", default="none")

        def get_marker() -> Text:
            nonlocal n
            marker = n
            n += 1

            return Text(f"{marker:2d}. ", style=marker_style)

        elem = self.make_list(get_marker, ctx.elements)
        self.insert_line_break()
        self.elements.append(elem)

    visit_list_item = container_visit
    depart_list_item = container_depart

    # Definition lists
    ####################################

    visit_line = container_visit
    depart_line = styled_text_depart

    visit_term = visit_paragraph
    depart_term = depart_paragraph

    visit_definition = container_visit

    def depart_definition(self, node: docutils.nodes.definition) -> None:
        contents = self.pop_as_group()
        self.elements.append(Padding(contents, pad=(0, 0, 0, 4)))

    # Tables
    #####################################

    def visit_table(self, node: docutils.nodes.table) -> None:
        self.push_context()
        self.context.table = Table(show_header=False)

        # Only support simple table layouts.
        tgroups = [
            child for child in node.children if isinstance(child, docutils.nodes.tgroup)
        ]
        assert len(tgroups) == 1, "Complex table layouts not supported"

    def depart_table(self, node: docutils.nodes.table) -> None:
        context = self.pop_context()
        self.insert_line_break()
        self.elements.append(context.table)

    visit_row = container_visit

    def depart_row(self, node: docutils.nodes.row) -> None:
        assert self.context.table

        context = self.pop_context()
        if isinstance(node.parent, docutils.nodes.thead):
            self.context.table.show_header = True
            for item in context.elements:
                self.context.table.add_column(item)
        else:
            self.context.table.add_row(*context.elements)

    visit_entry = container_visit
    depart_entry = container_depart


def print_document(
    document: docutils.nodes.document, file: Optional[TextIO] = None, **kwargs: Any
) -> None:
    """Display the report on the console. Depends on KevlarReporter"""
    printer = ConsolePrinter(document)
    console = Console(file=file, theme=THEME, **kwargs)
    console.print(printer)

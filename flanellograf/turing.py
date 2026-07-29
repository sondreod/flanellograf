import os
import re
from pathlib import Path

import yaml
from rich import box
from rich.panel import Panel
from rich.console import Console, ConsoleOptions, RenderResult
from rich.markdown import Markdown, Heading, CodeBlock, ImageItem, Text, BlockQuote
from rich.table import Table
from markdown_it import MarkdownIt
from textual_image.renderable import Image

page = """
# Lol
![Wat](/home/debian/repos/advanced-python-2026/03_data_model/_static/wat-horse.png) where is this text?
"""

from textual_image.renderable import (
    SixelImage as SixelRenderable,
)

class CustomImageItem(ImageItem):
    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:

        uri = self.destination
        yield Image(Path(uri), height='auto', width='20%')
        #yield from super().__rich_console__(console, options)


class MarkdownRenderer(Markdown):
    elements = {
        **Markdown.elements,
        # "heading_open": CustomHeading,
        "image": CustomImageItem,
    }
uri = "examples/turing.jpg"
console = Console()
table = Table.grid(padding=1, collapse_padding=True)

table.add_column("Released", width=10)
table.add_column("Title", justify="left")
table.add_row(
    SixelRenderable(uri, height='auto', width='100%'),
    "[italic]Alan Mathison Turing[/italic]\n1920 - 1950 ⨁OBE ⨁FRS\n\n[italic cyan]“We can only see a short distance ahead,\nbut we can see plenty there that needs to be done”[/italic cyan]\n[bold dim]                                 — Alan M. Turing[/bold dim]"
)
table.add_row(
    "",
)


os.system("cls" if os.name == "nt" else "clear")
console.print(
    table
)
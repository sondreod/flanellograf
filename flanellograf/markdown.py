from pathlib import Path

from textual_image.renderable import Image
from rich.markdown import Markdown, Heading, CodeBlock, ImageItem, Text
from rich.console import Console, ConsoleOptions, RenderResult

class CustomCodeBlock(CodeBlock):
    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:

        if self.lexer_name == "lol":
            self.lexer_name = "python"
        yield from super().__rich_console__(console, options)

class CustomImageItem(ImageItem):
    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:

        uri = self.destination
        yield Image(Path(uri), width='auto', height='90%')
        #yield from super().__rich_console__(console, options)


class MarkdownRenderer(Markdown):
    elements = {
        **Markdown.elements,
        # "heading_open": CustomHeading,
        "image": CustomImageItem,
        "fence": CustomCodeBlock,  # for code blocks with language fences
    }
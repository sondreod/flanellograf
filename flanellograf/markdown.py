from pathlib import Path

from textual_image.renderable import Image
from rich.markdown import Markdown, Heading, CodeBlock, ImageItem, Text
from rich.console import Console, ConsoleOptions, RenderResult

class CustomCodeBlock(CodeBlock):
    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:

        if self.lexer_name in ("python-cell", "python-show"):
            self.lexer_name = "python"
        yield from super().__rich_console__(console, options)

class CustomImageItem(ImageItem):
    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:

        uri = self.destination
        yield Image(Path(uri), width='auto', height='50%')
        #yield from super().__rich_console__(console, options)


class MarkdownRenderer(Markdown):
    elements = {
        **Markdown.elements,
        # "heading_open": CustomHeading,
        "image": CustomImageItem,
        "fence": CustomCodeBlock,  # for code blocks with language fences
    }


""" Support matplotlib inline using TGP (pip install kitcat matplotlib)
import logging
import matplotlib
import matplotlib.pyplot as plt
# Must configure backend BEFORE importing pyplot
matplotlib.use("kitcat")
logging.getLogger('matplotlib.font_manager').disabled = True

plt.style.use('dark_background')
fig, ax = plt.subplots()
fig.patch.set_facecolor('#232627')
ax.set_facecolor('#232627')

plt.xkcd()
plt.bar(['lav','medium','lol','kek'],[3,7,1,6], color="green", alpha=0.7)
plt.show()
"""
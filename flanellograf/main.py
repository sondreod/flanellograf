import os
import re
import signal
from pathlib import Path

from flanellograf.markdown import MarkdownRenderer

import yaml
from rich import box
from rich.panel import Panel
from rich.console import Console
from markdown_it import MarkdownIt



# hack to programatically invoke interactive repl (the one you get with -i, not the ugly one from `code.interact()`)
os.environ['PYTHONINSPECT'] = 'TRUE'


def clear():
    os.system("cls" if os.name == "nt" else "clear")
    return None  # pyinstaller requires explicit None return value O.ó



def parse_slide_source(source: str):
    _, frontmatter, *slides = re.split(r"^---", source, flags=re.MULTILINE)
    return frontmatter, slides



console = Console(color_system="truecolor")

class Board:
    def __init__(self, board_name):
        self.board_name = board_name
        self.slide = -1
        text = Path("examples/intro.md").read_text()

        frontmatter, self.slides = parse_slide_source(text)
        self.frontmatter = yaml.safe_load(frontmatter)

    def display(self):
        clear()
        try:
            page = self.slides[self.slide]
        except IndexError:
            console.print("End of slideshow")
            return
       
        code = []
        md = MarkdownIt()
        tokens = md.parse(page)
        for token in tokens:
            if token.type == 'fence':
                code.append(token.content)

        console.print(
            Panel.fit(
                MarkdownRenderer(page, code_theme="stata-dark",inline_code_lexer="python"),
                box=getattr(box, self.frontmatter.get("style", "ROUNDED").upper()),
                title="───┤ Whats my type? ├────",
                title_align="left"
            )
        )

        exec("\n".join(code), globals())

    def __repr__(self):
        self.slide += 1
        self.display()
        return ""

    def __invert__(self):
        self.display()

    def __pos__(self):
        self.slide = 0
        self.display()

    def __neg__(self):
        self.slide -= 1
        self.display()

    def __call__(self, slide):
        self.slide = int(slide) - 1
        self.display()

    def __matmul__(self, other):
        self.__call__(int(other))


e = Board("lol")
repr(e)

def receive_handler(signum, frame):
    globals()["e"].display()

signal.signal(signal.SIGUSR1, receive_handler)


def sig_handler(*carebear):
    print("lol")
    #globals()["e"].display()

signal.signal(signal.SIGWINCH, sig_handler)
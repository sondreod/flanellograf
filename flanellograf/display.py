import readline
import os
import re
import ast
from pathlib import Path

from flanellograf.markdown import MarkdownRenderer

import yaml
from rich import box
from rich.panel import Panel, Text
from rich.padding import Padding
from rich.console import Console
from rich.syntax import Syntax
from markdown_it import MarkdownIt

def clear():
    os.system("cls" if os.name == "nt" else "clear")
    return None  # pyinstaller requires explicit None return value O.ó

def parse_slide_source(source: str):
    try:
        _, frontmatter, *slides = re.split(r"^---", source, flags=re.MULTILINE)
    except ValueError:
        frontmatter = "style: ROUNDED"
        slides = [source]
    return frontmatter, slides


class Board:
    def __init__(self, path, globals):
        self.globals = globals
        self.slide = -1
        self.text = Path(path).read_text()
        self.console = Console(color_system="truecolor")

        frontmatter, self.slides = parse_slide_source(self.text)
        self.frontmatter = yaml.safe_load(frontmatter)

    def display(self):
        clear()
        try:
            page = self.slides[self.slide]
        except IndexError:
            self.console.print("End of slideshow")
            return
    
        code = []
        md = MarkdownIt()
        tokens = md.parse(page)

        token_info = None
        for token in tokens:
            if token.type == 'fence':
                if token.info in ('python', 'py'):
                    token_info = 'python'
                if token.info in ('python-cell', 'py-cell'):
                    token_info = 'python-cell'
            if token_info:
                code.append(token.content)

        padding = self.console.width - len(self.frontmatter.get("title", "")) - 1 - 2
        title = self.frontmatter.get("title", "") + " " + "─"*padding + " [bold]UGRADERT"
        self.console.print(
            Panel.fit(
                MarkdownRenderer(page, code_theme="stata-dark", inline_code_lexer="python"),
                box=getattr(box, self.frontmatter.get("style", "ROUNDED").upper()),
                title=title,
                subtitle="[bold]UGRADERT",
                subtitle_align="right",
                title_align="left",
                padding=1,
            )
        )
        if token_info in ('py', 'python', 'python-cell'):
            if code:

                source = "\n".join(code)
                nodes = list(ast.iter_child_nodes(ast.parse(source)))
                
                if nodes:
                    """
                    if isinstance(nodes[-1], ast.Expr):
                        if len(nodes) > 1:
                            exec(compile(ast.Module(body=nodes[:-1], type_ignores=[]), "<ast>", "exec"), self.globals)
                        r= eval(compile(ast.Expression(body=nodes[-1].value), "<ast>", "eval"), self.globals)
                    else:
                    """
                    exec(source, self.globals)

            if token_info == 'python-cell':
                if code:
                    readline.add_history(code[-1])



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
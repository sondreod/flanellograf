"""Flanellograf"""

import argparse
import ast
import code as codelib
import os
import pathlib
import re
import readline
from collections import defaultdict

from rich.console import Console, Group
from rich.markdown import Markdown
from rich.panel import Panel
from rich.syntax import Syntax


def pause(minutes=15):
    clear()
    print("\n\n")
    for line in """
    ██████   █████  ██    ██ ███████ ███████ 
    ██   ██ ██   ██ ██    ██ ██      ██      
    ██████  ███████ ██    ██ ███████ █████   
    ██      ██   ██ ██    ██      ██ ██      
    ██      ██   ██  ██████  ███████ ███████ 
    """.splitlines():
        console.print(line)
    from datetime import datetime, timedelta

    new_time = datetime.now() + timedelta(minutes=minutes)
    info = f"Starter igjen {new_time:%H:%M}"
    console.print(f"\n\n{info}")

    try:
        input("Enter / ctrl+c to continue")
    except KeyboardInterrupt:
        clear()

        console.print()


def clear():
    os.system("cls" if os.name == "nt" else "clear")
    return None  # pyinstaller requires explicit None return value O.ó


BOARDS = defaultdict(list)


parser = argparse.ArgumentParser()
parser.add_argument("path", type=pathlib.Path)
args = parser.parse_args()

if args.path.resolve().is_file():
    slide_files = [args.path.resolve()]
else:
    slide_files = list(args.path.resolve().glob("**/board_*.py"))

for f in slide_files:
    board_name = f.name.removeprefix("board_").removesuffix(".py")
    code = f.read_text()
    tree = ast.parse(code)

    functions = [
        node
        for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    ]

    code_lines = code.splitlines()
    max_line_no = 0
    for function in functions:
        if function.end_lineno > max_line_no:  # Skip inner functions
            max_line_no = function.end_lineno
            positional_arguments = [arg.arg for arg in function.args.args]

            func_body = "\n".join(
                x[4:] for x in code_lines[function.lineno : function.end_lineno]
            )

            if func_body.startswith('"""'):
                docstring, *code = func_body[3:].split('"""\n', maxsplit=1)
                if code:
                    code = code[0]
                else:
                    code = ""
            docstring = docstring.strip()

            if "hide_code" in positional_arguments:
                segment = [""]
            else:
                segment = re.split("^yield\n", code, flags=re.MULTILINE)

            page = ""
            for sub_page in segment:
                page += sub_page

                if "raw" in positional_arguments:
                    docstring = f"<RAW>{docstring.removesuffix('"""')}"

                BOARDS[board_name].append((docstring, page))

console = Console()


class Board:
    def __init__(self, board_name):
        self.board_name = board_name
        self.slide = -1

    def display(self):
        clear()
        try:
            page, code = BOARDS[self.board_name][self.slide]
        except IndexError:
            console.print("End of slideshow")
            return
        title, page = page.splitlines()[0], "\n".join(page.splitlines()[1:])

        page = page.removeprefix("\n").removesuffix("\n")
        if title.startswith("<RAW>"):
            title = title[5:]
            page_rendered = page
        else:
            page_rendered = Markdown(
                page,
                inline_code_lexer="python",
            )

        code = code.removeprefix("\n").removesuffix("\n")
        code_rendered = ""
        if code:
            code_rendered = Syntax(
                code,
                "python",
            )

        group = [
            page_rendered,
            code_rendered,
        ]

        if code:
            group.insert(1, "")

        console.print(
            Panel(
                Group(*group),
                title=title,
                title_align="left",
            )
        )
        exec(code, globals())

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


for board in BOARDS:
    globals()[board] = globals()[board[0]] = Board(board)  # (╯°□°)╯︵ ┻━┻

if len(BOARDS) == 1:
    repr(globals()[list(BOARDS.keys())[0]])
else:
    # TODO: make proper TOC
    console.print(Panel("\n".join(BOARDS), title="Flanellograf"))

# TODO: Make code callouts with unicode circle numbers

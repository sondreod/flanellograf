from _pyrepl import console

exec("x = 12")


class Board:
    def __init__(self, board_name):
        self.board_name = board_name
        self.slide = -1
        self.code = ["p = 1337"]

    def display(self):

        exec(self.code[0], globals())

    def __repr__(self):
        self.slide += 1
        mself.display()
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

def main():

    repl = console.InteractiveColoredConsole(locals=locals() | globals())
    repl.interact()

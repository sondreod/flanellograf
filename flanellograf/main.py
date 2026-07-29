import os
import sys
import signal
import readline

from flanellograf.display import Board

# hack to programatically invoke interactive repl (the one you get with -i, not the ugly one from `code.interact()`)
# bah, does'nt seem to work with entry points. (e.g. `uvx flanellograf`). Need more work.
os.environ['PYTHONINSPECT'] = "TRUE"
os.environ['PYTHON_BASIC_REPL'] = "1"


def SIGUSR1_handler(signum, frame):
    globals()["e"].display()

def SIGWINCH_handler(*carebear):
    globals()["e"].display()

signal.signal(signal.SIGUSR1, SIGUSR1_handler)
signal.signal(signal.SIGWINCH, SIGWINCH_handler)

try:
    path = sys.argv[1]
except IndexError:
    print("No file path provided...\nExiting.\n\n")
    exit(1)


e = Board(path, globals=globals())

repr(e)
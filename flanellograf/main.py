import os
import signal

from flanellograf.display import Board

# hack to programatically invoke interactive repl (the one you get with -i, not the ugly one from `code.interact()`)
# bah, does'nt seem to work with entry points. (e.g. `uvx flanellograf`). Need more work.
os.environ['PYTHONINSPECT'] = 'TRUE'


def SIGUSR1_handler(signum, frame):
    globals()["e"].display()

def SIGWINCH_handler(*carebear):
    globals()["e"].display()

signal.signal(signal.SIGUSR1, SIGUSR1_handler)
signal.signal(signal.SIGWINCH, SIGWINCH_handler)

e = Board("lol")

repr(e)
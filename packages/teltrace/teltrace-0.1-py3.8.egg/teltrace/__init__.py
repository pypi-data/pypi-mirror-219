import os

__version__ = "0.1"

# set Python env variable to keep track of example data dir
teltrace_dir = os.path.dirname(__file__)
DATADIR = os.path.join(teltrace_dir, "data/")


try:
    from . import load

    cext = True
except ImportError:
    cext = False

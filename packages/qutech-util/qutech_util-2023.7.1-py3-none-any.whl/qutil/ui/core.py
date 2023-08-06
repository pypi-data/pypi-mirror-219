"""This module contains UI utility functions."""

import sys
from typing import Iterable, Optional, TextIO

__all__ = ['progressbar', 'progressbar_range']

_NOTEBOOK_NAME = None  # flags if _import_tqdm was run
tqdm = None
trange = None


def _import_tqdm():
    # In principle there is tqdm.autonotebook, but it doesn't work in a Spyder kernel.
    global tqdm, trange, _NOTEBOOK_NAME

    import importlib
    try:
        import ipynbname
        _NOTEBOOK_NAME = ipynbname.name()
    except (ImportError, IndexError, FileNotFoundError):
        _NOTEBOOK_NAME = ''

    try:
        if _NOTEBOOK_NAME:
            tqdm = importlib.import_module('tqdm.notebook').tqdm
            trange = importlib.import_module('tqdm.notebook').trange
        elif _NOTEBOOK_NAME is not None:
            # Either not running notebook or not able to determine
            tqdm = importlib.import_module('tqdm').tqdm
            trange = importlib.import_module('tqdm').trange
    except (ImportError, AttributeError):
        pass


def _simple_progressbar(iterable: Iterable, desc: str = "Computing", disable: bool = False,
                        total: Optional[int] = None, size: int = 25, file: TextIO = sys.stdout,
                        *_, **__):
    """https://stackoverflow.com/a/34482761"""
    if disable:
        yield from iterable
        return

    if total is None:
        try:
            total = len(iterable)
        except TypeError:
            raise ValueError(f'{iterable} has no len, please supply the total argument.')

    def show(j):
        x = int(size*j/total)
        file.write("\r{}:\t[{}{}] {} %".format(desc, "#"*x, "."*(size - x),
                   int(100*j/total)))
        file.flush()

    show(0)
    for i, item in enumerate(iterable):
        yield item
        show(i + 1)

    file.write("\n")
    file.flush()


def progressbar(iterable: Iterable, *args, **kwargs):
    """
    Progress bar for loops. Uses tqdm if available or a quick-and-dirty
    implementation from stackoverflow.

    Usage::

        for i in progressbar(range(10)):
            do_something()

    See :class:`~tqdm.tqdm` or :func:`_simple_progressbar` for possible
    args and kwargs.
    """
    if _NOTEBOOK_NAME is None:
        _import_tqdm()
    if tqdm is not None:
        return tqdm(iterable, *args, **kwargs)
    else:
        return _simple_progressbar(iterable, *args, **kwargs)


def progressbar_range(*args, **kwargs):
    if _NOTEBOOK_NAME is None:
        _import_tqdm()
    if tqdm is not None:
        return trange(*args, **kwargs)
    else:
        return _simple_progressbar(range(*args), **kwargs)

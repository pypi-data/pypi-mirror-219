"""Import everything from functools and some custom functions."""
from functools import *
from typing import Callable, Iterator, Any
import inspect


class FunctionChain:
    """Chain of multiple functions. The return value(s) of each previous
    function are the first ``n_args`` positional argument(s) of the next
    function call. This class is for convenient reuse of function chains
    and passing them around as callable objects.

    Similar to :func:`reduce`, but instead of reducing a sequence using
    a single function, this reduces a list of functions by applying them
    iteratively to the output of the function before.

    Example:

    >>> from qutil.functools import chain
    >>> import numpy as np
    >>> x = np.array([1, 4, -6, 8], dtype=float)
    >>> f_chain = FunctionChain(np.abs, np.sqrt)
    >>> f_chain(x, out=x)  # Will write all intermediate results into the same array.
    array([1.        , 2.        , 2.44948974, 2.82842712])

    n_args argument:

    >>> def adder(x, axis):
    ...     return x.sum(axis), axis - 1
    >>> def multiplier(x, axis):
    ...     return x.prod(axis), axis - 1
    >>> x = np.arange(12).reshape(3, 4)
    >>> axis = 1
    >>> f_chain = FunctionChain(adder, multiplier, n_args=2)
    >>> f_chain(x, axis)
    (5016, -1)
    """

    def __init__(self, *functions: Callable, n_args: int = 1, inspect_kwargs: bool = False):
        self.functions = functions
        self.n_args = n_args
        self.inspect_kwargs = inspect_kwargs
        if self.n_args < 1:
            raise ValueError(f'n_args should be a positive integer, not {n_args}.')

    def __getitem__(self, item: Any) -> Callable:
        return self.functions[item]

    def __len__(self) -> int:
        return len(self.functions)

    def __iter__(self) -> Iterator[Callable]:
        yield from self.functions

    def __repr__(self) -> str:
        return (
            super().__repr__()
            + ' with functions'
            + ('\n - {}'*len(self)).format(*self.functions)
        )

    def __call__(self, *args, **kwargs):
        """Iteratively apply functions to the return value of the
        previous one, starting with `x` as initial argument.

        Args:
            *args: Positional arguments that get passed to each function besides the previous function's return value.
            **kwargs: Keyword arguments that get passed to each function.

        Returns:
            Return value of the last function
        """
        args = list(args)
        for func in self.functions:
            if self.inspect_kwargs:
                tmp_kwargs = {k: v for k, v in kwargs.items()
                              if k in inspect.signature(func).parameters}
            else:
                tmp_kwargs = kwargs
            if self.n_args > 1:
                args[:self.n_args] = func(*args, **tmp_kwargs)
            else:
                args[0] = func(args[0], *args[1:], **tmp_kwargs)
        return tuple(args[:self.n_args]) if self.n_args > 1 else args[0]


def chain(*functions: callable, n_args: int = 1, inspect_kwargs: bool = False) -> FunctionChain:
    """Chain multiple functions. The return value of each previous function is the first argument of the next function
    call.

    Example:
        >>> from qutil.functools import chain
        >>> import numpy as np
        >>> f_chain = chain(np.diff, np.sum, print)
        >>> f_chain([1, 3, 6])
        5

    Args:
        *functions: Functions to be chained.
    Returns:
        Callable object that chains arguments.
    """
    return FunctionChain(*functions, n_args=n_args, inspect_kwargs=inspect_kwargs)

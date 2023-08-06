import logging
import warnings
from contextlib import contextmanager
from importlib import import_module
from types import ModuleType
from typing import Dict, Optional, Union
from unittest.mock import MagicMock


@contextmanager
def all_logging_disabled(highest_level=logging.CRITICAL):
    """
    A context manager that will prevent any logging messages
    triggered during the body from being processed.
    :param highest_level: the maximum logging level in use.
    This would only need to be changed if a custom level greater than CRITICAL
    is defined.

    https://gist.github.com/simon-weber/7853144
    """
    # two kind-of hacks here:
    #    * can't get the highest logging level in effect => delegate to the user
    #    * can't get the current module-level override => use an undocumented
    #       (but non-private!) interface

    previous_level = logging.root.manager.disable

    logging.disable(highest_level)

    try:
        yield
    finally:
        logging.disable(previous_level)


@contextmanager
def filter_warnings(action, category=Warning, lineno=0, append=False, *,
                    record=False, module=None):
    """A context manager that combines catching and filtering warnings."""
    with warnings.catch_warnings(record=record, module=module) as manager:
        warnings.simplefilter(action, category, lineno, append)
        try:
            yield manager
        finally:
            pass


def import_or_mock(
        name: str, package: Optional[str] = None, local_name: Optional[str] = None
) -> Dict[str, Union[ModuleType, MagicMock]]:
    """Imports a module or, if it cannot be imported, mocks it.

    If it is importable, equivalent to::
        from name import package as local_name

    Parameters
    ----------
    name : str
        See :func:`importlib.import_module`.
    package : str | None
        See :func:`importlib.import_module`.
    local_name : str
        Either the name assigned to the module or the object to be
        imported from the module.

    Returns
    -------
    dict[str, ModuleType | MagicMock]
        A dictionary with the single entry {local_name: module}.

    Examples
    --------
    >>> locals().update(import_or_mock('numpy', None, 'pi'))
    >>> pi
    3.141592653589793
    >>> locals().update(import_or_mock('owiejlkjlqz'))
    >>> owiejlkjlqz
    <MagicMock name='mock.owiejlkjlqz' id='...'>

    """
    local_name = local_name or name
    try:
        module = import_module(name, package)
    except ImportError:
        module = MagicMock(__name__=name)
    return {local_name: getattr(module, local_name, module)}

"""This module contains some useful plotting functions.

Moreoever, there are custom stylefiles defined in the ``stylelib``
subdir. You can employ these globally by calling::

    plt.style.use('qutil.plotting.<stylename>')

or within a context::

    with plt.style.context('qutil.plotting.<stylename>'):
        ...

Note that this requires ``matplotlib>=3.7.0``. If you don't want to
upgrade, you can also copy the style files to
``matplotlib.get_configdir()/stylelib``.

Examples
--------
Note that this syntax requires ``matplotlib>=3.7.0``.

Plot data using a style adjusted to APS journals:

>>> import matplotlib.pyplot as plt
>>> with plt.style.context('qutil.plotting.publication_aps_tex'):
...    plt.plot([1, 2], [3, 4], label='presentation style')
...    plt.legend()
...    plt.show(block=False)
[...

Plot data using all available custom styles:

>>> import pathlib, qutil
>>> module_path = pathlib.Path(qutil.__file__).parent
>>> for file in (module_path / 'plotting').glob('*.mplstyle'):
...     file = file.relative_to(module_path)
...     style = '.'.join(('qutil',) + file.parent.parts + (file.stem,))
...     with plt.style.context(style):
...         plt.plot([1, 2], [3, 4])
...         plt.title(file.stem)
...         plt.show(block=False)
[...
"""
from .core import *

"""This module contains some useful plotting functions.

TODO
----
    - Use matplotlib widgets for LineClicker, CoordClicker. See
      https://matplotlib.org/stable/gallery/index.html#widgets
"""
import dataclasses
import pathlib
import warnings
from contextlib import contextmanager
from typing import Sequence, Tuple, Mapping, Any, Union, List
from weakref import WeakValueDictionary

import matplotlib as mpl
import numpy as np
import pandas as pd
from matplotlib import cycler
from matplotlib import pyplot as plt

__all__ = [
    "CoordClicker",
    "LineClicker",
    "LaTeXPlotHelper",
    "BlitManager",
    "changed_plotting_backend",
    "plot_2d_dataframe",
    "cycle_plots",
    "update_plot",
    "list_styles",
    "get_rwth_color_cycle",
    "rwth_color_cycle",
    "rwth_color_cycle_25",
    "rwth_color_cycle_50",
    "rwth_color_cycle_75",
    "rwth_color_cycle_100",
    "RWTH_COLORS"
]

_color_names = ['blue', 'magenta', 'green', 'orange', 'teal', 'maygreen',
                'red', 'purple', 'violet', 'bordeaux', 'petrol', 'yellow']
_color_tuples = [
    (0/255, 84/255, 159/255),       # blue
    (227/255, 0/255, 102/255),      # magenta
    (87/255, 171/255, 39/255),      # green
    (246/255, 168/255, 0/255),      # orange
    (0/255, 152/255, 161/255),      # teal
    (189/255, 205/255, 0/255),      # maygreen
    (204/255, 7/255, 30/255),       # red
    (122/255, 111/255, 172/255),    # purple
    (97/255, 33/255, 88/255),       # violet
    (161/255, 16/255, 53/255),      # bordeaux
    (0/255, 97/255, 101/255),       # petrol
    (255/255, 237/255, 0/255),      # yellow
]
RWTH_COLORS = dict(zip(_color_names, _color_tuples))


class CoordClicker:
    def __init__(self, fig, plot_click: bool = False, print_coords: bool = False, precision=3,
                 **style):
        self.fig = fig
        self.print_coords = print_coords
        self.plot_click = plot_click
        self.style = {**{'marker': 'x', 'color': 'r'}, **style}
        self.precision = precision
        self.xs = []
        self.ys = []
        self.cid = self.fig.canvas.mpl_connect('button_press_event', self)

    def __call__(self, click):
        self.xs.append(click.xdata)
        self.ys.append(click.ydata)
        if self.plot_click:
            click.inaxes.plot(self.xs[-1], self.ys[-1], **self.style)
            self.fig.canvas.draw()
        if self.print_coords:
            with np.printoptions(precision=self.precision):
                print(f"(x, y) = {np.array([self.xs, self.ys])[:, -1]}")

    def __del__(self):
        self.disconnect()

    def disconnect(self):
        self.fig.canvas.mpl_disconnect(self.cid)


class LineClicker:
    def __init__(self, ax, print_coords: bool = False, color='tab:red'):
        self.ax = ax
        self.fig = ax.get_figure()
        self.line, = self.ax.plot([], [], color=color)
        self.print_coords = print_coords
        self.xs = list(self.line.get_xdata())
        self.ys = list(self.line.get_ydata())
        self.cid = self.fig.canvas.mpl_connect('button_press_event', self)

    def __call__(self, click):
        if click.inaxes != self.ax:
            return
        self.xs.append(click.xdata)
        self.ys.append(click.ydata)
        self.line.set_data(self.xs, self.ys)
        self.fig.canvas.draw()
        if self.print_coords:
            with np.printoptions(precision=3):
                print(f"(x, y) = {np.array(self.line.get_data())[:, -1]}")

    def __del__(self):
        self.disconnect()

    def disconnect(self):
        self.fig.canvas.mpl_disconnect(self.cid)


class BlitManager:
    """A manager for blitting raster graphics to speed up plot
    refreshes.

    This class is taken from the matplotlib documentation [1]_. See also
    there for a general introduction to blitting and how it can help
    speed up plot updates.

    Parameters
    ----------
    canvas : FigureCanvasAgg
        The canvas to work with, this only works for subclasses of the
        Agg canvas which have the
        :meth:`~FigureCanvasAgg.copy_from_bbox` and
        :meth:`~FigureCanvasAgg.restore_region` methods.

    animated_artists : Iterable[Artist]
        List of the artists to manage

    Examples
    --------
    Also adapted from the documentation:

    >>> import time

    >>> # make a new figure
    >>> fig, ax = plt.subplots()
    >>> # add a line
    >>> x = np.linspace(-10, 10, 1001)
    >>> (ln,) = ax.plot(x, np.sin(x), animated=True)
    >>> # add a frame number
    >>> fr_number = ax.annotate(
    ...     "frame: 0",
    ...     (0, 1),
    ...     xycoords="axes fraction",
    ...     xytext=(10, -10),
    ...     textcoords="offset points",
    ...     ha="left",
    ...     va="top",
    ...     animated=True,
    ... )
    >>> bm = BlitManager(fig.canvas, [ln, fr_number])
    >>> # make sure our window is on the screen and drawn
    >>> plt.show(block=False)
    >>> plt.pause(.1)

    >>> elapsed = np.empty(201)
    >>> elapsed[0] = time.perf_counter()
    >>> for j in range(200):
    ...     # update the artists
    ...     ln.set_ydata(np.sin(x + (j / 200) * np.pi))
    ...     fr_number.set_text("frame: {j}".format(j=j))
    ...     # tell the blitting manager to do its thing
    ...     bm.update()
    ...     elapsed[j+1] = time.perf_counter()
    >>> print(f'Average time per update: {np.diff(elapsed).mean():.2g} s')  #doctest: +SKIP
    Average time per update: 0.0026 s

    Just for comparison, without blitting:

    >>> ln.set_animated(False)
    >>> ln.set_ydata(np.sin(x))
    >>> fr_number.set_animated(False)
    >>> fr_number.set_text("frame: 0")

    >>> elapsed = np.empty(201)
    >>> elapsed[0] = time.perf_counter()
    >>> for j in range(200):
    ...     # update the artists
    ...     ln.set_ydata(np.sin(x + (j / 200) * np.pi))
    ...     fr_number.set_text("frame: {j}".format(j=j))
    ...     fig.canvas.draw_idle()
    ...     fig.canvas.flush_events()
    ...     elapsed[j+1] = time.perf_counter()
    >>> print(f'Average time per update: {np.diff(elapsed).mean():.2g} s')  #doctest: +SKIP
    Average time per update: 0.015 s

    References
    ----------
    .. [1] https://matplotlib.org/stable/tutorials/advanced/blitting.html
    """

    def __init__(self, canvas, animated_artists=()):
        self.canvas = canvas
        self._bg = None
        self._artists = []

        for a in animated_artists:
            self.add_artist(a)
        # grab the background on every draw
        self.cid = canvas.mpl_connect("draw_event", self.on_draw)

    def on_draw(self, event):
        """Callback to register with 'draw_event'."""
        cv = self.canvas
        if event is not None:
            if event.canvas != cv:
                raise RuntimeError
        self._bg = cv.copy_from_bbox(cv.figure.bbox)
        self._draw_animated()

    def add_artist(self, art):
        """Add an artist to be managed.

        Parameters
        ----------
        art : Artist
            The artist to be added. Will be set to 'animated' (just
            to be safe). *art* must be in the figure associated with
            the canvas this class is managing.

        """
        if art.figure != self.canvas.figure:
            raise RuntimeError
        art.set_animated(True)
        self._artists.append(art)

    def _draw_animated(self):
        """Draw all of the animated artists."""
        fig = self.canvas.figure
        for a in self._artists:
            fig.draw_artist(a)

    def update(self):
        """Update the screen with animated artists."""
        cv = self.canvas
        fig = cv.figure
        # paranoia in case we missed the draw event,
        if self._bg is None:
            self.on_draw(None)
        else:
            # restore the background
            cv.restore_region(self._bg)
            # draw all of the animated artists
            self._draw_animated()
            # update the GUI state
            cv.blit(fig.bbox)
        # let the GUI event loop process anything it has to do
        cv.flush_events()


def _to_corner_coords(index: pd.Index) -> np.ndarray:
    """Helper function to transform N coordinates pointing at centers of bins to N+1 coords pointing to the edges"""
    coords = index.values

    delta = coords[-1] - coords[-2]

    return np.concatenate((coords, [coords[-1] + delta])) - delta / 2


def _data_hash(*args: np.ndarray) -> int:
    return hash(tuple(arg.tobytes() for arg in args))


@contextmanager
def changed_plotting_backend(backend='agg'):
    """ This decorator/context manager wraps a function to temporarily use the agg backend for matplotlib.

    This class wraps functions to use the agg backend for matplotlib plots. It saves the previously chosen backend,
    sets agg as the backend, runs the wrapped function, and then sets the backend back to what it was previously. The
    standard backend leaks memory, thus switching to agg is advantageous if one only want to savefig things.
    """
    original_backend = mpl.get_backend()
    plt.switch_backend(backend)
    try:
        yield
    finally:
        plt.switch_backend(original_backend)


def plot_2d_dataframe(df: pd.DataFrame,
                      ax: plt.Axes = None, square=True,
                      column=None, index_is_y=True,
                      update_mode: str = 'auto',
                      colorbar_kwargs: Mapping[str, Any] = None,
                      pcolormesh_kwargs: Mapping[str, Any] = None,
                      colorbar_powerlimits: Tuple[int, int] = None) -> plt.Axes:
    """Plot pandas data frames using pcolormesh. This function expects numeric labels and it can update an existing
    plot. Have a look at seaborn.heatmap if you need something else.

    'auto': 'rescale' if x-label, y-label, and title are the same else 'clear'
    'clear': Clear axis before drawing
    'overwrite': Just plot new data frame on top (no colorbar is drawn)
    'rescale': Recalculate and redraw the colorbar

    Details:
     - plotted meshes are stored in ax.meshes
     - The colorbar is stored in ax.custom_colorbar (DO NOT RELY ON THIS)
     - If the plotted data is already present we just shift it to the top using set_zorder
     - Uses _data_hash(x, y, c) to identify previously plotted data

    :param df: pandas dataframe to plot
    :param ax: Axes object
    :param square:
    :param column: Select this column from the dataframe and unstack the index
    :param index_is_y: If true the index are on the y-axis and the columns on the x-axis
    :param update_mode: 'auto',  'overwrite' or 'rescale'
    :param colorbar_kwargs: passed to plt.colorbar
    :param pcolormesh_kwargs: passed to plt.pcolormesh
    :param colorbar_powerlimits: passed to `colorbar.formatter.set_powerlimits` if not None. Pass (0, 0) to enforce scientific notation
    :return:
    """
    if ax is None:
        ax = plt.gca()

    if square:
        ax.set_aspect("equal")

    if column is None and len(df.columns) == 1 and len(df.index.levshape) == 2:
        column = df.columns[0]

    if column is not None:
        title = column
        series = df[column]
        df = series.unstack()

    else:
        title = None

    colorbar_kwargs = colorbar_kwargs or {}
    pcolormesh_kwargs = pcolormesh_kwargs or {}

    c = df.values
    x_idx = df.columns
    y_idx = df.index

    if not index_is_y:
        c = np.transpose(c)
        x_idx, y_idx = y_idx, x_idx

    x_label = x_idx.name
    y_label = y_idx.name

    if update_mode == 'auto':
        if (x_label, y_label, title) == (ax.get_xlabel(), ax.get_ylabel(), ax.get_title()):
            update_mode = 'rescale'
        else:
            update_mode = 'clear'
    if update_mode not in ('clear', 'rescale', 'overwrite'):
        raise ValueError('%s is an invalid value for update_mode' % update_mode)

    if update_mode == 'clear':
        if hasattr(ax, 'custom_colorbar'):
            # clear colorbar axis
            ax.custom_colorbar.ax.clear()
        ax.clear()
        ax.meshes = WeakValueDictionary()

    y = _to_corner_coords(y_idx)
    x = _to_corner_coords(x_idx)

    if not hasattr(ax, 'meshes'):
        ax.meshes = WeakValueDictionary()

    df_hash = _data_hash(x, y, c)
    current_mesh = ax.meshes.get(df_hash, None)

    if current_mesh is None:
        # data not yet drawn -> draw it
        current_mesh = ax.pcolormesh(x, y, c, **pcolormesh_kwargs)
        ax.meshes[df_hash] = current_mesh

    # push to foreground
    max_z = max(mesh.get_zorder() for mesh in ax.meshes.values()) if ax.meshes else 0
    current_mesh.set_zorder(max_z + 1)

    if update_mode != 'overwrite':
        all_data = [mesh.get_array()
                    for mesh in ax.meshes.values()]
        vmin = min(map(np.min, all_data))
        vmax = max(map(np.max, all_data))

        if not hasattr(ax, 'custom_colorbar'):
            ax.custom_colorbar = plt.colorbar(ax=ax, mappable=current_mesh, **colorbar_kwargs)
            if colorbar_powerlimits:
                ax.custom_colorbar.formatter.set_powerlimits(colorbar_powerlimits)

        for mesh in ax.meshes.values():
            mesh.set_clim(vmin, vmax)

        try:
            ax.custom_colorbar.set_clim(vmin, vmax)
        except AttributeError:
            ax.custom_colorbar.mappable.set_clim(vmin, vmax)

    else:
        # TODO: fix
        warnings.warn("for update_mode='overwrite' the colorbar code is stupid")

    ax.set(ylabel=y_label, xlabel=x_label, title=title)

    return ax


def update_plot(handle, data):
    """Update a plot.

    Parameters
    ----------
    handle: matplotlib data handle
        The plot object that is updated. For instance, a lines.Line2D or
        image.AxesImage object.
    *data: Sequence
        New data to plot.
            - for line plots: [xdata, ydata]
            - for image plots: imdata (m x n array)

    """
    handle.set_data(data)
    if hasattr(handle, 'colorbar'):
        handle.colorbar.set_array(data)
        handle.colorbar.changed()
        handle.colorbar.autoscale()
        handle.colorbar.draw_all()

    # Rescale
    handle.axes.relim()
    handle.axes.autoscale_view()
    # We need to draw *and* flush
    handle.figure.canvas.draw()
    handle.figure.canvas.flush_events()


def cycle_plots(plot_callback, *args,
                fig: plt.Figure = None, ax: plt.Axes = None, **kwargs) -> Tuple[plt.Figure, plt.Axes]:
    """Call ``plot_callback(fig, ax, curr_pos, *args, **kwargs)`` on each left/right arrow key press.
    Initially curr_pos = 0. The right arrow increases and the left arrow decreases the current position.
    There is no limit so you need to do the wraparound yourself if needed:

    >>> plot_data = [(x1, y1), (x2, y2), ...]  # doctest: +SKIP
    >>> def example_plot_callback(fig, ax, pos):  # doctest: +SKIP
    ...     idx = pos % len(plot_data)
    ...     ax.plot(*plot_data[idx])
    """
    def key_event(e):
        if e.key == "right":
            key_event.curr_pos += 1
        elif e.key == "left":
            key_event.curr_pos -= 1
        else:
            return
        plot_callback(fig, ax, key_event.curr_pos, *args, **kwargs)
        plt.draw_all()

    key_event.curr_pos = 0

    if fig is None:
        if ax is None:
            fig = plt.figure()
        else:
            fig = ax.get_figure()
    if ax is None:
        ax = fig.add_subplot(111)

    if isinstance(ax, np.ndarray):
        assert all(a in fig.axes for a in ax.flat)
    else:
        assert ax in fig.axes, "axes not in figure"

    fig.canvas.mpl_connect('key_press_event', key_event)

    plot_callback(fig, ax, key_event.curr_pos, *args, **kwargs)
    plt.draw_all()

    return fig, ax


def get_rwth_color_cycle(alpha: float = 1, exclude: Sequence[str] = None):
    """Get the default RWTH color cycle with an alpha channel.

    Parameters
    ----------
    alpha: float
        The alpha (transparency) value for the color cycle.
    exclude: sequence of str
        Exclude these colors. See RWTH_COLORS for all available keys.
        Yellow is a good choice to exclude.

    Example
    -------
    >>> from unittest import mock; plt = mock.MagicMock() # do no do in real code ;)
    >>> cycle_100 = get_rwth_color_cycle(1.)
    >>> cycle_50 = get_rwth_color_cycle(.5)
    >>> ax = plt.gca()
    >>> x = np.linspace(0, 2*np.pi, 51)
    >>> for i, (v100, v50) in enumerate(zip(cycle_100, cycle_50)):
    ...     ax.plot(x, np.sin(x) + i / len(cycle_100), lw=2, **v100)  # doctest: +SKIP
    ...     ax.plot(x, -np.sin(x) + i / len(cycle_50), lw=2, **v50)   # doctest: +SKIP
    ...     pass

    See Also
    --------
    https://matplotlib.org/stable/tutorials/intermediate/color_cycle.html

    https://matplotlib.org/cycler/
    """
    if alpha < 0 or alpha > 1:
        raise ValueError('alpha should be in the range [0, 1].')

    exclude = exclude or []
    return cycler(color=[tup + (alpha,) for name, tup in RWTH_COLORS.items()
                         if name not in exclude])


rwth_color_cycle_25 = get_rwth_color_cycle(.25)
rwth_color_cycle_50 = get_rwth_color_cycle(.5)
rwth_color_cycle_75 = get_rwth_color_cycle(.75)
rwth_color_cycle_100 = get_rwth_color_cycle(1)
rwth_color_cycle = rwth_color_cycle_100


def list_styles(include_matplotlib_styles: bool = False) -> List[str]:
    """List available matplotlib styles.

    Parameters
    ----------
    include_matplotlib_styles : bool, default False
        Include the default styles that ship with ``matplotlib`` as well
        as the custom styles in the matplotlib config directory. If
        False, only the custom styles defined in this module are
        listed.

    Returns
    -------
    styles : list[str]
        The styles such that ``plt.style.use(style)`` works for all
        ``style`` in ``styles``.
    """
    custom_styles = []
    root_path = pathlib.Path(__file__).parents[1]
    for file in (root_path / 'plotting').glob('*.mplstyle'):
        file = file.relative_to(root_path.parent)
        style = '.'.join(file.parent.parts + (file.stem,))
        custom_styles.append(style)

    if include_matplotlib_styles:
        return plt.style.available + custom_styles
    else:
        return custom_styles


@dataclasses.dataclass
class LaTeXPlotHelper:
    A4_SIZE_INCHES = (8.25, 11.75)

    textwidth_in_inches: float = dataclasses.field(default=0.9 * A4_SIZE_INCHES[0])

    def scale_relative_textwidth(self, fig, width: float, height: Union[bool, float] = False):
        if isinstance(fig, int):
            fig = plt.figure(fig)

        old_w, old_h = fig.get_size_inches()
        new_w = self.textwidth_in_inches * width
        if isinstance(height, float):
            new_h = self.textwidth_in_inches * height
        else:
            new_h = old_h * (new_w / old_h) if height else old_h
        fig.set_size_inches(new_w, new_h)

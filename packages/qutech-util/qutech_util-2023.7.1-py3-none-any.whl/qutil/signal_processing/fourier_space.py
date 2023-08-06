"""This module contains signal processing functions that work on data in
frequency space. For consistency, functions in this module should have
the data to be processed as first and the frequencies at which the data
is sampled as their second argument, while always returning a tuple of
(possibly processed) frequencies and processed data, i.e.::

    def fun(data, f, *args, **kwargs) -> processed_data, processed_f:
        ...

"""
import inspect
from typing import Literal, Tuple, TypeVar, Optional

import numpy as np
from scipy import integrate

from qutil import linalg
from qutil.functools import wraps
from qutil.linalg import abs2
from qutil.typecheck import check_literals

try:
    import numba as nb
    numba = True
except ImportError:
    numba = False

_S = TypeVar('_S')
_T = TypeVar('_T')


def _standardize(function):
    """Adds variadic kwargs and f arg and return param."""
    try:
        parameters = inspect.signature(function).parameters
        assert 'f' not in parameters, \
            'Only use this decorator for functions without parameter named f'
        assert not any(p.kind is inspect.Parameter.VAR_KEYWORD for _, p in parameters.items()), \
            'Only use this decorator for functions without variadic keyword arguments.'
    except ValueError:
        # ufunc, https://numpy.org/doc/stable/reference/ufuncs.html#ufuncs-kwargs
        parameters = {'out', 'where', 'axes', 'axis', 'keepdims', 'casting', 'order', 'dtype',
                      'subok', 'signature', 'extobj'}

    @wraps(function)
    def wrapper(x, f, *args, **kwargs):
        # Filter kwargs that function actually accepts
        kwargs = {k: v for k, v in kwargs.items() if k in parameters}
        return function(x, *args, **kwargs), f

    return wrapper


def Id(x: _S, f: _T, *_, **__) -> Tuple[_S, _T]:
    """The identity mapping."""
    return x, f


def derivative(x, f, deriv_order: int = 0, **_) -> Tuple[np.ndarray, np.ndarray]:
    """Perform (anti-)derivatives.

    .. note::
        For negative antiderivatives, the zero-frequency component is
        set to zero (due to zero-division).

    Parameters
    ----------
    x : array_like
        The data to be filtered.
    f : array_like
        Frequencies corresponding to the last axis of `x`.
    deriv_order : int
        The order of the derivative. If negative, the antiderivative is
        computed (indefinite integral). Default: 0.
    """
    f = np.asanyarray(f)
    with np.errstate(invalid='ignore', divide='ignore'):
        xp = np.asanyarray(x)*(2*np.pi*f)**deriv_order
    if deriv_order < 0:
        xp[..., (f == 0).nonzero()] = 0
    return xp, f


def rms(x, f, /, out=None, *, axis: Optional[int] = None, where=True, dtype=None, keepdims=False,
        **_) -> Tuple[np.ndarray, np.ndarray]:
    """Compute the RMS (root-mean-square).

    See :class:`numpy.ufunc` and the `NumPy reference`_ for
    documentation of the arguments.

    .. _NumPy reference: https://numpy.org/doc/stable/reference/ufuncs.html

    Examples
    --------
    >>> t = np.linspace(0, 1, 1001)
    >>> x = 2*np.sqrt(2)*np.sin(2*np.pi*10*t)
    >>> xf = np.fft.fft(x)  # nb rfft would need to be scaled by factor √2
    >>> r, _ = rms(xf, ...)  # f not actually needed
    >>> r  # doctest: +ELLIPSIS
    1.9990007493755...
    >>> np.allclose(r, np.sqrt(x.mean()**2 + x.var()))
    True
    """
    x = np.asanyarray(x)
    N = np.take(x.shape, axis or range(x.ndim)).prod()

    result = linalg.abs2(x, where=where, dtype=dtype)
    result = np.sum(result, axis=axis, dtype=dtype, out=out, keepdims=keepdims, where=where)
    result = np.sqrt(result, out=out, dtype=dtype)
    result /= N
    return result, f


if numba:
    # nb.guvectorize generates gufuncs with all the kwargs, so only work and result array required.
    def _rms(x, res):
        res[0] = 0
        if np.iscomplexobj(x):
            for i in range(x.shape[0]):
                xx = x[i]
                real = xx.real
                imag = xx.imag
                res += real * real + imag * imag
        else:
            for i in range(x.shape[0]):
                real = x[i].real
                res += real * real
        res[0] = np.sqrt(res[0]) / x.shape[0]

    _rms.__doc__ = rms.__doc__
    rms = _standardize(
        nb.guvectorize([(nb.float32[:], nb.float32[:]),
                        (nb.float64[:], nb.float64[:]),
                        (nb.complex64[:], nb.float32[:]),
                        (nb.complex128[:], nb.float64[:])],
                       '(n)->()',
                       target='parallel',
                       cache=True)(_rms)
    )


def brickwall_filter(x, f, f_min: float = 0, f_max: float = np.inf, **_) -> Tuple[np.ndarray,
                                                                                  np.ndarray]:
    """Apply a brick wall filter to the data.

    Parameters
    ----------
    x : array_like
        The data to be filtered.
    f : array_like
        Frequencies corresponding to the last axis of `x`.
    f_min, f_max : float
        The locations of the brick walls for (low-, band-, high-)pass
        filtering.
    """
    f = np.asanyarray(f)
    xp = np.copy(x)
    xp[..., (f < f_min) | (f > f_max)] = 0
    return xp, f


@check_literals
def octave_band_rms(x, f, base: Literal[2, 10] = 10, fraction: int = 1,
                    return_band_edges: bool = False, **_) -> Tuple[np.ndarray, np.ndarray]:
    """Compute the rms over octave fractions [1]_, [2]_.

    Parameters
    ----------
    x : ndarray, shape (..., n_freq)
        The amplitude spectral density to compute the rms from.
        (I.e., the frequency-domain data).
    f : ndarray, shape (n_freq,)
        The frequencies corresponding to the data x.
    base : 2 or 10
        The logarithm base for the octaves.
    fraction : int
        The denominator of the fraction of an octave band to use for
        the calculation.
    return_band_edges : bool
        Return the edges instead of the midband frequencies.

    Returns
    -------
    octave_band_rms : ndarray
        The rms values.
    bandedge_frequencies : ndarray
        The frequencies of the octave band edges
        (if return_band_edges is true).
    midband_frequencies : ndarray
        The midband frequencies of the octave bands.
        (if return_band_edges is false).

    References
    ----------
    .. [1] C. G. Gordon, “Generic vibration criteria for vibration-
       sensitive equipment”, in Optomechanical Engineering and
       Vibration Control, Vol. 3786 (Sept. 28, 1999), pp. 22–33.
       https://www.spiedigitallibrary.org/conference-proceedings-of-spie/3786/0000/Generic-vibration-criteria-for-vibration-sensitive-equipment/10.1117/12.363802.short
    .. [2] ANSI/ASA S1.11-2004 (R2009). Octave-Band and Fractional-
       Octave-Band Analog and Digital Filters.
       https://webstore.ansi.org/standards/asa/ansiasas1112004r2009
    """
    mask = f > 0
    f = f[mask]
    x = abs2(x[..., mask])
    df = f[1] - f[0]

    # Computed according to ANSI S1.11-2004
    reference_frequency = 1000
    frequency_ratio = 10**0.3 if base == 10 else 2
    # Compute the band index x from the frequencies given
    # and then calculate back the midband frequencies
    if fraction % 2:
        bmin = fraction*np.log(f.min()/reference_frequency)/np.log(frequency_ratio) + 30
        bmax = fraction*np.log(f.max()/reference_frequency)/np.log(frequency_ratio) + 30
        band_index = np.arange(np.ceil(bmin), np.ceil(bmax))
        midband_frequencies = reference_frequency*frequency_ratio**((band_index - 30)/fraction)
    else:
        bmin = (2*fraction*np.log(f.min()/reference_frequency)/np.log(frequency_ratio) + 59)/2
        bmax = (2*fraction*np.log(f.max()/reference_frequency)/np.log(frequency_ratio) + 59)/2
        band_index = np.arange(np.ceil(bmin), np.ceil(bmax))
        midband_frequencies = reference_frequency*frequency_ratio**((2*band_index - 59)/2/fraction)

    bandedge_frequencies = (midband_frequencies[:, None]
                            * frequency_ratio**(np.array([-1, 1])/2/fraction))
    bandwidths = np.diff(bandedge_frequencies)[:, 0]

    # drop bands for which the frequency resolution is too low to integrate
    mask = 2*df < bandwidths
    midband_frequencies = midband_frequencies[mask]
    bandedge_frequencies = bandedge_frequencies[mask, :]

    mean_square = np.empty(x.shape[:-1] + midband_frequencies.shape)
    for i, (f_lower, f_upper) in enumerate(bandedge_frequencies):
        mask = (f_lower <= f) & (f <= f_upper)
        mean_square[..., i] = integrate.trapezoid(x[..., mask], f[..., mask])

    if return_band_edges:
        return np.sqrt(mean_square), bandedge_frequencies
    else:
        return np.sqrt(mean_square), midband_frequencies

"""This module contains signal processing functions that work on data in
real space. For consistency, functions in this module should have the
data to be processed as their first argument while the processed data
should be the sole return argument, i.e.::

    def fun(data, *args, **kwargs) -> processed_data:
        ...

"""
import inspect
import warnings
from typing import Optional, Sequence, Callable, Union, Tuple, Literal, TypeVar

import numpy as np
from scipy import signal, fft

from qutil import linalg
from qutil.functools import chain, partial, wraps
from qutil.signal_processing import fourier_space
from qutil.typecheck import check_literals

# TODO: replace unsupported imports
try:
    from scipy.signal.spectral import _median_bias, _triage_segments
except ImportError:
    from scipy.signal._spectral_py import _median_bias, _triage_segments

try:
    import numba as nb
    numba = True
except ImportError:
    numba = False

_T = TypeVar('_T')


def _standardize(function):
    """Adds variadic kwargs."""
    try:
        parameters = inspect.signature(function).parameters
    except ValueError:
        # ufunc, https://numpy.org/doc/stable/reference/ufuncs.html#ufuncs-kwargs
        parameters = {'out', 'where', 'axes', 'axis', 'keepdims', 'casting', 'order', 'dtype',
                      'subok', 'signature', 'extobj'}

    @wraps(function)
    def wrapper(x, *args, **kwargs):
        # Filter kwargs that function actually accepts
        kwargs = {k: v for k, v in kwargs.items() if k in parameters}
        return function(x, *args, **kwargs)

    return wrapper


def Id(x: _T, *_, **__) -> _T:
    """The identity mapping."""
    return x


def rms(x, /, out=None, *, axis: Optional[int] = None, where=True, dtype=None, keepdims=False,
        **_) -> np.ndarray:
    """Compute the RMS (root-mean-square).

    See :class:`numpy.ufunc` and the `NumPy reference`_ for
    documentation of the arguments.

    .. _NumPy reference: https://numpy.org/doc/stable/reference/ufuncs.html

    Examples
    --------
    >>> t = np.linspace(0, 2*np.pi, 1001)
    >>> x = 2*np.sqrt(2)*np.sin(t)
    >>> r = rms(x)
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
    result /= np.sqrt(N)
    return result


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
        res[0] = np.sqrt(res[0] / x.shape[0])

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


@check_literals
def butter_filter(x, fs: float, order: int = 5,
                  btype: Literal['lowpass', 'highpass', 'bandpass'] = 'bandpass', f_min: float = 0,
                  f_max: float = np.inf, **_) -> np.ndarray:
    """Apply a digital Butter filter to the data.

    This function provides a simplified interface to SciPy's `signal`
    functionality by abstracting away some of the API.

    Parameters
    ----------
    x : array_like
        The data to be filtered.
    fs : float
        Sample frequency.
    order : int
        The filter order. Default: 5.
    btype : str
        The filter type. {'bandpass', 'highpass', 'lowpass'}.
    f_min, f_max : float
        The edges for (low-, band-, high-)pass filtering.

    See Also
    --------
    :func:`scipy.signal.butter`
    :func:`scipy.signal.sosfilt`
    """
    if btype == 'lowpass':
        cutoff = f_max
    elif btype == 'highpass':
        cutoff = f_min
    elif btype == 'bandpass':
        cutoff = [f_min, f_max]
    else:
        raise ValueError('Expected btype to be one of {lowpass, highpass, bandpass} but got '
                         f'{btype}')
    return signal.sosfilt(signal.butter(order, cutoff, btype, analog=False, output='sos', fs=fs),
                          x)


def welch(x, fourier_procfn: Optional[Union[Callable, Sequence[Callable]]] = None, fs: float = 1.0,
          window: Union[str, Tuple[np.ndarray, ...]] = 'hann', nperseg: Optional[int] = None,
          noverlap: Optional[int] = None, nfft: Optional[int] = None,
          detrend: Union[str, Callable] = 'constant', normalize: Union[bool, Callable] = False,
          return_onesided: Optional[bool] = None, scaling: str = 'density', axis: int = -1,
          average: str = 'mean', workers: Optional[int] = None,
          **settings) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Use Welch's method to estimate the power spectral density.

    Adapted from :mod:`scipy.signal.spectral`, so see that module for
    parameter explanations.

    Unlike the SciPy version, this function allows to perform an
    additional processing step on the Fourier transform of the time data
    ``x``. This is done by applying ``fourier_procfn`` to the FFT'd data
    before the PSD is estimated. ``fourier_procfn`` should be a
    (sequence of) callable(s) with the following signature::

        fourier_procfn(Fx, f, **settings) -> Fxp, fp

    The function defaults to the identity map, so should reproduce the
    SciPy result. If a sequence, functions are applied from left to
    right, i.e., if ``fourier_procfn = [a, b, c]``, then they are
    applied as ``c(b(a(Fx, f, **s), f, **s, f, **s)``.

    By default, the twosided spectrum is computed if x is complex, and
    the transformed data are shifted using :func:`~np.fft.fftshift` so
    that they are ordered by monotonously increasing frequencies.

    Parameters
    ----------
    The following parameters are not present in the scipy function:

    fourier_procfn : callable or sequence thereof
        A processing function that acts on the Fourier-transformed
        data (see above).
    normalize : callable or bool, default: False
        Similar to `detrend`, this can be used to normalize each Welch
        segment with some function. If True, the data is normalized by
        its standard deviation (corresponding to the RMS by default as
        the normalization is performed after detrending). This can be
        useful if one wants to compare spectra qualitatively.
    workers : int, optional
        The workers parameter of :func:`scipy:scipy.fft.fft`.

    Returns
    -------
    PSD : ndarray
        The power spectral density.
    f : ndarray
        The discrete FFT frequencies.
    ifft : ndarray
        The timeseries data after processing in Fourier space.

    Examples
    --------
    Same as :func:`scipy.signal.welch` for no fourier_procfn:

    >>> from scipy import signal
    >>> rng = np.random.default_rng()
    >>> x = rng.standard_normal((10, 3, 500))
    >>> np.array_equal(signal.welch(x)[1], welch(x)[0])  # returned arguments switched around
    True

    Spectrum of differentiated signal:

    >>> def derivative(x, f, **_):
    ...     return x*2*np.pi*f, f
    >>> S, f, dxdt = welch(x, fourier_procfn=derivative)

    Compare to spectrum of numerical derivative:

    >>> import matplotlib.pyplot as plt
    >>> Sn, fn, dxdtn = welch(np.gradient(x, axis=-1))
    >>> lines = plt.loglog(f, S.mean((0, 1)), fn, Sn.mean((0, 1)))
    """
    if np.iterable(fourier_procfn):
        fourier_procfn = chain(*fourier_procfn, n_args=2)
    else:
        fourier_procfn = chain(fourier_procfn or fourier_space.Id, n_args=2)

    # Default to twosided if x is complex
    return_onesided = return_onesided or not np.iscomplexobj(x)

    axis = int(axis)
    # Ensure we have np.arrays, get outdtype
    # outdtype cannot be complex since we only calculate autocorrelations here.
    x = np.asarray(x)
    outdtype = np.result_type(x.real, np.float32)

    if x.size == 0:
        return (np.empty(x.shape, dtype=outdtype),
                np.empty(x.shape, dtype=outdtype),
                np.empty(x.shape, dtype=outdtype))

    if x.ndim > 1 and axis != -1:
        x = np.moveaxis(x, axis, -1)

    if nperseg is not None:  # if specified by user
        nperseg = int(nperseg)
        if nperseg < 1:
            raise ValueError('nperseg must be a positive integer')

    # parse window; if array like, then set nperseg = win.shape
    win, nperseg = _triage_segments(window, nperseg, input_length=x.shape[-1])

    if nfft is None:
        nfft = nperseg
    elif nfft < nperseg:
        raise ValueError('nfft must be greater than or equal to nperseg.')
    else:
        nfft = int(nfft)

    if noverlap is None:
        noverlap = nperseg//2
    else:
        noverlap = int(noverlap)
    if noverlap >= nperseg:
        raise ValueError('noverlap must be less than nperseg.')

    # Handle detrending and window functions
    if not detrend:
        def detrend_func(d):
            return d
    elif not callable(detrend):
        def detrend_func(d):
            return signal.detrend(d, type=detrend, axis=-1)
    elif axis != -1:
        # Wrap this function so that it receives a shape that it could
        # reasonably expect to receive.
        def detrend_func(d):
            d = np.moveaxis(d, -1, axis)
            d = detrend(d)
            return np.moveaxis(d, axis, -1)
    else:
        detrend_func = detrend

    if not normalize:
        def normalize_func(d):
            return d
    elif not callable(normalize):
        def normalize_func(d):
            # RMS normalization. Assumes detrend has already removed a constant trend.
            return d / rms(d, axis=-1, keepdims=True)
    elif axis != -1:
        def normalize_func(d):
            d = np.moveaxis(d, -1, axis)
            d = normalize(d)
            return np.moveaxis(d, axis, -1)
    else:
        normalize_func = normalize

    if np.result_type(win, np.float32) != outdtype:
        win = win.astype(outdtype)

    if scaling == 'density':
        scale = 1.0 / (fs * (win*win).sum())
    elif scaling == 'spectrum':
        scale = 1.0 / win.sum()**2
    else:
        raise ValueError('Unknown scaling: %r' % scaling)

    if return_onesided:
        if np.iscomplexobj(x):
            sides = 'twosided'
            warnings.warn('Input data is complex, switching to '
                          'return_onesided=False')
        else:
            sides = 'onesided'
    else:
        sides = 'twosided'

    if sides == 'twosided':
        freqs_func = chain(partial(fft.fftfreq, d=1/fs), partial(fft.fftshift, axes=-1))
        fft_func = chain(_fft_helper, partial(fft.fftshift, axes=-1), inspect_kwargs=True)
        ifft_func = chain(partial(fft.ifftshift, axes=-1), fft.ifft)
    else:
        # sides == 'onesided'
        freqs_func = partial(fft.rfftfreq, d=1/fs)
        fft_func = _fft_helper
        ifft_func = fft.irfft

    freqs = freqs_func(nfft)

    # Perform the windowed FFTs. Need to pass kwargs so that FunctionChain can pass on only those
    # that are allowed for each function
    result = fft_func(x, win=win, detrend_func=detrend_func, normalize_func=normalize_func,
                      nperseg=nperseg, noverlap=noverlap, nfft=nfft, sides=sides, workers=workers)

    # Do custom stuff with the Fourier transformed data
    result, freqs = fourier_procfn(result, freqs, **settings)

    # Absolute value square and scaling to get the PSD
    result = scale * linalg.abs2(result)

    if sides == 'onesided':
        if nfft % 2:
            result[..., 1:] *= 2
        else:
            # Last point is unpaired Nyquist freq point, don't double
            result[..., 1:-1] *= 2

    # Inverse fft for processed time series data (not averaged over Welch segments)
    if not all(fp is fourier_space.Id for fp in fourier_procfn.functions):
        y, _ = fourier_procfn(
            # Basically just fft.fft or fft.rfft
            fft_func(
                x, win=1, detrend_func=Id, normalize_func=Id, nperseg=x.shape[-1], noverlap=0,
                nfft=x.shape[-1], sides=sides, workers=workers
            )[..., 0, :],
            freqs_func(x.shape[-1]),
            **settings
        )
        ifft = np.moveaxis(ifft_func(y, workers=workers), -1, axis)
    else:
        ifft = np.moveaxis(x, -1, axis)

    result = result.astype(outdtype)

    # Output is going to have new last axis for time/window index, so a
    # negative axis index shifts down one
    if axis < 0:
        axis -= 1

    # Roll frequency axis back to axis where the data came from
    result = np.moveaxis(result, -1, axis)

    # Average over windows.
    if len(result.shape) >= 2 and result.size > 0:
        if result.shape[-1] > 1:
            if average == 'median':
                # np.median must be passed real arrays for the desired result
                bias = _median_bias(result.shape[-1])
                if np.iscomplexobj(result):
                    result = (np.median(np.real(result), axis=-1)
                              + 1j * np.median(np.imag(result), axis=-1))
                else:
                    result = np.median(result, axis=-1)
                result /= bias
            elif average == 'mean':
                result = result.mean(axis=-1)
            else:
                raise ValueError('average must be "median" or "mean", got %s'
                                 % (average,))
        else:
            result = np.reshape(result, result.shape[:-1])

    return result, freqs, ifft


def _fft_helper(x, win, detrend_func, normalize_func, nperseg, noverlap, nfft, sides, workers):
    """
    Calculate windowed FFT, for internal use by
    `scipy.signal._spectral_helper`.

    This is a helper function that does the main FFT calculation for
    `_spectral helper`. All input validation is performed there, and the
    data axis is assumed to be the last axis of x. It is not designed to
    be called externally. The windows are not averaged over; the result
    from each window is returned.

    Returns
    -------
    result : ndarray
        Array of FFT data

    Notes
    -----
    Adapted from matplotlib.mlab
    Then adapted from scipy.signal

    .. versionadded:: 0.16.0
    """
    # Created strided array of data segments
    if nperseg == 1 and noverlap == 0:
        result = x[..., np.newaxis]
    else:
        # https://stackoverflow.com/a/5568169
        step = nperseg - noverlap
        shape = x.shape[:-1]+((x.shape[-1]-noverlap)//step, nperseg)
        strides = x.strides[:-1]+(step*x.strides[-1], x.strides[-1])
        result = np.lib.stride_tricks.as_strided(x, shape=shape,
                                                 strides=strides)

    # Detrend and normalize each data segment individually
    result = normalize_func(detrend_func(result))

    # Apply window by multiplication
    result *= win

    # Perform the fft. Acts on last axis by default. Zero-pads automatically
    if sides == 'twosided':
        func = fft.fft
    else:
        result = result.real
        func = fft.rfft

    return func(result, n=nfft, workers=workers)

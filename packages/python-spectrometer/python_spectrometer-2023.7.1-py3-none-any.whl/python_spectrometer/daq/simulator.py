"""Provides a simulation backend for data acquisition."""
from __future__ import annotations

import dataclasses
from typing import Callable, Iterator

import numpy as np
from python_spectrometer.daq.core import DAQ
from qutil.functools import partial

try:
    from numpy.typing import NDArray
except ImportError:
    from numpy import ndarray as NDArray

try:
    import qopt
except ImportError as e:
    raise ImportError('This simulated DAQ requires qopt. You can install it by running '
                      "'pip install qopt.'") from e


@dataclasses.dataclass
class QoptColoredNoise(DAQ):
    """Simulates noise using :mod:`qopt:qopt`.

    See :class:`~python_spectrometer.core.Spectrometer` for
    more details on usage and
    :class:`~python_spectrometer.daq.settings.DAQSettings`
    for more information on setup parameters.

    Parameters
    ----------
    spectral_density : Callable, optional
        A callable with signature::

            f(ndarray, **settings) -> ndarray

        that returns the power spectral density for given frequencies.
        Defaults to white noise with scale parameter ``S_0``.

    See Also
    --------
    :func:`qopt:qopt.noise.fast_colored_noise`
        For information on the simulation.

    """
    spectral_density: Callable[[NDArray, ...], NDArray] = dataclasses.field(
        default_factory=lambda: QoptColoredNoise.white_noise
    )

    @staticmethod
    def white_noise(f, S_0: float = 1.0, **_) -> NDArray:
        """White noise power spectral density with amplitude S_0."""
        return np.full_like(f, S_0)

    def acquire(self, *, n_avg: int, fs: float, n_pts: int, **settings) -> Iterator[NDArray]:
        """Executes a measurement and yields the resulting timetrace."""
        for _ in range(n_avg):
            yield qopt.noise.fast_colored_noise(
                partial(
                    settings.get('spectral_density', self.spectral_density),
                    **settings
                ),
                dt=1/fs, n_samples=n_pts, output_shape=()
            )
        # This is the place to return metadata (possibly obtained from the instrument)
        return {'qopt_version': qopt.__version__}


# Alias for backwards compatibility only.
qopt_colored_noise = QoptColoredNoise

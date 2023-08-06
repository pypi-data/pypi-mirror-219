"""This module provides the :class:`~.Spectrometer` class for
spectrum estimation using general-purpose acquisition hardware. The
class manages the acquisition, processing, as well as displaying of
acquired data.

An object of the :class:`~.Spectrometer` class is instantiated with an
instance of the :class:`~daq.core.DAQ` class which implements thin
wrappers around hardware drivers in :mod:`.daq` by means of its
:meth:`~daq.core.DAQ.setup` and :meth:`~daq.core.DAQ.acquire` methods.
Conceptually, :meth:`~daq.core.DAQ.setup` should configure the hardware
for data acquisition given a dictionary of settings, while
:meth:`~daq.core.DAQ.acquire()` should execute said acquisition and
yield an array of data when iterated. Furthermore, a custom estimator
for the power spectral density can be supplied, which could for instance
perform some processing of the Fourier-transformed data before computing
the spectrum using the conventional Welch's method, or use some other
method of spectral estimation.

To give a better idea of what these functions should do without delving
into the source code, we outline how to implement them for the example
of a vibration measurement here. Assume the measurement device outputs
a voltage that is proportional to the acceleration, and we would like
to obtain the displacement spectrum::

    from qutil.signal_processing.real_space import welch
    from python_spectrometer.daq import DAQ

    def psd_estimator(taccel, **settings):
        '''PSD estimator for displacement profile from acceleration.'''
        def accel_to_displ(a, f, **settings):
            # Integration in Fourier space corresponds to division by ω
            return a/(2*np.pi*f)**2
        return welch(taccel, fourier_procfn=accel_to_displ), f

    class MyDAQ(DAQ):
        # daq is the actual device driver
        daq: object

        def setup(self, **settings):
            # Configure the hardware through some driver representing
            # the device by the daq object.
            daq.setup(...)
            # We may modify settings here, for instance to account for
            # hardware constraints.
            return settings

        def acquire(self, **settings):
            for _ in settings.get('n_avg', 1):
                yield daq.measure()  # yields ndarray with data
            return metadata  # optionally returns metadata

We can then instantiate a :class:`~core.Spectrometer` object like so::

    from python_spectrometer import Spectrometer

    spect = Spectrometer(MyDAQ(daq), psd_estimator)

Spectra can then be acquired using the :meth:`~.Spectrometer.take`
method, which takes as arguments a comment to identify the spectrum by
as well as keyword-argument pairs of settings that are passed through
to :meth:`~daq.core.DAQ.setup`, :meth:`~daq.core.DAQ.acquire`, and
:func:`psd_estimator`::

    settings = {'f_max': 1234.5}
    spect.take('a comment', n_avg=5, **settings)

For the default PSD estimator
(:func:`qutil:qutil.signal_processing.real_space.welch`), a dictionary
subclass exists, :class:`daq.settings.DAQSettings`, which manages the
interdependencies of parameters for data acquisition. For example,
:attr:`~.daq.settings.DAQSettings.f_max` cannot be larger than half the
sampling rate :attr:`~.daq.settings.DAQSettings.fs` due to Nyquist's
theorem. See the class docstring for those special parameters.

Spectra can be hidden from the current display and shown again::

    spect.hide(0)
    spect.show('a comment')  # same as spect.show(0)

A run can also be serialized to disk and recalled at a later point::

    spect.serialize_to_disk('./foo')
    spect_loaded = Spectrometer.recall_from_disk('./foo')
    spect_loaded.print_keys()
    (0, 'a comment')
    spect_loaded.print_settings('a comment')
    Settings for key (0, 'a'):
    {...}

Finally, plot options can be changed dynamically at runtime::

    spect.plot_raw = True  # Updates the figure accordingly
    spect.plot_timetrace = False

See the documentation of :class:`~core.Spectrometer` and its methods
for more information.
"""
__version__ = '2023.7.1'

from . import daq
from .core import Spectrometer

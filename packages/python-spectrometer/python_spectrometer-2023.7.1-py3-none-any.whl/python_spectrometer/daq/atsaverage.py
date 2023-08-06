"""Use atsaverage to take spectra using Alazar cards.

Examples
--------
Set up and take a spectrum::

    from python_spectrometer import daq, Spectrometer
    from tempfile import mkdtemp
    from atsaverage import alazar
    from atsaverage.core import getLocalCard

    card = getLocalCard(1, 1)
    spect = Spectrometer(daq.atsaverage.AlazarATS9xx0(card, 0), savepath=mkdtemp())

    spect.take(fs=1e6, input_range=alazar.InputRangeID.range_100_mV)

"""
from __future__ import annotations

import dataclasses
import string
import time
from typing import Iterator, Type

from python_spectrometer.daq.core import DAQ
from python_spectrometer.daq.settings import DAQSettings
from qutil.domains import ReciprocalDiscreteInterval
from qutil.functools import cached_property
from qutil.misc import import_or_mock

try:
    from numpy.typing import NDArray
except ImportError:
    from numpy import array as NDArray

# Need to do ugly import mocking because pytest bypasses lazy imports during test discovery
locals().update(import_or_mock('atsaverage'))
locals().update(import_or_mock('atsaverage.core'))
locals().update(import_or_mock('atsaverage.masks', None, 'PeriodicMask'))
locals().update(import_or_mock('atsaverage.operations', None, 'Downsample'))
locals().update(import_or_mock('atsaverage.alazar', None, 'InputRangeID'))
for obj in ('BoardConfiguration', 'EngineTriggerConfiguration',
            'CaptureClockConfiguration', 'CaptureClockType', 'SampleRateID',
            'create_scanline_definition', 'InputConfiguration', 'Channel'):
    locals().update(import_or_mock('atsaverage.config2', None, obj))


@dataclasses.dataclass
class AlazarATS9xx0(DAQ):
    card: atsaverage.core.AlazarCard  # noqa
    hardware_channel: int | str | atsaverage.config2.Channel  # noqa
    trigger_callback: callable | str = 'software'

    def __post_init__(self):
        if isinstance(self.hardware_channel, int):
            self.hardware_channel = string.ascii_uppercase[self.hardware_channel]
        if not isinstance(self.hardware_channel, Channel):  # noqa
            self.hardware_channel = getattr(Channel, self.hardware_channel)  # noqa
        if self.trigger_callback == 'software':
            self.trigger_callback = self.card.forceTrigger
        else:
            raise NotImplementedError('Hardware trigger not yet implemented. Please open a PR.')

        self.default_capture_clock_config = CaptureClockConfiguration(  # noqa
            CaptureClockType.internal_clock,  # noqa
            SampleRateID.rate_100MSPS  # noqa
        )

    @cached_property
    def DAQSettings(self) -> Type[DAQSettings]:
        class AlazarDAQSettings(DAQSettings):
            @property
            def ALLOWED_FS(self) -> ReciprocalDiscreteInterval:
                return ReciprocalDiscreteInterval(
                    numerator=self['capture_clock_config'].get_numeric_sample_rate(),
                    precision=self.PRECISION
                )

        return AlazarDAQSettings

    def setup(self, fs: float = 100e6,
              capture_clock_config: CaptureClockConfiguration | None = None,  # noqa
              input_range: InputRangeID = InputRangeID.range_1_V,  # noqa
              **settings):
        settings = self.DAQSettings(
            fs=fs,
            capture_clock_config=capture_clock_config or self.default_capture_clock_config,
            input_range=input_range,
            **settings
        )

        hardware_sample_rate = settings.ALLOWED_FS.numerator
        # can round since settings.fs is guaranteed to be hardware_sample_rate divided by an int
        averaged_samples = round(hardware_sample_rate / settings.fs)
        assert averaged_samples > 0

        masks = [PeriodicMask("M",  # noqa
                              begin=0, end=averaged_samples, period=averaged_samples,
                              channel=self.hardware_channel, skip=0, take=settings.n_pts)]
        operations = [Downsample('M', 'M')]  # noqa
        board_spec = self.card.get_board_spec()

        board_config = BoardConfiguration(  # noqa
            trigger_engine=EngineTriggerConfiguration.software_trigger(),  # noqa
            capture_clock_configuration=settings['capture_clock_config'],
            input_configuration=InputConfiguration(self.hardware_channel,  # noqa
                                                   input_range=settings['input_range'])
        )

        scanline_definition = create_scanline_definition(  # noqa
            masks=masks,
            operations=operations,
            numeric_sample_rate=hardware_sample_rate,
            board_spec=board_spec,
            raw_data_mask=0,
        )

        self.card.apply_board_configuration(board_config)
        self.card.configureMeasurement(scanline_definition)
        self.card.acquisitionTimeout = settings.get(
            'acquisitionTimeout',  # ms...
            max(1000000, int(2 * 1000 * settings['n_pts'] / settings['fs']))
        )
        self.card.computationTimeout = settings.get('computationTimeout',
                                                    self.card.acquisitionTimeout)
        self.card.triggerTimeout = settings.get('triggerTimeout', self.card.acquisitionTimeout)

        return settings.to_consistent_dict()

    def acquire(self, *, n_avg: int, input_range: InputRangeID, **settings) -> Iterator[NDArray]:  # noqa
        self.card.startAcquisition(n_avg)

        for _ in range(n_avg):
            time.sleep(.05)
            self.trigger_callback()
            result = self.card.extractNextScanline()

            yield result.operationResults['M'].getAsVoltage(input_range)

        return self.card.get_board_spec()

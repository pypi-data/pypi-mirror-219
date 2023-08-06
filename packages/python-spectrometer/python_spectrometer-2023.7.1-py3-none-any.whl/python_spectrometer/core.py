import contextlib
import copy
import inspect
import os
import shelve
import warnings
from datetime import datetime
from pathlib import Path
from pprint import pprint
from typing import (Any, Callable, ContextManager, Dict, Generator, Iterable, Iterator, List,
                    Literal, Mapping, Optional, Sequence, Tuple, Union)
from unittest import mock

import dill
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import colors, gridspec
from qutil import io
from qutil.functools import cached_property, chain, partial
from qutil.itertools import compress, count
from qutil.misc import filter_warnings
from qutil.signal_processing.real_space import Id, welch
from qutil.typecheck import check_literals
from qutil.ui import progressbar
from scipy import integrate, signal

from python_spectrometer.daq import settings as daq_settings
from python_spectrometer.daq.core import DAQ

_keyT = Union[int, str, Tuple[int, str]]
_pathT = Union[str, os.PathLike]
_styleT = Union[str, os.PathLike, dict]
_styleT = Union[None, _styleT, List[_styleT]]


def _forward_property(cls: type, member: str, attr: str):
    def getter(self):
        return getattr(getattr(self, member), attr)

    def setter(self, val):
        return setattr(getattr(self, member), attr, val)

    return property(getter, setter, doc=getattr(cls, attr).__doc__)


class _PlotManager:
    PLOT_TYPES = ('main', 'cumulative', 'time')
    LINE_TYPES = ('processed', 'raw')

    def __init__(self, data: Dict[_keyT, Any], plot_raw: bool = False,
                 plot_timetrace: bool = False, plot_cumulative: bool = False,
                 plot_negative_frequencies: bool = True, plot_absolute_frequencies: bool = True,
                 plot_amplitude: bool = True, plot_density: bool = True,
                 plot_cumulative_normalized: bool = False, plot_style: _styleT = 'fast',
                 plot_update_mode: str = 'fast', plot_dB_scale: bool = False, prop_cycle=None,
                 raw_unit: str = 'V', processed_unit: str = 'V',
                 uses_windowed_estimator: bool = True, figure_kw: Optional[Mapping] = None,
                 subplot_kw: Optional[Mapping] = None, gridspec_kw: Optional[Mapping] = None,
                 legend_kw: Optional[Mapping] = None):
        """A helper class that manages plotting spectrometer data."""
        self._data = data

        # settable properties exposed to Spectrometer
        self._plot_raw = plot_raw
        self._plot_timetrace = plot_timetrace
        self._plot_cumulative = plot_cumulative
        self._plot_negative_frequencies = plot_negative_frequencies
        self._plot_absolute_frequencies = plot_absolute_frequencies
        self._plot_amplitude = plot_amplitude
        self._plot_density = plot_density
        self._plot_cumulative_normalized = plot_cumulative_normalized
        self._plot_style = plot_style
        self._plot_update_mode = plot_update_mode
        self._plot_dB_scale = plot_dB_scale
        self._processed_unit = processed_unit

        # For dB scale plots, default to the first spectrum acquired.
        self._reference_spectrum: Optional[_keyT] = None

        self.prop_cycle = prop_cycle or plt.rcParams['axes.prop_cycle']
        self.raw_unit = raw_unit
        self.uses_windowed_estimator = uses_windowed_estimator

        self._leg = None
        self.axes = {key: dict.fromkeys(self.LINE_TYPES) for key in self.PLOT_TYPES}
        self.lines = dict()
        self.figure_kw = figure_kw or dict()
        self.subplot_kw = subplot_kw or dict()
        self.gridspec_kw = gridspec_kw or dict()
        self.legend_kw = legend_kw or dict()

        if not any('layout' in key for key in self.figure_kw.keys()):
            self.figure_kw['layout'] = 'tight'
        if self.subplot_kw.pop('sharex', None) is not None:
            warnings.warn('sharex in subplot_kw not negotiable, dropping', UserWarning)

        self.setup_figure()

    @cached_property
    def fig(self):
        """The figure hosting the plots."""
        try:
            return plt.figure(**self.figure_kw)
        except TypeError:
            if layout := self.figure_kw.pop('layout', False):
                # matplotlib < 3.5 doesn't support layout kwarg yet
                self.figure_kw[f'{layout}_layout'] = True
            elif layout is False:
                raise
            return plt.figure(**self.figure_kw)

    @property
    def ax(self):
        """The axes hosting processed lines."""
        return np.array([val['processed'] for val in self.axes.values()
                         if val['processed'] is not None])

    @property
    def ax_raw(self):
        """The axes hosting raw lines."""
        return np.array([val['raw'] for val in self.axes.values()
                         if val['raw'] is not None])

    @property
    def leg(self):
        """Axes legend."""
        return self._leg

    @property
    def shown(self) -> Tuple[Tuple[int, str], ...]:
        return tuple(key for key, val in self.lines.items()
                     if not val['main']['processed']['hidden'])

    @property
    def lines_to_draw(self) -> Tuple[str, ...]:
        return self.LINE_TYPES[:1 + self.plot_raw]

    @property
    def plots_to_draw(self) -> Tuple[str, ...]:
        return tuple(compress(self.PLOT_TYPES, [True, self.plot_cumulative, self.plot_timetrace]))

    @property
    def plot_context(self) -> ContextManager:
        if self.plot_style is not None:
            return plt.style.context(self.plot_style, after_reset=True)
        else:
            return contextlib.nullcontext()

    @property
    def plot_raw(self) -> bool:
        """If the raw data is plotted on a secondary y-axis."""
        return self._plot_raw

    @plot_raw.setter
    def plot_raw(self, val: bool):
        val = bool(val)
        if val != self._plot_raw:
            self._plot_raw = val
            self.update_line_attrs(self.plots_to_draw, ['raw'], stale=True, hidden=not val)
            self.setup_figure()

    @property
    def plot_cumulative(self) -> bool:
        """If the cumulative (integrated) PSD or spectrum is plotted on a subplot."""
        return self._plot_cumulative

    @plot_cumulative.setter
    def plot_cumulative(self, val: bool):
        val = bool(val)
        if val != self._plot_cumulative:
            self._plot_cumulative = val
            self.update_line_attrs(['cumulative'], self.lines_to_draw, stale=True, hidden=not val)
            self.setup_figure()

    @property
    def plot_timetrace(self) -> bool:
        """If the timetrace data is plotted on a subplot.

        The absolute value is plotted if the time series is complex."""
        return self._plot_timetrace

    @plot_timetrace.setter
    def plot_timetrace(self, val: bool):
        val = bool(val)
        if val != self._plot_timetrace:
            self._plot_timetrace = val
            self.update_line_attrs(['time'], self.lines_to_draw, stale=True, hidden=not val)
            self.setup_figure()

    @property
    def plot_negative_frequencies(self) -> bool:
        """Plot the negative frequencies for a two-sided spectrum."""
        return self._plot_negative_frequencies

    @plot_negative_frequencies.setter
    def plot_negative_frequencies(self, val: bool):
        val = bool(val)
        if val != self._plot_negative_frequencies:
            self._plot_negative_frequencies = val
            self.update_line_attrs(['main', 'cumulative'], self.lines_to_draw, stale=True)
            self.setup_figure()

    @property
    def plot_absolute_frequencies(self) -> bool:
        """For a lock-ins, plot physical frequencies at the input.

        This means the displayed frequencies are shifted by the
        demodulation frequency, which must be present in the settings
        under the keyword 'freq'."""
        return self._plot_absolute_frequencies

    @plot_absolute_frequencies.setter
    def plot_absolute_frequencies(self, val: bool):
        val = bool(val)
        if val != self._plot_absolute_frequencies:
            self._plot_absolute_frequencies = val
            self.update_line_attrs(
                plots=['main', 'cumulative'],
                keys=[key for key in self.shown if 'freq' in self._data[key]['settings']],
                stale=True
            )
            self.setup_figure()

    @property
    def plot_amplitude(self) -> bool:
        """If the amplitude spectral density is plotted instead of the
        power spectral density (ASD = sqrt(PSD)).

        Also applies to the cumulative spectrum, in which case that plot
        corresponds to the cumulative mean square instead of the root-
        mean-square (RMS)."""
        return self._plot_amplitude

    @plot_amplitude.setter
    def plot_amplitude(self, val: bool):
        val = bool(val)
        if val != self._plot_amplitude:
            self._plot_amplitude = val
            self.update_line_attrs(['main', 'cumulative'], self.lines_to_draw, stale=True)
            self.setup_figure()

    @property
    def plot_density(self) -> bool:
        """Plot the density or the spectrum."""
        return self._plot_density

    @plot_density.setter
    def plot_density(self, val: bool):
        val = bool(val)
        if val != self._plot_density:
            self._plot_density = val
            self.update_line_attrs(['main', 'cumulative'], self.lines_to_draw, stale=True)
            self.setup_figure()

    @property
    def plot_cumulative_normalized(self) -> bool:
        """If the cumulative spectrum is plotted normalized."""
        return self._plot_cumulative_normalized

    @plot_cumulative_normalized.setter
    def plot_cumulative_normalized(self, val: bool):
        val = bool(val)
        if val != self._plot_cumulative_normalized:
            self._plot_cumulative_normalized = val
            self.update_line_attrs(['cumulative'], self.lines_to_draw, stale=True)
            self.setup_figure()

    @property
    def plot_style(self) -> _styleT:
        """The matplotlib style used for plotting.

        See :attr:`matplotlib.style.available` for all available
        styles. Default is 'fast'.
        """
        return self._plot_style

    @plot_style.setter
    def plot_style(self, val: _styleT):
        if val != self._plot_style:
            self._plot_style = val
            self.destroy_axes()
            self.update_line_attrs(self.plots_to_draw, self.lines_to_draw, stale=True)
            self.setup_figure()

    @property
    def plot_update_mode(self) -> str:
        """Setting influencing how often the matplotlib event queue is
        flushed."""
        return self._plot_update_mode

    @plot_update_mode.setter
    @check_literals
    def plot_update_mode(self, mode: Literal['fast', 'always', 'never']):
        self._plot_update_mode = mode

    @property
    def plot_dB_scale(self) -> bool:
        """Plot data as dB relative to a reference spectrum.

        See also :attr:`reference_spectrum`."""
        return self._plot_dB_scale

    @plot_dB_scale.setter
    def plot_dB_scale(self, val: bool):
        val = bool(val)
        if val != self._plot_dB_scale:
            self._plot_dB_scale = val
            self.update_line_attrs(['main', 'cumulative'], self.lines_to_draw, stale=True)
            self.setup_figure()

    @property
    def reference_spectrum(self) -> Optional[Tuple[int, str]]:
        """Spectrum taken as a reference for the dB scale.

        See also :attr:`plot_dB_scale`."""
        if self._reference_spectrum is None and self._data:
            return list(self._data)[0]
        return self._reference_spectrum

    @property
    def processed_unit(self) -> str:
        """The unit displayed for processed data."""
        return self._processed_unit

    @processed_unit.setter
    def processed_unit(self, val: str):
        val = str(val)
        if val != self._processed_unit:
            self._processed_unit = val
            self.setup_figure()

    def main_plot(self, key, line_type):
        x, y = self.get_freq_data(key, line_type, self.plot_dB_scale)

        d = self.lines[key]['main'][line_type]
        if line := d['line']:
            line.set_data(x, y)
            line.set_color(self.line_props(key[0], d)['color'])
            line.set_alpha(self.line_props(key[0], d)['alpha'])
            line.set_zorder(self.line_props(key[0], d)['zorder'])
        else:
            line, = self.axes['main'][line_type].plot(x, y, **self.line_props(key[0], d))
        self.update_line_attrs(['main'], [line_type], [key], stale=False, line=line)

    def cumulative_plot(self, key, line_type):
        # y is the power irrespective of whether self.plot_amplitude is True or not.
        # This means that if the latter is True, this plot shows the cumulative RMS,
        # and if it's False the cumulative MS (mean square, variance).
        x, y = self.get_freq_data(key, line_type, self.plot_dB_scale, cumulative=True)

        x_min, x_max = self.axes['cumulative'][line_type].get_xlim()
        mask = (x_min <= x) & (x <= x_max)
        x = x[..., mask]
        y = y[..., mask]
        y = integrate.cumulative_trapezoid(y, x, initial=0, axis=-1)
        if self.plot_amplitude:
            y = np.sqrt(y)
        if self.plot_cumulative_normalized:
            y = (y - y.min()) / y.ptp()

        d = self.lines[key]['cumulative'][line_type]
        if line := d['line']:
            line.set_data(x, y)
            line.set_color(self.line_props(key[0], d)['color'])
            line.set_alpha(self.line_props(key[0], d)['alpha'])
            line.set_zorder(self.line_props(key[0], d)['zorder'])
        else:
            line, = self.axes['cumulative'][line_type].plot(x, y, **self.line_props(key[0], d))
        self.update_line_attrs(['cumulative'], [line_type], [key], stale=False, line=line)

    def time_plot(self, key, line_type):
        y = self._data[key][f'timetrace_{line_type}'][-1]
        if np.iscomplexobj(y):
            y = np.abs(y)
        x = np.arange(y.size) / self._data[key]['settings']['fs']

        d = self.lines[key]['time'][line_type]
        if line := d['line']:
            line.set_data(x, y)
            line.set_color(self.line_props(key[0], d)['color'])
            line.set_alpha(self.line_props(key[0], d)['alpha'])
            line.set_zorder(self.line_props(key[0], d)['zorder'])
        else:
            line, = self.axes['time'][line_type].plot(x, y, **self.line_props(key[0], d))
        self.update_line_attrs(['time'], [line_type], [key], stale=False, line=line)

    def setup_figure(self):
        gs = gridspec.GridSpec(2 + self.plot_cumulative + self.plot_timetrace, 1, figure=self.fig,
                               **self.gridspec_kw)
        with self.plot_context:
            self.setup_main_axes(gs)
            self.setup_cumulative_axes(gs)
            self.setup_time_axes(gs)
            self.destroy_unused_axes()
            self.update_figure()

    def setup_main_axes(self, gs: gridspec.GridSpec):
        if self.axes['main']['processed'] is None:
            self.axes['main']['processed'] = self.fig.add_subplot(gs[:2], **self.subplot_kw)
            self.axes['main']['processed'].grid(True)
            self.axes['main']['processed'].set_xlabel('$f$ (Hz)')
        self.axes['main']['processed'].set_xscale('log')
        self.axes['main']['processed'].set_yscale('linear' if self.plot_dB_scale else 'log')
        # can change
        self.axes['main']['processed'].set_ylabel(
            _ax_label(self.plot_amplitude, False, self.plot_dB_scale, self.reference_spectrum)
            + _ax_unit(self.plot_amplitude, self.plot_density, False,
                       self.plot_cumulative_normalized, self.plot_dB_scale,
                       'dB' if self.plot_dB_scale else self.processed_unit)
        )
        if self.plot_raw:
            if self.axes['main']['raw'] is None:
                self.axes['main']['raw'] = self.axes['main']['processed'].twinx()
            self.axes['main']['raw'].set_yscale('linear' if self.plot_dB_scale else 'log')
            # can change
            self.axes['main']['raw'].set_ylabel(
                _ax_label(self.plot_amplitude, False, self.plot_dB_scale, self.reference_spectrum)
                + _ax_unit(self.plot_amplitude, self.plot_density, False,
                           self.plot_cumulative_normalized, self.plot_dB_scale,
                           'dB' if self.plot_dB_scale else self.raw_unit)
            )
        self.set_subplotspec('main', gs[:2])

    def setup_cumulative_axes(self, gs: gridspec.GridSpec):
        if self.plot_cumulative:
            if self.axes['cumulative']['processed'] is None:
                self.axes['cumulative']['processed'] = self.fig.add_subplot(
                    gs[2], sharex=self.axes['main']['processed'], **self.subplot_kw
                )
                self.axes['cumulative']['processed'].grid(True)
                self.axes['cumulative']['processed'].set_xlabel('$f$ (Hz)')
            self.axes['cumulative']['processed'].set_xscale('log')
            # can change
            self.axes['cumulative']['processed'].set_ylabel(
                _ax_label(self.plot_amplitude, True, self.plot_dB_scale, self.reference_spectrum)
                + _ax_unit(self.plot_amplitude, self.plot_density, True,
                           self.plot_cumulative_normalized, self.plot_dB_scale,
                           'dB' if self.plot_dB_scale else self.processed_unit)
            )
            if self.plot_raw:
                if self.axes['cumulative']['raw'] is None:
                    self.axes['cumulative']['raw'] = self.axes['cumulative']['processed'].twinx()
                # can change
                self.axes['cumulative']['raw'].set_ylabel(
                    _ax_label(self.plot_amplitude, True, self.plot_dB_scale,
                              self.reference_spectrum)
                    + _ax_unit(self.plot_amplitude, self.plot_density, True,
                               self.plot_cumulative_normalized, self.plot_dB_scale,
                               'dB' if self.plot_dB_scale else self.raw_unit)
                )
            self.set_subplotspec('cumulative', gs[2])

    def setup_time_axes(self, gs: gridspec.GridSpec):
        if self.plot_timetrace:
            if self.axes['time']['processed'] is None:
                self.axes['time']['processed'] = self.fig.add_subplot(gs[-1], **self.subplot_kw)
                self.axes['time']['processed'].grid(True)
                self.axes['time']['processed'].set_xlabel('$t$ (s)')
            # can change
            self.axes['time']['processed'].set_ylabel(f'Amplitude ({self.processed_unit})')
            if self.plot_raw:
                if self.axes['time']['raw'] is None:
                    self.axes['time']['raw'] = self.axes['time']['processed'].twinx()
                # can change
                self.axes['time']['raw'].set_ylabel(f'Amplitude ({self.raw_unit})')
            self.set_subplotspec('time', gs[-1])

    def destroy_axes(self,
                     plots: Iterable[str] = PLOT_TYPES,
                     lines: Iterable[str] = LINE_TYPES):
        self.destroy_lines(plots, lines)
        for plot in plots:
            for line in lines:
                try:
                    self.axes[plot][line].remove()
                    self.axes[plot][line] = None
                except AttributeError:
                    # Ax None
                    continue

    def destroy_unused_axes(self):
        if not self.plot_raw:
            self.destroy_axes(lines=['raw'])
        self.destroy_axes(set(self.PLOT_TYPES).difference(self.plots_to_draw))

    def destroy_lines(self,
                      plots: Iterable[str] = PLOT_TYPES,
                      lines: Iterable[str] = LINE_TYPES,
                      keys: Optional[Iterable[_keyT]] = None):
        for key in keys or self.shown:
            for plot in plots:
                for line in lines:
                    try:
                        self.lines[key][plot][line]['line'].remove()
                        self.lines[key][plot][line]['line'] = None
                        self.lines[key][plot][line]['stale'] = None
                        self.lines[key][plot][line]['hidden'] = None
                    except AttributeError:
                        # Line None
                        continue

    def update_figure(self):
        if not plt.fignum_exists(self.fig.number):
            # Need to completely restore figure
            self.__dict__.pop('fig', None)
            self.destroy_axes()
            self.update_line_attrs(self.plots_to_draw, self.lines_to_draw, self.shown, stale=True)
            self.setup_figure()

        # Flush out all idle events
        self.fig.canvas.draw_idle()
        if self.plot_update_mode in {'always'}:
            self.fig.canvas.flush_events()

        # First set new axis scales and x-limits, then update the lines (since the cumulative
        # spectrum plot changes dynamically with the limits). Once all lines are drawn, update
        # y-limits
        self.set_xscales()
        self.set_xlims()
        self.update_lines()
        self.set_ylims()

        try:
            labels, handles = zip(*sorted(zip(self.shown,
                                              [val['main']['processed']['line']
                                               for val in self.lines.values()
                                               if val['main']['processed']['line'] is not None])))
            self._leg = self.ax[0].legend(handles=handles, labels=labels, **self.legend_kw)
        except ValueError:
            # Nothing to show or no data, do not draw the legend / remove it
            if self._leg is not None:
                self._leg.remove()

        # Needed to force update during a loop for instance
        self.fig.canvas.draw_idle()
        if self.plot_update_mode in {'always', 'fast'}:
            self.fig.canvas.flush_events()
        self.fig.show()

    def update_lines(self):
        for key in self.shown:
            for plot in self.plots_to_draw:
                for line in self.lines_to_draw:
                    if self.lines[key][plot][line]['stale']:
                        getattr(self, f'{plot}_plot')(key, line)

    def add_new_line_entry(self, key: Tuple[int, str]):
        self.lines[key] = dict.fromkeys(self.PLOT_TYPES)
        for plot in self.PLOT_TYPES:
            self.lines[key][plot] = dict.fromkeys(self.LINE_TYPES)
            for line in self.LINE_TYPES:
                self.lines[key][plot][line] = dict.fromkeys(['line', 'color', 'stale', 'hidden'])
            self.lines[key][plot]['processed']['zorder'] = 5
            self.lines[key][plot]['processed']['alpha'] = 1
            self.lines[key][plot]['raw']['zorder'] = 4
            self.lines[key][plot]['raw']['alpha'] = 0.5

    def set_subplotspec(self, plot: str, gs: gridspec.GridSpec):
        for line in self.lines_to_draw:
            self.axes[plot][line].set_subplotspec(gs)

    def set_xlims(self):
        # Frequency-axis plots
        right = max((
            self._data[k]['settings']['f_max']
            + (self._data[k]['settings'].get('freq', 0)
               if self.plot_absolute_frequencies else 0)
            for k in self.shown
        ), default=None)
        if (
                not self.plot_negative_frequencies
                or self.axes['main']['processed'].get_xscale() == 'log'
        ):
            left = min((
                self._data[k]['settings']['f_min']
                + (self._data[k]['settings'].get('freq', 0)
                   if self.plot_absolute_frequencies else 0)
                for k in self.shown
            ), default=None)
        else:
            left = min((
                - self._data[k]['settings']['f_max']
                + (self._data[k]['settings'].get('freq', 0)
                   if self.plot_absolute_frequencies else 0)
                for k in self.shown
            ), default=None)

        with filter_warnings('ignore', UserWarning):
            # ignore warnings issued for empty plots with log scales
            self.axes['main']['processed'].set_xlim(left, right)

        # Time-axis plot
        # Need to call relim before autoscale in case we used set_data()
        # before, see :meth:`matplotlib.axes.Axes.autoscale_view`
        if self.plot_timetrace:
            self.axes['time']['processed'].relim(visible_only=True)
            self.axes['time']['processed'].autoscale(enable=True, axis='x', tight=True)

    def set_ylims(self):
        if not self.shown:
            return

        margin = plt.rcParams['axes.ymargin']
        for plot in self.plots_to_draw:
            for line in self.lines_to_draw:
                top = -np.inf
                bottom = np.inf
                for key in self.shown:
                    left, right = self.axes[plot][line].get_xlim()
                    xdata = self.lines[key][plot][line]['line'].get_xdata()
                    ydata = self.lines[key][plot][line]['line'].get_ydata()[
                        (left <= xdata) & (xdata <= right)
                    ]
                    top = max(top, ydata.max())
                    bottom = min(bottom, ydata.min())
                # Transform to correct scale
                transform = self.axes[plot][line].transScale
                top, bottom = transform.transform([(1, top),
                                                   (1, bottom)])[:, 1]
                interval = top - bottom
                top += margin * interval
                bottom -= margin * interval
                # Transform back
                top, bottom = transform.inverted().transform([(1, top),
                                                              (1, bottom)])[:, 1]
                self.axes[plot][line].set_ylim(bottom, top)

    def set_xscales(self):
        if (
                self.plot_negative_frequencies
                and any(d['f_processed'][0] < 0 for d in self._data.values())
                or self.plot_raw and any(d['f_raw'][0] < 0 for d in self._data.values())
                and self.axes['main']['processed'].get_xscale() == 'log'
        ):
            if self.axes['main']['processed'].get_xscale() == 'log':
                # matplotlib>=3.6 has asinh scale for log plots with negative values
                try:
                    self.axes['main']['processed'].set_xscale('asinh')
                    if self.plot_cumulative:
                        self.axes['cumulative']['processed'].set_xscale('asinh')
                except ValueError:
                    self.axes['main']['processed'].set_xscale('linear')
                    if self.plot_cumulative:
                        self.axes['cumulative']['processed'].set_xscale('linear')
        else:
            if self.axes['main']['processed'].get_xscale() != 'log':
                self.axes['main']['processed'].set_xscale('log')
                if self.plot_cumulative:
                    self.axes['cumulative']['processed'].set_xscale('log')

    def update_line_attrs(self,
                          plots: Iterable[str] = PLOT_TYPES,
                          lines: Iterable[str] = LINE_TYPES,
                          keys: Optional[Iterable[_keyT]] = None,
                          **kwargs):
        for key in keys or self.shown:
            for plot in plots:
                for line in lines:
                    self.lines[key][plot][line].update(kwargs)

    def line_props(self, index: int, line_dct: dict) -> dict:
        props = {key: val[index % len(self.prop_cycle)]
                 for key, val in self.prop_cycle.by_key().items()}
        # Default values for raw/processed lines
        props.setdefault('zorder', line_dct['zorder'])
        props.setdefault('alpha', line_dct['alpha'])
        # Color can be overridden in show()
        if line_dct['color'] is not None:
            props['color'] = line_dct['color']
        return props

    def drop_lines(self, key: _keyT):
        del self.lines[key]

    def get_freq_data(self, key, line_type, dB, reference=False,
                      cumulative=False) -> Tuple[np.ndarray, np.ndarray]:
        x = self._data[key][f'f_{line_type}'].copy()
        if self.plot_absolute_frequencies:
            x += self._data[key]['settings'].get('freq', 0)

        window = self._data[key]['settings'].get(
            'window', 'hann' if self.uses_windowed_estimator else 'boxcar'
        )
        nperseg = self._data[key]['settings']['nperseg']
        fs = self._data[key]['settings']['fs']

        y = np.mean(self._data[key][f'S_{line_type}'], axis=0)
        if not self.plot_density or dB:
            # Need to calculate dB using the spectrum, not the density
            if isinstance(window, str) or isinstance(window, tuple):
                window = signal.get_window(window, nperseg)
            else:
                window = np.asarray(window)
            y *= fs * (window ** 2).sum() / window.sum() ** 2
        if self.plot_amplitude and not cumulative:
            y **= 0.5

        if dB and not reference:
            _, y0 = self.get_freq_data(self.reference_spectrum, line_type, dB=True, reference=True)
            with np.errstate(divide='ignore', invalid='ignore'):
                try:
                    y = 10 * np.log10(y / y0)
                except ValueError as error:
                    raise RuntimeError(f'dB scale requested but data for key {key} does not have '
                                       'the same shape as reference data with key '
                                       f'{self.reference_spectrum}. Select a different reference '
                                       'using Spectrometer.set_reference_spectrum() or adapt your '
                                       'acquisition parameters') from error
            if self.plot_density:
                y /= fs * (window ** 2).sum() / window.sum() ** 2

        return x, y


class Spectrometer:
    r"""A spectrometer to acquire and display power spectral densities.

    Spectra are acquired using :meth:`take` and identified by an
    index-comment two-tuple. The data is measured and processed by
    either a user-supplied function or
    :func:`~qutil:qutil.signal_processing.real_space.welch`.

    Parameters
    ----------
    daq : DAQ
        A :class:`.daq.core.DAQ` object handling data acquisition. This
        class abstracts away specifics of how to interact with the
        hardware to implement an interface that is independent of the
        lower-level driver. See the :class:`.DAQ` docstring for more
        information.

        If not given, the instance is read-only and can only be used
        for processing and plotting old data.
    psd_estimator : Callable or kwarg dict
        If callable, a function with signature::

            f(data, **settings) -> (ndarray, ndarray, ndarray)

        that takes the data acquired by the DAQ and the settings
        dictionary and estimates the PSD, returning a tuple of
        (PSD, frequencies, iFFTd data). If dict, a keyword-argument
        dictionary to be passed to
        :func:`~qutil:qutil.signal_processing.real_space.welch` as a PSD
        estimator.

        .. note::

            If a dict, the keyword 'density' will be excluded when
            called since it is always assumed that the ``psd_estimator``
            will return a power spectral density.

    procfn : Callable or sequence of Callable
        A (sequence of) callable with signature::

            f(timetrace, **settings) -> ndarray

        that performs processing steps on the raw timeseries data.
        The function is called with the settings as returned by
        :meth:`.DAQ.setup`. If a sequence, the functions are applied
        from left-to-right, e.g., if ``procfn = [a, b, c]``, then
        it is applied as ``c(b(a(xf, f, **s), f, **s), f, **s)``.
    plot_raw : bool, default False
        Plot the raw spectral data on a secondary y-axis using a
        smaller alpha (more transparent line). Can also be toggled
        dynamically by setting :attr:`plot_raw`.
    plot_timetrace : bool, default False
        Plot the most recent raw timeseries data on a new subplot.
        Can also be toggled dynamically by setting
        :attr:`plot_timetrace`.
    plot_cumulative : bool, default False
        Plot the cumulative data given by

        .. math::
            \int_{f_\mathrm{min}}^f\mathrm{d}f^\prime S(f^\prime)

        on a new subplot. :math:`S(f)` is whatever is plotted in the
        main plot and therefore depends on :attr:`plot_density` and
        :attr:`plot_amplitude`. Can also be toggled dynamically by
        setting :attr:`plot_cumulative`.
    plot_negative_frequencies : bool, default True
        Plot negative frequencies for two-sided spectra (in case the
        time-series data is complex). For ``matplotlib >= 3.6`` an
        ``asinh``, otherwise a linear scale is used. Can also be
        toggled dynamically by setting
        :attr:`plot_negative_frequencies`.
    plot_absolute_frequencies : bool, default True
        For lock-in measurements: plot the physical frequencies at the
        input of the device, not the downconverted ones. This means the
        displayed frequencies are shifted by the demodulation
        frequency, which must be present in the settings under the
        keyword 'freq'. Can also be toggled dynamically by setting
        :attr:`plot_absolute_frequencies`.
    plot_amplitude : bool, default True
        Plot the amplitude spectral density / spectrum (the square root)
        instead of the power. Also applies to the cumulative plot
        (:attr:`plot_cumulative`), in which case that plot
        corresponds to the cumulative mean square instead of the
        root-mean-square (RMS) if plotting the density. Can also be
        toggled dynamically by setting :attr:`plot_amplitude`.

        .. note::
            :attr:`psd_estimator` should always return a power spectral
            density, the conversions concerning this parameter are done
            only when plotting.

    plot_density : bool, default True
        Plot the * spectral density rather than the * spectrum. If
        False and plot_amplitude is True, i.e. if the amplitude spectrum
        is plotted, the height of a peak will give an estimate of the
        RMS amplitude. Can also be toggled dynamically by setting
        :attr:`plot_density`.

        .. note::
            :attr:`psd_estimator` should always return a power spectral
            density, the conversions concerning this parameter are done
            only when plotting.

    plot_cumulative_normalized : bool, default False
        Normalize the cumulative data so that it corresponds to the CDF.
        Can also be toggled dynamically by setting
        :attr:`plot_cumulative_normalized`.
    plot_style : str, Path, dict, list thereof, or None, default 'fast'
        Use a matplotlib style sheet for plotting. All styles available
        are given by :attr:`matplotlib.style.available`. Set to None to
        disable styling and use default parameters. Note that line
        styles in ``prop_cycle`` override style settings.
    plot_update_mode : {'fast', 'always', 'never'}, default 'fast'
        Determines how often the event queue of the plot is flushed.

         - 'fast' : queue is only flushed after all plot calls are
           done. Lines might not show upon every average update. By
           experience, whether lines are updated inside a loop depends
           on the DAQ backend. (default)
         - 'always' : forces a flush before and after plot calls are
           done, but slows down the entire plotting by a factor of
           order unity.
         - 'never' : Queue is never flushed explicitly.
    plot_dB_scale : bool, default False
        Plot data in dB relative to a reference spectrum instead of
        in absolute units. The reference spectrum defaults to the first
        acquired, but can be set using :meth:`set_reference_spectrum`.
    prop_cycle : cycler.Cycler
        A property cycler for styling the plotted lines.
    savepath : str or Path
        Directory where the data is saved. All relative paths, for
        example those given to :meth:`serialize_to_disk`, will be
        referenced to this.
    compress : bool
        Compress the data when saving to disk (using
        :func:`numpy:numpy.savez_compressed`).
    raw_unit : str
        The unit of the raw, unprocessed data returned by
        meth:`DAQ.acquire`.
    processed_unit : str
        The unit of the processed data. Can also be set dynamically by
        setting :attr:`processed_unit` in case it changed when using
        :meth:`reprocess_data`.
    figure_kw, gridspec_kw, subplot_kw, legend_kw : Mappings
        Keyword arguments forwarded to the corresopnding matplotlib
        constructors.

    Examples
    --------
    Perform spectral estimation on simulated data using `qopt` as
    backend:

    >>> from pathlib import Path
    >>> from tempfile import mkdtemp
    >>> from python_spectrometer.daq import QoptColoredNoise
    >>> def spectrum(f, A=1e-4, exp=1.5, **_):
    ...     return A/f**exp
    >>> daq = QoptColoredNoise(spectrum)
    >>> spect = Spectrometer(daq, savepath=mkdtemp())
    >>> spect.take('a comment', f_max=2000, A=2e-4)
    >>> spect.print_keys()
    (0, 'a comment')
    >>> spect.take('more comments', df=0.1, f_max=2000)
    >>> spect.print_keys()
    (0, 'a comment')
    (1, 'more comments')

    Hide and show functionality:

    >>> spect.hide(0)
    >>> spect.show('a comment')  # same as spect.show(0)
    >>> spect.drop(1)  # drops the spectrum from cache but leaves the data

    Save/recall functionality:

    >>> spect.serialize_to_disk('foo')
    >>> spect_loaded = Spectrometer.recall_from_disk(
    ...     spect.savepath / 'foo', daq
    ... )
    >>> spect_loaded.print_keys()
    (0, 'a comment')
    >>> spect.print_settings('a comment')
    Settings for key (0, 'a comment'):
    {'A': 0.0002,
     'df': 1.0,
     'f_max': 2000.0,
     'f_min': 1.0,
     'fs': 4000.0,
     'n_avg': 1,
     'n_pts': 12000,
     'n_seg': 5,
     'noverlap': 2000,
     'nperseg': 4000}

    """
    _OLD_PARAMETER_NAMES = {
        'plot_cumulative_power': 'plot_cumulative',
        'plot_cumulative_spectrum': 'plot_cumulative',
        'cumulative_normalized': 'plot_cumulative_normalized',
        'amplitude_spectral_density': 'plot_amplitude'
    }

    @check_literals
    def __init__(self, daq: Optional[DAQ] = None, *,
                 psd_estimator: Optional[Union[Callable, Dict[str, Any]]] = None,
                 procfn: Optional[Union[Callable, Sequence[Callable]]] = None,
                 plot_raw: bool = False, plot_timetrace: bool = False,
                 plot_cumulative: bool = False, plot_negative_frequencies: bool = True,
                 plot_absolute_frequencies: bool = True, plot_amplitude: bool = True,
                 plot_density: bool = True, plot_cumulative_normalized: bool = True,
                 plot_style: _styleT = 'fast',
                 plot_update_mode: Literal['fast', 'always', 'never'] = 'fast',
                 plot_dB_scale: bool = False, prop_cycle=None,
                 purge_raw_data: bool = False, savepath: _pathT = None,
                 compress: bool = True, raw_unit: str = 'V', processed_unit: str = 'V',
                 figure_kw: Optional[Mapping] = None, subplot_kw: Optional[Mapping] = None,
                 gridspec_kw: Optional[Mapping] = None, legend_kw: Optional[Mapping] = None):

        self._data: Dict[Tuple[int, str], Dict] = {}
        self._savepath: Optional[Path] = None

        self.daq = daq
        self.procfn = chain(*procfn) if np.iterable(procfn) else chain(procfn or Id)
        self.savepath = savepath or '~/python_spectrometer/' + datetime.now().strftime('%Y-%m-%d')
        self.compress = compress
        if purge_raw_data:
            warnings.warn('Enabling purge raw data might break some plotting features!',
                          UserWarning, stacklevel=2)
        self.purge_raw_data = purge_raw_data

        if psd_estimator is None:
            psd_estimator = {}
        if callable(psd_estimator):
            self.psd_estimator = psd_estimator
        elif isinstance(psd_estimator, Mapping):
            self.psd_estimator = partial(welch, **psd_estimator)
        else:
            raise TypeError('psd_estimator should be callable or kwarg dict for welch().')
        uses_windowed_estimator = 'window' in inspect.signature(self.psd_estimator).parameters

        self._plot_manager = _PlotManager(self._data, plot_raw, plot_timetrace,
                                          plot_cumulative, plot_negative_frequencies,
                                          plot_absolute_frequencies, plot_amplitude,
                                          plot_density, plot_cumulative_normalized,
                                          plot_style, plot_update_mode, plot_dB_scale,
                                          prop_cycle, raw_unit, processed_unit,
                                          uses_windowed_estimator, figure_kw, subplot_kw,
                                          gridspec_kw, legend_kw)

    # Expose plot properties from plot manager
    _to_expose = ('fig', 'ax', 'ax_raw', 'leg', 'plot_raw', 'plot_timetrace', 'plot_cumulative',
                  'plot_negative_frequencies', 'plot_absolute_frequencies', 'plot_amplitude',
                  'plot_density', 'plot_cumulative_normalized', 'plot_style', 'plot_update_mode',
                  'plot_dB_scale', 'reference_spectrum', 'processed_unit')
    locals().update({attr: _forward_property(_PlotManager, '_plot_manager', attr)
                     for attr in _to_expose})

    def __repr__(self) -> str:
        if self.keys():
            return super().__repr__() + ' with keys\n' + self._repr_keys()
        else:
            return super().__repr__()

    def __del__(self):
        plt.close(self.fig)

    def __getitem__(self, key: _keyT) -> Dict[str, Any]:
        return self._data[self._parse_keys(key)[0]]

    def __iter__(self) -> Iterator[Dict[str, Any]]:
        """Iterator (yields values instead of keys like a dict)."""
        yield from self.values()

    def __len__(self) -> int:
        return self._data.__len__()

    @property
    def _index(self) -> int:
        """Next available index."""
        known_ix = sorted((ix for ix, *_ in self._data))
        free_ix = (np.diff(known_ix) != 1).nonzero()[0]
        if 0 not in known_ix:
            return 0
        elif free_ix.size:
            return free_ix[0] + 1
        else:
            return len(self._data)

    @cached_property
    def _runfile(self) -> Path:
        return self._get_new_file('files', suffix='txt')

    @cached_property
    def _objfile(self) -> Path:
        return self._get_new_file('object', suffix='')

    @property
    def files(self) -> Generator[str, None, None]:
        """List of all data files."""
        return (str(data['filepath']) for data in self.values())

    @property
    def savepath(self) -> Path:
        """The base path where files are stored on disk."""
        return self._savepath

    @savepath.setter
    def savepath(self, path):
        self._savepath = io.to_global_path(path)

    def _resolve_relative_path(self, file: _pathT) -> Path:
        if not (file := Path(file)).is_absolute():
            file = self.savepath / file
        return io.to_global_path(file)

    def _get_new_file(self, append: str = 'data', comment: str = '', suffix: str = 'npz') -> Path:
        """Obtain a new file."""
        self.savepath.mkdir(parents=True, exist_ok=True)
        comment = _make_filesystem_compatible(comment)
        return (self.savepath
                / "spectrometer{}_{}{}{}".format('_' + append if append else '',
                                                 datetime.now().strftime('%Y-%m-%d_%H-%M-%S'),
                                                 '_' + comment if comment else '',
                                                 '.' + suffix if suffix else ''))

    def _unravel_coi(self, *comment_or_index: _keyT) -> Tuple[_keyT, ...]:
        if len(comment_or_index) == 1:
            if comment_or_index[0] == 'all':
                comment_or_index = tuple(self.keys())
            elif isinstance(comment_or_index[0], slice):
                idx = [ix for ix, _ in self.keys()]
                comment_or_index = tuple(
                    ix for ix in list(range(max(idx) + 1))[comment_or_index[0]]
                    if ix in idx
                )
        return comment_or_index

    def _parse_keys(self, *comment_or_index: _keyT) -> List[Tuple[int, str]]:
        """Get spectrum data for key."""
        parsed = []
        for coi in comment_or_index:
            if coi in self.keys():
                # key a tuple of (int, str)
                parsed.append(coi)
            else:
                # Check if key is either int or str, otherwise raise
                indices, comments = zip(*tuple(self._data))
                try:
                    if isinstance(coi, str):
                        ix = [i for i, elem in enumerate(comments) if elem == coi]
                        if len(ix) == 0:
                            raise ValueError
                        elif len(ix) == 1:
                            ix = ix[0]
                        else:
                            raise KeyError(f"Comment '{coi}' occurs multiple times. Please "
                                           + "specify the index.") from None
                    elif isinstance(coi, int):
                        # Allow for negative indices. Can raise ValueError
                        ix = indices.index(coi if coi >= 0 else len(indices) + coi)
                    else:
                        raise ValueError
                except ValueError:
                    raise KeyError(f'Key {coi} not registered') from None
                parsed.append((indices[ix], comments[ix]))
        return parsed

    def _repr_keys(self, *keys) -> str:
        if not keys:
            keys = self.keys()
        return '\n'.join((str(key) for key in sorted(self.keys()) if key in keys))

    @mock.patch.multiple('numpy.compat.py3k.pickle',
                         Unpickler=dill.Unpickler, Pickler=dill.Pickler)
    def _savefn(self, file: _pathT, **kwargs):
        file = io.check_path_length(file)
        if self.compress:
            np.savez_compressed(str(file), **_to_native_types(kwargs))
        else:
            np.savez(str(file), **_to_native_types(kwargs))

    @classmethod
    def _make_kwargs_compatible(cls, kwargs: Dict[str, Any]) -> Dict[str, Any]:
        compatible_kwargs = dict()
        signature = inspect.signature(cls)

        # Replace old param names by new ones ...
        for old, new in cls._OLD_PARAMETER_NAMES.items():
            if old in kwargs:
                if new not in kwargs:
                    kwargs[new] = kwargs.pop(old)
                else:
                    # Don't overwrite in case of clash
                    kwargs.pop(old)

        # And drop all other unknown ones.
        for param, val in kwargs.items():
            if param not in signature.parameters:
                warnings.warn(f'Parameter {param} not supported anymore, dropping', RuntimeWarning)
            else:
                compatible_kwargs[param] = val

        return compatible_kwargs

    def _process_data(self, timetrace_raw, **settings) -> Dict[str, Any]:
        S_raw, f_raw, _ = welch(timetrace_raw, **settings)
        S_processed, f_processed, timetrace_processed = self.psd_estimator(
            self.procfn(np.array(timetrace_raw), **settings),
            **settings
        )
        # if read-only, self.daq is None
        DAQSettings = getattr(self.daq or daq_settings, 'DAQSettings')
        data = dict(timetrace_raw=timetrace_raw,
                    timetrace_processed=timetrace_processed,
                    f_raw=f_raw,
                    f_processed=f_processed,
                    S_raw=S_raw,
                    S_processed=S_processed,
                    settings=DAQSettings(settings))
        return data

    def take(self, comment: str = '', progress: bool = True, **settings):
        """Acquire a spectrum with given settings and comment.

        There are default parameter names that manage data acqusition
        settings by way of a dictionary subclass,
        :class:`.daq.settings.DAQSettings`. These are checked for
        consistency at runtime, since it is for example not possible to
        specify :attr:`~.daq.settings.DAQSettings.f_min` to be smaller
        than the frequency resolution
        :attr:`~.daq.settings.DAQSettings.df`. See the
        :class:`~.daq.settings.DAQSettings` docstring for examples; the
        special settings are reproduced below.

        Parameters
        ----------
        comment : str
            An explanatory comment that helps identify the spectrum.
        progress : bool
            Show a progressbar for the outer repetitions of data acqusition.
            Default True.
        **settings
            Keyword argument settings for the data acquisition and
            possibly data processing using :attr:`procfn` or
            :attr:`fourier_procfn`.
        """
        if not isinstance(self.daq, DAQ):
            raise ReadonlyError('Cannot take new data since no DAQ backend given')

        if (key := (self._index, comment)) in self._data:
            raise KeyError(f'Key {key} already exists. Choose a different comment.')

        # Drop density from settings so that self.psd_estimator will always return a PSD
        if 'density' in settings:
            settings.pop('density')

        settings = self.daq.DAQSettings(self.daq.setup(**settings))
        filepath = self._get_new_file(comment=comment)
        self._data[key] = {'settings': settings, 'comment': comment, 'filepath': filepath}
        self._plot_manager.add_new_line_entry(key)

        iterator = self.daq.acquire(**settings)
        for i in progressbar(count(), disable=not progress, total=settings.n_avg,
                             desc=f'Acquiring {settings.n_avg} spectra with key {key}'):
            # Promote warnings to errors during data acquisition since usually
            # something will go wrong at some point anyway.
            try:
                fetched_data = next(iterator)
                processed_data = self._process_data(fetched_data, **settings)
            except StopIteration as stop:
                measurement_metadata = stop.value
                break
            except Exception as error:
                # Make sure we are left in a reproducible state
                self.drop(key)
                msg = 'Something went wrong during data acquisition'
                if 'fetched_data' in locals():
                    msg = msg + (f'. {self.daq.acquire} last returned the following data:\n '
                                 f'{fetched_data}')
                raise RuntimeError(msg) from error

            # TODO: This could fail if the iterator was empty and processed_data was never assigned
            self._data[key].update(_merge_data_dicts(self._data[key], processed_data))
            self.set_reference_spectrum(self.reference_spectrum)
            self.show(key)

        self._data[key].update(measurement_metadata=measurement_metadata)
        if self.purge_raw_data:
            del self._data[key]['timetrace_raw']
            del self._data[key]['timetrace_processed']
            del self._data[key]['f_raw']
            del self._data[key]['S_raw']
            self._data[key]['S_processed'] = np.mean(self._data[key]['S_processed'], axis=0)[None]

        self._savefn(filepath, **self._data[key])

    take.__doc__ = (take.__doc__.replace(8*' ', '')
                    + '\n\nDAQ Parameters'
                    + '\n==============\n'
                    + '\n'.join((f'{key} : {val}' for key, val in daq_settings._doc_.items())))

    def drop(self, *comment_or_index: _keyT, update_figure: bool = True):
        """Delete a spectrum from cache and plot.

        Parameters
        ----------
        *comment_or_index : int | str | (int, str)
            Key(s) for spectra. May be either the integer index, the
            string comment, or a tuple of both. See :meth:`print_keys`
            for all registered keys.
        update_figure : bool, default True
            Update the figure. Only used internally.

        See Also
        --------
        :meth:`hide`
        :meth:`show`

        Examples
        --------
        The following are equivalent for a :class:`Spectrometer` with
        keys ``[(0, 'a'), (1, 'b')]``::

            spect.drop(0)
            spect.drop('a')
            spect.drop(-2)
            spect.drop((0, 'a'))

        Multiple spectra can be dropped at the same time::

            spect.drop(0, (1, 'b'))

        """
        try:
            for key in self._parse_keys(*self._unravel_coi(*comment_or_index)):
                self._plot_manager.destroy_lines(keys=[key])
                self._plot_manager.drop_lines(key)
                del self._data[key]
                if key == self.reference_spectrum:
                    if self:
                        self._plot_manager._reference_spectrum = list(self.keys())[0]
                    else:
                        self._plot_manager._reference_spectrum = None
        finally:
            if update_figure:
                with self._plot_manager.plot_context:
                    self._plot_manager.update_figure()

    def delete(self, *comment_or_index: _keyT):
        """Delete the data of a spectrum saved on disk and drop it
        from cache.

        .. warning::
            This deletes data from disk!

        Parameters
        ----------
        *comment_or_index : int | str | (int, str)
            Key(s) for spectra. May be either the integer index, the
            string comment, or a tuple of both. See :meth:`print_keys`
            for all registered keys.

        """
        try:
            for key in self._parse_keys(*self._unravel_coi(*comment_or_index)):
                file = self[key]['filepath']
                if io.query_yes_no(f'Really delete file {file}?', default='no'):
                    self.drop(key, update_figure=False)
                    os.remove(file)
        finally:
            with self._plot_manager.plot_context:
                self._plot_manager.update_figure()

    def hide(self, *comment_or_index: _keyT):
        """Hide a spectrum in the plot.

        Parameters
        ----------
        *comment_or_index : int | str | (int, str) | slice | 'all'
            Key(s) for spectra. May be either the integer index, the
            string comment, or a tuple of both. See :meth:`print_keys`
            for all registered keys. Can also be 'all', which hides
            all registered spectra.

        See Also
        --------
        :meth:`drop`
        :meth:`show`

        Examples
        --------
        The following are equivalent for a :class:`Spectrometer` with
        keys ``[(0, 'a'), (1, 'b')]``::

            spect.hide(0)
            spect.hide('a')
            spect.hide(-2)
            spect.hide((0, 'a'))

        Multiple spectra can be hidden at the same time::

            spect.hide(0, (1, 'b'))

        """
        try:
            for key in self._parse_keys(*self._unravel_coi(*comment_or_index)):
                self._plot_manager.destroy_lines(keys=[key])
                self._plot_manager.update_line_attrs(self._plot_manager.plots_to_draw,
                                                     self._plot_manager.lines_to_draw,
                                                     [key], stale=False, hidden=True)
        finally:
            with self._plot_manager.plot_context:
                self._plot_manager.update_figure()

    def show(self, *comment_or_index: _keyT, color: Optional[Union[str, List[str]]] = None):
        """Show a spectrum in the plot.

        Parameters
        ----------
        *comment_or_index : int | str | (int, str) | slice | 'all'
            Key(s) for spectra. May be either the integer index, the
            string comment, or a tuple of both. See :meth:`print_keys`
            for all registered keys. Can also be 'all', which shows
            all registered spectra.
        color: str or list[str]
            A valid matplotlib color to override the default color for
            this key.

        See Also
        --------
        :meth:`drop`
        :meth:`hide`

        Examples
        --------
        The following are equivalent for a :class:`Spectrometer` with
        keys ``[(0, 'a'), (1, 'b')]``::

            spect.show(0)
            spect.show('a')
            spect.show(-2)
            spect.show((0, 'a'))

        Multiple spectra can be shown at the same time::

            spect.show(0, (1, 'b'))

        You can override the default color for the spectrum::

            spect.show(0, color='pink')
            spect.show(0, 1, color=['k', 'r'])

        """
        # Need to unravel 'all' or slice for colors below
        comment_or_index = self._unravel_coi(*comment_or_index)

        if color is not None:
            if colors.is_color_like(color):
                color = [color]
            assert len(color) == len(comment_or_index), 'Need as many colors as there are keys'
        else:
            color = [None]*len(comment_or_index)

        try:
            for key, col in zip(self._parse_keys(*comment_or_index), color):
                # Color kwarg needs to be set for all plot and line types
                # (also the ones not currently shown)
                self._plot_manager.update_line_attrs(keys=[key], color=col)
                self._plot_manager.update_line_attrs(self._plot_manager.plots_to_draw,
                                                     self._plot_manager.lines_to_draw,
                                                     [key], stale=True, hidden=False)
        finally:
            with self._plot_manager.plot_context:
                self._plot_manager.update_figure()

    def reprocess_data(self,
                       *comment_or_index: _keyT,
                       save: Literal[False, True, 'overwrite'] = False,
                       processed_unit: Optional[str] = None,
                       **new_settings):
        """Repeat data processing using updated settings.

        .. warning::
            This can change data saved on disk!

        Parameters
        ----------
        *comment_or_index : int | str | (int, str) | slice | 'all'
            Key(s) for spectra. May be either the integer index, the
            string comment, or a tuple of both. See :meth:`print_keys`
            for all registered keys. Can also be 'all', which processes
            all registered spectra.
        save : bool or 'overwrite', default False
            Save the processed data to a new or overwrite the old file.
        processed_unit : str, optional
            A string for the new unit if it changes.
        **new_settings
            Updated keyword argument settings for data processing using
            :attr:`procfn` or :attr:`fourier_procfn`. Previous settings
            are used for those not provided here.
        """
        try:
            for key in self._parse_keys(*self._unravel_coi(*comment_or_index)):
                data = self._data[key]
                data.update(self._process_data(self._data[key]['timetrace_raw'],
                                               **{**data['settings'], **new_settings}))

                if save:
                    if save == 'overwrite':
                        data['filepath'] = io.query_overwrite(data['filepath'])
                    else:
                        data['filepath'] = self._get_new_file(comment=data['comment'])
                    self._savefn(data['filepath'], **data)

                self._data[key] = data
                self._plot_manager.update_line_attrs(self._plot_manager.plots_to_draw,
                                                     self._plot_manager.lines_to_draw,
                                                     keys=[key], stale=True)
        finally:
            if processed_unit is not None:
                self._plot_manager.processed_unit = str(processed_unit)
                self._plot_manager.setup_figure()
            else:
                with self._plot_manager.plot_context:
                    self._plot_manager.update_figure()

    def set_reference_spectrum(self, comment_or_index: Optional[_keyT] = None):
        """Set the spectrum to be taken as a reference for the dB scale.

        Applies only if :attr:`plot_dB_scale` is True."""
        # Cannot implement this as a setter for the reference_spectrum propert
        # since we need the _parse_keys method of Spectrometer.
        if comment_or_index is None:
            # Default for no data
            if self._data:
                comment_or_index = 0
            else:
                return
        key = self._parse_keys(comment_or_index)[0]
        if key != self._plot_manager._reference_spectrum:
            self._plot_manager._reference_spectrum = key
            if self.plot_dB_scale:
                self._plot_manager.update_line_attrs(['main', 'cumulative'],
                                                     self._plot_manager.lines_to_draw,
                                                     stale=True)
                self._plot_manager.setup_figure()

    def update_metadata(self, comment_or_index: _keyT, *, delete_old_file: bool = False,
                        new_comment: Optional[str] = None,
                        new_settings: Optional[Mapping[str, Any]] = None,
                        new_savepath: Union[bool, _pathT] = False):
        """Update the metadata of a previously acquired spectrum and
        write it to disk.

        .. warning::
            This can change data saved on disk!

        Parameters
        ----------
        *comment_or_index : int | str | (int, str)
            Key for spectrum. May be either the integer index, the
            string comment, or a tuple of both. See :meth:`print_keys`
            for all registered keys.
        delete_old_file : bool
            Rename the file on disk according to the updated comment.
            If false, a new file is written and the old retained.
            Default: False.

            .. note::
                The new file will have the same timestamp but possibly
                a different comment and therefore filename. Thus, any
                old serialization files will have dead filename links
                generated by :meth:`save_run` and you should
                re-serialize the object.

        new_comment : str
            A new comment replacing the old one.
        new_settings : Mapping[str, Any]
            New (metadata) settings to add to/replace existing ones.

            .. warning::
                This might overwrite settings used for spectral
                estimation. In some cases, it might be better to delete
                the previous spectrum from disk and acquire a new one.

        new_savepath : bool or PathLike, default: False
            Use this object's savepath or a specified one instead of
            the one stored in the file. Helpful for handling data
            that has been moved to a different system.
        """
        old_key = self._parse_keys(comment_or_index)[0]
        lines = self._plot_manager.lines.pop(old_key)
        data = self._data.pop(old_key)
        backup = {'comment': copy.deepcopy(data['comment']),
                  'settings': copy.deepcopy(data['settings']),
                  'filepath': copy.deepcopy(data['filepath'])}

        try:
            if delete_old_file and io.query_yes_no(f"Really delete file {backup['filepath']}?",
                                                   default='no'):
                os.remove(backup['filepath'])
            if new_comment is not None:
                data['comment'] = new_comment
            if new_settings is not None:
                data['settings'].update(new_settings)
            if new_savepath is False:
                savepath = backup['filepath'].parent
            elif new_savepath is True:
                savepath = self.savepath
            else:
                savepath = Path(new_savepath)
            data['filepath'] = savepath / (
                # trunk and timestamp parts of the filename
                backup['filepath'].stem[:37]
                # new comment tail
                + (('_' + _make_filesystem_compatible(data['comment'])) if data['comment'] else '')
            )
            new_key = (old_key[0], data['comment'])

            self._savefn(data['filepath'], **data)
            self._data[new_key] = data

            # Housekeeping
            if self.reference_spectrum == old_key:
                self.set_reference_spectrum(new_key)

            self._plot_manager.lines[new_key] = lines
            with self._plot_manager.plot_context:
                self._plot_manager.update_figure()
        except FileNotFoundError:
            # trying to modify data on a non-existent path
            data.update(backup)
            self._data[old_key] = data
            self._plot_manager.lines[old_key] = lines
            raise
        except:  # noqa
            # Restore previous state
            try:
                del self._plot_manager.lines[new_key]
            except (NameError, KeyError):
                pass
            try:
                del self._data[new_key]
            except (NameError, KeyError):
                pass

            data.update(backup)
            self._data[old_key] = data
            self._savefn(data['filepath'], **data)
            self._plot_manager.lines[old_key] = lines
            print('Restored old metadata.')

    def save_run(self, file: Optional[_pathT] = None, verbose: bool = False) -> Path:
        """Saves the names of all data files to a text file."""
        if file:
            file = io.to_global_path(
                str(self._resolve_relative_path(file)) + '_files'
            ).with_suffix('.txt')
        else:
            file = self._runfile
        file = io.check_path_length(file)
        file.write_text('\n'.join(self.files))
        if verbose:
            print(f'Wrote filenames to {file}.')
        return file

    @mock.patch.multiple('shelve', Unpickler=dill.Unpickler, Pickler=dill.Pickler)
    def serialize_to_disk(self, file: Optional[_pathT] = None, protocol: int = -1,
                          verbose: bool = False):
        """Serialize the Spectrometer object to disk.

        Parameters
        ----------
        file : str | Path
            Where to save the data. Defaults to the same directory where
            also the spectral data is saved.
        protocol : int
            The pickle protocol to use.
        verbose : bool
            Print some progress updates.

        See Also
        --------
        :meth:`recall_from_disk`
        """
        # shelve writes three files, .dat, .bak, and .dir. Only need to check for one
        file = io.check_path_length(io.query_overwrite(
            _resolve_shelve_file(self._resolve_relative_path(file or self._objfile))
        )).with_suffix('')

        spectrometer_attrs = ['psd_estimator', 'procfn', 'savepath', 'plot_raw', 'plot_timetrace',
                              'plot_cumulative', 'plot_negative_frequencies',
                              'plot_absolute_frequencies', 'plot_amplitude', 'plot_density',
                              'plot_cumulative_normalized', 'plot_style', 'plot_update_mode',
                              'plot_dB_scale', 'compress']
        plot_manager_attrs = ['reference_spectrum', 'prop_cycle', 'raw_unit', 'processed_unit']
        with shelve.open(str(file), protocol=protocol) as db:
            # Constructor args
            for attr in spectrometer_attrs:
                try:
                    db[attr] = getattr(self, attr)
                except AttributeError:
                    pass
            for attr in plot_manager_attrs:
                try:
                    db[attr] = getattr(self._plot_manager, attr)
                except AttributeError:
                    pass
            # Write a text file with the locations of all data files
            db['runfile'] = self.save_run(file, verbose=verbose)
        if verbose:
            print(f'Wrote object data to {file}')

    @classmethod
    @mock.patch.multiple('shelve', Unpickler=dill.Unpickler, Pickler=dill.Pickler)
    def recall_from_disk(cls, file: _pathT, daq: Optional[DAQ] = None, *,
                         reprocess_data: bool = False, **new_settings):
        """Restore a Spectrometer object from disk.

        Parameters
        ----------
        file : str | Path
            The saved file.
        daq : DAQ
            The :class:`.DAQ` instance that sets up and executes data
            acquisition (see also the class constructor).

            If not given, the instance is read-only and can only be used
            for processing and plotting old data.
        reprocess_data : bool
            Redo the processing steps using this object's :attr:`procfn`
            and :attr:`psd_estimator`. Default: False.

        See Also
        --------
        :meth:`serialize_to_disk`
        """

        if not (file := _resolve_shelve_file(io.to_global_path(file))).exists():
            raise FileNotFoundError(f'File {file} does not exist!')
        with shelve.open(str(file.with_suffix(''))) as db:
            if not db:
                raise FileNotFoundError(f'File {file} is empty!')
            try:
                kwargs = dict(**db)
            except TypeError:
                # Weirdly, if a serialized function object does not exist in the
                # namespace, a TypeError is raised instead of complaining about
                # said object. Therefore, go through the db one-by-one to trigger
                # the error on the object actually causing problems
                kwargs = dict()
                for key, val in db.items():
                    kwargs[key] = val

            spectrum_files = np.array(
                io.to_global_path(kwargs.pop('runfile')).read_text().split('\n')
            )

        # Need to treat reference_spectrum separately since it is not a
        # Spectrometer but a _PlotManager attribute.
        reference_spectrum = kwargs.pop('reference_spectrum', None)

        spectrometer = cls(daq=daq, **cls._make_kwargs_compatible(kwargs))

        # Then restore the data
        keys = []
        for i, file in enumerate(progressbar(spectrum_files, desc='Loading files')):
            try:
                keys.append(spectrometer.add_spectrum_from_file(file, show=False,
                                                                reprocess_data=reprocess_data,
                                                                **new_settings))
            except FileNotFoundError:
                print(f'Could not retrieve file {file}. Skipping.')

        spectrometer.set_reference_spectrum(reference_spectrum)
        # Show all at once to save drawing time
        spectrometer.show(*keys)
        return spectrometer

    def add_spectrum_from_file(self, file: _pathT, show: bool = True, color: Optional[str] = None,
                               reprocess_data: bool = False, **new_settings) -> Tuple[int, str]:
        """Load data from disk and display it in the current figure.

        Parameters
        ----------
        file : str | os.PathLike
            The file to be loaded.
        show : bool
            Show the added spectrum in the plot.
        color : str
            A custom color to be used for the spectrum.
        reprocess_data : bool
            Redo the processing steps using this object's :attr:`procfn`
            and :attr:`psd_estimator`. Default: False.
        **new_settings
            New settings to use for reprocessing the data.

        Returns
        -------
        key : Tuple[int, str]
            The key assigned to the new spectrum data.

        """
        data = _load_spectrum(self._resolve_relative_path(file).with_suffix('.npz'))

        if reprocess_data:
            data.update(self._process_data(data['timetrace_raw'],
                                           **{**data['settings'], **new_settings}))

        key = (self._index, data['comment'])
        self._data[key] = data
        self._plot_manager.add_new_line_entry(key)
        if show:
            self.show(key, color=color)
        else:
            # Sets flags correctly
            self.hide(key)
        return key

    def print_settings(self, comment_or_index: _keyT):
        """Convenience method to pretty-print the settings for a
        previously acquired spectrum."""
        key = self._parse_keys(comment_or_index)[0]
        print(f'Settings for key {key}:')
        pprint(self[key]['settings'], width=120)

    def print_keys(self, *comment_or_index: _keyT):
        """Prints the registered (index, comment) tuples."""
        print(self._repr_keys(*self._parse_keys(*comment_or_index)))

    def keys(self) -> List[Tuple[int, str]]:
        """Registered keys (sorted)."""
        return sorted(self._data.keys())

    def values(self) -> List[Dict[str, Any]]:
        """Registered data (sorted by keys)."""
        return [value for _, value in sorted(self._data.items())]

    def items(self) -> List[Tuple[Tuple[int, str], Dict[str, Any]]]:
        """Registered (key, data) tuples (sorted by keys)."""
        return [(key, value) for key, value in sorted(self._data.items())]


def _load_spectrum(file: _pathT) -> Dict[str, Any]:
    """Loads data from a spectrometer run."""
    class monkey_patched_io:
        # Wrap around data saved during JanewayPath folly
        class JanewayWindowsPath(os.PathLike):
            def __init__(self, *args):
                self.path = Path(*args)

            def __fspath__(self):
                return str(self.path)

        def __enter__(self):
            setattr(io, 'JanewayWindowsPath', self.JanewayWindowsPath)

        def __exit__(self, exc_type, exc_val, exc_tb):
            delattr(io, 'JanewayWindowsPath')

    with np.load(file, allow_pickle=True) as fp, monkey_patched_io():
        data = {}
        for key, val in fp.items():
            try:
                # Squeeze singleton arrays into native Python data type
                data[key] = val.item()
            except ValueError:
                data[key] = val
            except Exception as err:
                raise RuntimeError(f'Encountered unhandled object in file {file}') from err

    return _from_native_types(data)


def _ax_unit(amplitude: bool, density: bool, integrated: bool, cumulative_normalized: bool,
             dB: bool, unit: str) -> str:
    if integrated and cumulative_normalized:
        return ' (a.u.)'
    if dB:
        unit = 'dB'
    power = '$^2$' if not amplitude and not dB else ''
    hz_mul = 'Hz' if integrated and not density else ''
    if density and not integrated:
        return ' ({unit}{power}{hz_mul}{hz_div})'.format(
            unit=unit,
            power=power,
            hz_mul=hz_mul,
            hz_div=r'/$\sqrt{\mathrm{Hz}}$' if amplitude and density else r'/$\mathrm{Hz}$'
        )
    return ' ({unit}{power}{hz_mul})'.format(
        unit=unit,
        power=power,
        hz_mul=hz_mul,
    )


def _ax_label(amplitude: bool, integrated: bool, dB: bool, reference: _keyT) -> str:
    if not dB:
        return '{a}{b}S{c}(f){d}'.format(
            a=r'$\sqrt{{' if amplitude else '$',
            b=r'\int_0^f\mathrm{{d}}f^\prime ' if integrated else '',
            c='^2' if integrated and amplitude else '',
            d='}}$' if amplitude else '$'
        )
    return '{a}{b} relative to index {c}'.format(
        a='integrated ' if integrated else '',
        b='amplitude' if amplitude else 'power',
        c=reference[0]
    ).capitalize()


def _make_filesystem_compatible(comment: str) -> str:
    for old, new in zip((' ', '/', '.', ':', '\\', '|', '*', '?', '<', '>'),
                        ('_', '_', '-', '-', '_', '_', '_', '_', '_', '_')):
        comment = comment.replace(old, new)
    return comment


def _merge_data_dicts(data: Dict[str, Any], new_data: Dict[str, Any]) -> Dict[str, Any]:
    for key, val in new_data.items():
        if key == 'settings' or key.startswith('f'):
            # Only store single copy of frequency arrays / settings
            data[key] = val
        else:
            if key not in data:
                data[key] = []
            # Append new data arrays to list of existing
            data[key].append(val)
    return data


def _resolve_shelve_file(path: Path) -> Path:
    # shelve writes a single file without suffix or three files with suffixes
    # .dat, .dir, .bak depending on the dbm implementation available.
    if (p := path.with_suffix('')).is_file():
        return p
    if (p := path.with_suffix('.dat')).is_file():
        return p
    return path


def _to_native_types(data: Dict[str, Any]) -> Dict[str, Any]:
    """Converts custom types to native Python or NumPy types."""
    data_as_native_types = dict()
    for key, val in data.items():
        if isinstance(val, Path):
            # Cannot instantiate WindowsPaths on Posix and vice versa
            data_as_native_types[key] = str(val)
        elif isinstance(val, daq_settings.DAQSettings):
            # DAQSettings might not be available on system loading the
            # data, so unravel to consistent Python dict.
            data_as_native_types[key] = val.to_consistent_dict()
        else:
            data_as_native_types[key] = val
    return data_as_native_types


def _from_native_types(data: Dict[str, Any]) -> Dict[str, Any]:
    """Inverts :func:`_to_native_types`."""
    for key, val in data.items():
        if key == 'filepath':
            data[key] = Path(data[key])
        elif key == 'settings':
            data[key] = daq_settings.DAQSettings(data[key])
        else:
            data[key] = val
    return data


class ReadonlyError(Exception):
    """Indicates a :class:`Spectrometer` object is read-only."""
    pass

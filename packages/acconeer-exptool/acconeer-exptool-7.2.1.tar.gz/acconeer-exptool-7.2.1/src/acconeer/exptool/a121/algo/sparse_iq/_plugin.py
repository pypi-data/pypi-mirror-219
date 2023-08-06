# Copyright (c) Acconeer AB, 2022-2023
# All rights reserved

from __future__ import annotations

import logging
from enum import Enum, auto
from typing import Callable, Tuple, Type

import numpy as np
import numpy.typing as npt

from PySide6.QtGui import QTransform
from PySide6.QtWidgets import QWidget

import pyqtgraph as pg

import acconeer.exptool as et
from acconeer.exptool import a121
from acconeer.exptool.a121 import algo
from acconeer.exptool.a121.algo._plugins import (
    ProcessorBackendPluginBase,
    ProcessorPlotPluginBase,
    ProcessorPluginPreset,
    ProcessorPluginSpec,
    ProcessorViewPluginBase,
)
from acconeer.exptool.app.new import (
    AppModel,
    Message,
    PidgetFactoryMapping,
    PluginFamily,
    PluginGeneration,
    PluginPresetBase,
    pidgets,
)

from ._processor import (
    AmplitudeMethod,
    Processor,
    ProcessorConfig,
    ProcessorResult,
    get_sensor_config,
)


log = logging.getLogger(__name__)


class PluginPresetId(Enum):
    DEFAULT = auto()


class BackendPlugin(ProcessorBackendPluginBase[ProcessorConfig, ProcessorResult]):

    PLUGIN_PRESETS = {
        PluginPresetId.DEFAULT.value: lambda: ProcessorPluginPreset(
            session_config=a121.SessionConfig(get_sensor_config()),
            processor_config=BackendPlugin.get_processor_config_cls()(),
        ),
    }

    @classmethod
    def get_processor_cls(cls) -> Type[Processor]:
        return Processor

    @classmethod
    def get_processor_config_cls(cls) -> Type[ProcessorConfig]:
        return ProcessorConfig

    @classmethod
    def get_default_sensor_config(cls) -> a121.SensorConfig:
        return get_sensor_config()


class ViewPlugin(ProcessorViewPluginBase[ProcessorConfig]):
    @classmethod
    def get_pidget_mapping(cls) -> PidgetFactoryMapping:
        return {
            "amplitude_method": pidgets.EnumPidgetFactory(
                enum_type=AmplitudeMethod,
                name_label_text="Amplitude method:",
                name_label_tooltip=(
                    "The method used to calculate the amplitude from the complex Sparse IQ data"
                ),
                label_mapping={
                    AmplitudeMethod.COHERENT: "Coherent",
                    AmplitudeMethod.NONCOHERENT: "Non-coherent",
                    AmplitudeMethod.FFT_MAX: "FFT Max",
                },
            )
        }

    @classmethod
    def get_processor_config_cls(cls) -> Type[ProcessorConfig]:
        return ProcessorConfig

    @classmethod
    def supports_multiple_subsweeps(self) -> bool:
        return True


class PlotPlugin(ProcessorPlotPluginBase[ProcessorResult]):
    def __init__(self, *, plot_layout: pg.GraphicsLayout, app_model: AppModel) -> None:
        super().__init__(plot_layout=plot_layout, app_model=app_model)
        self.smooth_max = et.utils.SmoothMax()

    def setup(self, metadata: a121.Metadata, sensor_config: a121.SensorConfig) -> None:
        self.ampl_plot = self._create_amplitude_plot(self.plot_layout, sensor_config.num_subsweeps)
        self.plot_layout.nextRow()
        self.phase_plot = self._create_phase_plot(self.plot_layout, sensor_config.num_subsweeps)
        self.plot_layout.nextRow()

        self.ampl_curves = []
        self.phase_curves = []
        self.ft_plots = []
        self.ft_im_list = []
        self.distances_m_list = []

        vels, vel_res = algo.get_approx_fft_vels(metadata, sensor_config)

        for i, subsweep in enumerate(sensor_config.subsweeps):
            distances_m, step_length_m = algo.get_distances_m(subsweep, metadata)
            self.distances_m_list.append(distances_m)

            ampl_curve = self._create_amplitude_curve(i, distances_m)
            self.ampl_plot.addItem(ampl_curve)
            self.ampl_curves.append(ampl_curve)

            phase_curve = self._create_phase_curve(i)
            self.phase_plot.addItem(phase_curve)
            self.phase_curves.append(phase_curve)

            ft_plot, ft_im = self._create_fft_plot(
                self.plot_layout,
                distances_m=distances_m,
                step_length_m=step_length_m,
                vels=vels,
                vel_res=vel_res,
            )
            self.ft_plots.append(ft_plot)
            self.ft_im_list.append(ft_im)

    def update(self, processor_result: ProcessorResult) -> None:
        max_ = 0.0

        for i, result in enumerate(processor_result):
            ampls = result.amplitudes
            self.ampl_curves[i].setData(self.distances_m_list[i], ampls)
            self.phase_curves[i].setData(self.distances_m_list[i], result.phases)
            dvm = result.distance_velocity_map
            self.ft_im_list[i].updateImage(
                dvm.T,
                levels=(0, 1.05 * np.max(dvm)),
            )

            max_ = max(max_, np.max(ampls).item())

        self.ampl_plot.setYRange(0, self.smooth_max.update(max_))

    @staticmethod
    def _create_amplitude_curve(
        cycle_num: int, depths_m: npt.NDArray[np.float_]
    ) -> pg.PlotDataItem:
        pen = et.utils.pg_pen_cycler(cycle_num)

        if len(depths_m) > 32:
            return pg.PlotDataItem(pen=pen)
        else:
            brush = et.utils.pg_brush_cycler(cycle_num)
            return pg.PlotDataItem(
                pen=pen, symbol="o", symbolSize=5, symbolBrush=brush, symbolPen="k"
            )

    @staticmethod
    def _create_phase_curve(cycle_num: int) -> pg.PlotDataItem:
        brush = et.utils.pg_brush_cycler(cycle_num)
        return pg.PlotDataItem(
            pen=None, symbol="o", symbolSize=5, symbolBrush=brush, symbolPen="k"
        )

    @staticmethod
    def _create_amplitude_plot(parent: pg.GraphicsLayout, colspan: int) -> pg.PlotItem:
        ampl_plot = parent.addPlot(colspan=colspan)
        ampl_plot.setMenuEnabled(False)
        ampl_plot.showGrid(x=True, y=True)
        ampl_plot.setLabel("left", "Amplitude")
        return ampl_plot

    @staticmethod
    def _create_phase_plot(parent: pg.GraphicsLayout, colspan: int) -> pg.PlotItem:
        phase_plot = parent.addPlot(colspan=colspan)
        phase_plot.setMenuEnabled(False)
        phase_plot.showGrid(x=True, y=True)
        phase_plot.setLabel("left", "Phase")
        phase_plot.setYRange(-np.pi, np.pi)
        phase_plot.getAxis("left").setTicks(et.utils.pg_phase_ticks)
        return phase_plot

    @staticmethod
    def _create_fft_plot(
        parent: pg.GraphicsLayout,
        *,
        distances_m: npt.NDArray[np.float_],
        step_length_m: float,
        vels: npt.NDArray[np.float_],
        vel_res: float,
    ) -> Tuple[pg.PlotItem, pg.ImageItem]:
        transform = QTransform()
        transform.translate(distances_m[0], vels[0] - 0.5 * vel_res)
        transform.scale(step_length_m, vel_res)

        im = pg.ImageItem(autoDownsample=True)
        im.setLookupTable(et.utils.pg_mpl_cmap("viridis"))
        im.setTransform(transform)

        plot = parent.addPlot()
        plot.setMenuEnabled(False)
        plot.setLabel("bottom", "Distance (m)")
        plot.setLabel("left", "Velocity (m/s)")
        plot.addItem(im)

        return plot, im


class PluginSpec(
    ProcessorPluginSpec[a121.Result, ProcessorConfig, ProcessorResult, a121.Metadata]
):
    def create_backend_plugin(
        self, callback: Callable[[Message], None], key: str
    ) -> BackendPlugin:
        return BackendPlugin(callback=callback, generation=self.generation, key=key)

    def create_view_plugin(self, app_model: AppModel, view_widget: QWidget) -> ViewPlugin:
        return ViewPlugin(app_model=app_model, view_widget=view_widget)

    def create_plot_plugin(
        self, app_model: AppModel, plot_layout: pg.GraphicsLayout
    ) -> PlotPlugin:
        return PlotPlugin(app_model=app_model, plot_layout=plot_layout)


SPARSE_IQ_PLUGIN = PluginSpec(
    generation=PluginGeneration.A121,
    key="sparse_iq",
    title="Sparse IQ",
    description="Basic usage of the sparse IQ service.",
    family=PluginFamily.SERVICE,
    presets=[
        PluginPresetBase(name="Default", preset_id=PluginPresetId.DEFAULT),
    ],
    default_preset_id=PluginPresetId.DEFAULT,
)

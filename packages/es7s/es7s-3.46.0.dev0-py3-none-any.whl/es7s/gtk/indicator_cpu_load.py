# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import typing as t
from pytermor import format_auto_float

from ._base import _BaseIndicator, CheckMenuItemConfig, _BoolState, _State, RadioMenuItemConfig
from es7s.shared import SocketMessage, get_merged_uconfig
from es7s.shared.dto import CpuInfo


class IndicatorCpuLoad(_BaseIndicator[CpuInfo]):
    def __init__(self):
        self.config_section = "indicator.cpu-load"

        self._show_perc = _BoolState(
            config_var=(self.config_section, "label-current"),
            gconfig=CheckMenuItemConfig("Show current (%)", sep_before=True),
        )
        self._show_avg_off = _BoolState(
            config_var=(self.config_section, "label-average"),
            config_var_value="off",
            gconfig=RadioMenuItemConfig("No average", sep_before=True, group=self.config_section),
        )
        self._show_avg = _BoolState(
            config_var=(self.config_section, "label-average"),
            config_var_value="one",
            gconfig=RadioMenuItemConfig("Show average (1min)", group=self.config_section),
        )
        self._show_avg3 = _BoolState(
            config_var=(self.config_section, "label-average"),
            config_var_value="three",
            gconfig=RadioMenuItemConfig("Show average (1/5/15min)", group=self.config_section),
        )

        super().__init__(
            indicator_name="cpu-load",
            socket_topic="cpu",
            icon_subpath="cpuload",
            icon_name_default="0.svg",
            icon_path_dynamic_tpl="%d.svg",
            icon_thresholds=[
                100,
                95,
                87,
                75,
                62,
                50,
                37,
                25,
                12,
                0,
            ],
            title="CPU",
            states=[self._show_perc, self._show_avg_off, self._show_avg, self._show_avg3],
        )

    def _render(self, msg: SocketMessage[CpuInfo]):
        self._update_title(self._format_result(msg.data.load_perc, *msg.data.load_avg, ignore_setup=True))
        self._render_result(
            self._format_result(msg.data.load_perc, *msg.data.load_avg),
            self._format_result(100, *[16.16] * len(msg.data.load_avg)),
            icon=self._select_icon(msg.data.load_perc),
        )

    def _format_result(self, perc: float, *avg: float, ignore_setup = False) -> str:
        parts = []
        if self._show_perc.active or ignore_setup:
            parts += [f"{perc:3.0f}% "]
        if self._show_avg3.active or ignore_setup:
            parts += (format_auto_float(a, 4) for a in avg)
        elif self._show_avg.active:
            parts += (format_auto_float(avg[0], 4),)
        return " ".join(parts).rstrip()

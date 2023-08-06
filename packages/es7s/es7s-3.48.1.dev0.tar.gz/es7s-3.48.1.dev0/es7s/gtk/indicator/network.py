# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------

import pytermor as pt

from es7s.shared import SocketMessage
from es7s.shared.dto import (
    NetworkCountryInfo,
    NetworkLatencyInfo,
    NetworkUsageInfo,
    NetworkUsageInfoStats,
)
from ._base import CheckMenuItemConfig, WAIT_PLACEHOLDER, _BaseIndicator, _BoolState

NetworkInfo = NetworkUsageInfo | NetworkLatencyInfo | NetworkCountryInfo


class IndicatorNetwork(_BaseIndicator[NetworkInfo]):
    RENDER_INTERVAL_SEC = 1.0

    def __init__(self):
        self.config_section = "indicator.network"
        self._interface = None
        self._last_dto = dict[type, NetworkInfo]()
        self._netcom = False

        self._show_rate = _BoolState(
            config_var=(self.config_section, "label_rate"),
            gconfig=CheckMenuItemConfig("Show rate (bit/s, max)", sep_before=True),
        )
        self._show_latency = _BoolState(
            config_var=(self.config_section, "label_latency"),
            gconfig=CheckMenuItemConfig("Show latency/delivery rate"),
        )
        self._show_country = _BoolState(
            config_var=(self.config_section, "label_country"),
            gconfig=CheckMenuItemConfig("Show country code"),
        )

        super().__init__(
            indicator_name="network",
            socket_topic=["network-usage", "network-latency", "network-country"],
            icon_subpath="network",
            icon_name_default="off.svg",
            icon_path_dynamic_tpl="%s-%s%s.svg",
            title="Network",
            states=[self._show_rate, self._show_latency, self._show_country],
        )
        self._formatter = pt.StaticFormatter(
            pt.formatter_bytes_human,
            max_value_len=4,
            auto_color=False,
            allow_negative=False,
            allow_fractional=True,
            discrete_input=False,
            unit="",
            unit_separator="",
            pad=True,
        )

    def _update_interface(self, last_usage: NetworkUsageInfo = None):
        if not last_usage:
            return
        self._interface = last_usage.interface

    def _render(self, msg: SocketMessage[NetworkInfo]):
        self._netcom = False
        self._last_dto.update({type(msg.data): msg.data})

        if hasattr(msg, "network_comm") and msg.network_comm:
            self._netcom = True

        if not (last_usage := self._get_last_usage()):
            self._render_no_data()
            return

        if not last_usage.isup:
            self._render_result("N/A", "N/A", icon=self._icon_name_default)
            return

        frames, bpss = [], []
        for uis in (last_usage.sent, last_usage.recv):
            if not uis:
                frames.append("0")
                bpss.append(None)
                continue
            frames.append(self._get_icon_frame(uis))
            bpss.append(uis.bps)

        frames.append("-nc" if self._netcom else "")
        icon = self._icon_path_dynamic_tpl % (*frames,)
        result = self._format_result(*bpss)
        self._update_title(self._format_result(*bpss, ignore_setup=True), f"[{self._interface}]")
        self._render_result(result, result, icon=icon)

    def _get_last_usage(self) -> NetworkUsageInfo | None:
        if last_usage := self._last_dto.get(NetworkUsageInfo, None):
            self._update_interface(last_usage)
        return last_usage

    def _get_failed_ratio(self) -> float:
        if last_latency := self._last_dto.get(NetworkLatencyInfo, None):
            return last_latency.failed_ratio
        return 0.0

    def _get_icon_frame(self, uis: NetworkUsageInfoStats) -> str:
        failed_ratio = self._get_failed_ratio()
        if uis.errors or failed_ratio > 0.5:
            return "e"
        if uis.drops or failed_ratio > 0.0:
            return "w"
        if uis.bps:
            if uis.bps > 1e7:  # 10 Mbps
                return "4"
            if uis.bps > 1e6:  # 1 Mbps
                return "3"
            if uis.bps > 1e5:  # 100 kbps
                return "2"
            if uis.bps > 1e4:  # 10 kpbs
                return "1"
        # if uis.ratio:
        #     if uis.ratio > 0.4:
        #         return "4"
        #     if uis.ratio > 0.2:
        #         return "3"
        #     if uis.ratio > 0.1:
        #         return "2"
        #     if uis.ratio > 0.01:
        #         return "1"
        return "0"

    def _format_result(self, *bps_values: float | None, ignore_setup=False) -> str:
        result = " ".join(
            res
            for res in [
                self._format_usage(*bps_values, ignore_setup=ignore_setup),
                self._format_latency(ignore_setup=ignore_setup),
                self._format_country(ignore_setup=ignore_setup),
            ]
            if res
        )
        if ignore_setup:
            return result.strip()
        return result

    def _format_usage(self, *bps_values: float | None, ignore_setup=False) -> str:
        if not self._show_rate and not ignore_setup:
            return ""
        if ignore_setup and len(bps_values) > 1:
            return f"↑{self._format_usage(bps_values[0], ignore_setup=True)} ↓{self._format_usage(bps_values[1], ignore_setup=True)} "
        if not any(bps_values):
            return " 0.0k"
        val = max(bps_values)
        if val < 1000:
            return "<1.0k"
        return self._formatter.format(val)

    def _format_latency(self, ignore_setup=False) -> str:
        if not self._show_latency and not ignore_setup:
            return ""
        if not (last_latency := self._last_dto.get(NetworkLatencyInfo, None)):
            return WAIT_PLACEHOLDER
        if last_latency.failed_ratio:
            return f"{100*(1-last_latency.failed_ratio):3.0f}%"
        val, sep, pfx, unit = pt.formatter_time_ms._format_raw(last_latency.latency_s * 1000)
        return " " * max(0, 4 - len(val + pfx + unit)) + val + pfx + unit

    def _format_country(self, ignore_setup=False) -> str:
        if not self._show_country and not ignore_setup:
            return ""
        if not (last_country := self._last_dto.get(NetworkCountryInfo, None)):
            return WAIT_PLACEHOLDER
        return last_country.country

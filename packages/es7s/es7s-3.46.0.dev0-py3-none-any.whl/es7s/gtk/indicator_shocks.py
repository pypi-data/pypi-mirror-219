# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import subprocess
from subprocess import CalledProcessError

import pytermor as pt

from ._base import (
    _BaseIndicator,
    _BoolState,
    CheckMenuItemConfig,
    _StaticState,
    _State,
    MenuItemConfig,
)
from es7s.shared import SocketMessage, get_logger, get_merged_uconfig
from es7s.shared.dto import NetworkTunnelInfo, ShocksInfo
from es7s.shared.strutil import to_subscript


class IndicatorShocks(_BaseIndicator):
    SYSTEMCTL_CALL_TIMEOUT_SEC = 60

    def __init__(self):
        self.config_section = "indicator.shocks"

        self._last_tunnel_info: NetworkTunnelInfo | None = None

        self._restart = _StaticState(
            callback=self._enqueue_restart,
            gconfig=MenuItemConfig("Restart ⚡ shocks daemon", sep_before=False),
        )
        self._show_lat = _BoolState(
            config_var=(self.config_section, "label"),
            gconfig=CheckMenuItemConfig("Show latency", sep_before=True),
        )
        self._latency_warning_threshold_ms = get_merged_uconfig().getint(
            self.config_section, "latency-warn-threshold-ms"
        )

        super().__init__(
            indicator_name="shocks",
            socket_topic=["shocks", "network-tunnel"],
            icon_subpath="shocks",
            icon_name_default="wait.svg",
            icon_path_dynamic_tpl="%s.svg",
            title="SSH/SOCKS proxy",
            states=[self._restart, self._show_lat],
        )

    def _restart_service(self):
        self._state.wait_timeout = self.SYSTEMCTL_CALL_TIMEOUT_SEC

        out, err = None, None
        try:
            try:
                cp = subprocess.run(
                    ["systemctl", "restart", "es7s-shocks"],
                    capture_output=True,
                    timeout=self.SYSTEMCTL_CALL_TIMEOUT_SEC,
                    check=True,
                )
            except CalledProcessError as e:
                out, err = e.stdout, e.stderr
                raise
        except Exception as e:
            get_logger().exception(e)
            self._add_timeout(self.RENDER_ERROR_TIMEOUT_SEC)
            self._render_error()
            self._monitor_data_buf.clear()
        else:
            out, err = cp.stdout, cp.stderr

        if out:
            get_logger().info(out)
        if err:
            get_logger().error(err)

    def _enqueue_restart(self, _=None):
        self._enqueue(self._restart_service)

    def _render(self, msg: SocketMessage[ShocksInfo | NetworkTunnelInfo]):
        if isinstance(msg.data, NetworkTunnelInfo):
            self._last_tunnel_info = msg.data
            return

        if self._state.is_waiting:
            if msg.data.running and msg.data.healthy:
                self._state.cancel_wait()
            else:
                icon = self._get_icon()
                if not self._show_lat:
                    self._render_result("", icon=icon)
                self._render_result("BUSY", icon=icon)
                return

        self._update_title(self._format_result(msg.data, ignore_setup=True))
        self._render_result(
            self._format_result(msg.data),
            icon=self._get_icon(msg.data, msg.network_comm),
        )

    def _format_result(self, data: ShocksInfo, ignore_setup = False) -> str:
        if not self._show_lat and not ignore_setup:
            return ""
        if not data.running:
            return "OFF"
        if not data.healthy:
            return "ERR"
        if not data.latency_s:
            return "---"
        if data.latency_s * 1000 >= self._latency_warning_threshold_ms:
            result = pt.format_auto_float(data.latency_s, 3, allow_exp_form=False) + "s"
        else:
            result = pt.format_time_ms(data.latency_s * 1e3)
        return result

    # noinspection PyMethodMayBeStatic
    def _get_icon_subtype(self, data: ShocksInfo = None, network_comm: bool = None) -> str:
        suffix = "-1"
        amount = self._last_tunnel_info.amount if self._last_tunnel_info else 0
        if network_comm:
            suffix = "-nc"
        elif amount:
            suffix = f"-{max(1, min(amount, 4))}"
        if not data or not data.running:
            return "disabled"
        if not data.healthy:
            return "failure" + suffix
        if not amount:
            return "wait"
        if (data.latency_s or 0) * 1000 >= self._latency_warning_threshold_ms:
            return "slow" + suffix
        return "up" + suffix

    def _get_icon(self, data: ShocksInfo = None, network_comm: bool = None) -> str:
        icon_subtype = self._get_icon_subtype(data, network_comm)
        return self._icon_path_dynamic_tpl % icon_subtype

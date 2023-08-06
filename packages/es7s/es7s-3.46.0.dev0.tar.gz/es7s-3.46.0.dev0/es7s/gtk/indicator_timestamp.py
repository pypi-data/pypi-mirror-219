# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import time

import pytermor as pt

from es7s.shared import SocketMessage, get_merged_uconfig
from es7s.shared.dto import TimestampInfo
from ._base import (
    CheckMenuItemConfig,
    MenuItemConfig,
    WAIT_PLACEHOLDER,
    _BaseIndicator,
    _BoolState,
    _StaticState,
)
from ..cli._foreign import ForeignInvoker


class IndicatorTimestamp(_BaseIndicator[TimestampInfo]):
    """
    ╭──────────╮                         ╭────────────╮
    │ Δ │ PAST │                         │ ∇ │ FUTURE │
    ╰──────────╯                         ╰────────────╯
             -1h  -30min   ṇọẉ   +30min  +1h
         ▁▁▁▁▁┌┴┐▁▁▁▁┌┴┐▁▁▁▁┌┴┐▁▁▁▁┌┴┐▁▁▁▁┌┴┐▁▁▁
       ⠄⠢⠲░░░░│▁│░░░░│▃│░░░░│█│░░░░│▀│░░░░│▔│░⣊⠈⣁⢉⠠⠂⠄
          ▔▔▔▔└┬┘▔▔▔▔└┬┘▔▔▔▔└┬┘▔▔▔▔└┬┘▔▔▔▔└┬┘▔▔▔▔
             ← 0%   +50%   +100%    |      |
                           -100%  -50%    -0% →
    """

    def __init__(self):
        self.config_section = "indicator.timestamp"
        self._formatter = pt.dual_registry.get_by_max_len(6)
        self._formatter._allow_fractional = False  # @FIXME (?) copied from monitor
        self._last_remote: int = 0
        self._invalidated_remote: int = 0

        self._reset = _StaticState(
            callback=self._enqueue_reset,
            gconfig=MenuItemConfig("Reset remote", sep_before=False),
        )
        self._show_value = _BoolState(
            config_var=(self.config_section, "label-value"),
            gconfig=CheckMenuItemConfig("Show value", sep_before=True),
        )

        super().__init__(
            indicator_name="timestamp",
            socket_topic="timestamp",
            icon_subpath="delta",
            icon_name_default="default.png",
            icon_path_dynamic_tpl="%s.png",
            title="Remote ∆T",
            states=[self._reset, self._show_value],
        )

    def _enqueue_reset(self, _=None):
        self._enqueue(self._reset_remote)

    def _reset_remote(self):
        self._invalidated_remote = self._last_remote
        self._update_title("")
        ForeignInvoker().spawn("-ic", 'remote "nalog add; nalog delete"', wait=False)

    def _render(self, msg: SocketMessage[TimestampInfo]):
        now = time.time()
        if (remote := msg.data.ts) is None:
            self._render_result("N/A", "N/A", True, self._get_icon("nodata", msg.network_comm))
            return
        self._last_remote = remote

        if self._invalidated_remote:
            if remote != self._invalidated_remote:
                self._invalidated_remote = 0
            else:
                self._render_result(
                    WAIT_PLACEHOLDER,
                    WAIT_PLACEHOLDER,
                    False,
                    self._get_icon("nodata", msg.network_comm),
                )
                return

        icon_subtype = self._get_icon_subtype(now, remote)
        icon = self._get_icon(icon_subtype, msg.data.ok, msg.network_comm)

        delta_str = self._formatter.format(now - remote)
        if get_merged_uconfig().get_indicator_debug_mode():
            delta_str += "|" + icon

        self._update_title(delta_str)

        if not self._show_value:
            delta_str = ""

        self._render_result(delta_str, delta_str, False, icon=icon)

    # noinspection PyMethodMayBeStatic
    def _get_icon_subtype(self, now: float, remote: int) -> str:
        prefix = "" if now > remote else "-"
        adiff = abs(now - remote)
        if adiff < 300:  # @TODO to config
            return "5m"
        if adiff < 3600:
            return f"{prefix}1h"
        if adiff < 3 * 3600:
            return f"{prefix}3h"
        if now < remote:
            return "future"
        return "default"

    def _get_icon(self, icon_subtype: str, ok: bool, network_comm: bool = None) -> str:
        if not ok:
            return self._icon_path_dynamic_tpl % "outdated"
        return self._icon_path_dynamic_tpl % (icon_subtype + ("-nc" if network_comm else ""))

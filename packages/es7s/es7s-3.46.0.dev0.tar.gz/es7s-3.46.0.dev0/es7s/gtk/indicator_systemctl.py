# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import random

from es7s.shared import SocketMessage, get_logger
from es7s.shared.dto import SystemCtlInfo
from ._base import _BaseIndicator


class IndicatorSystemCtl(_BaseIndicator[SystemCtlInfo]):
    def __init__(self):
        super().__init__(
            indicator_name="systemctl",
            socket_topic="systemctl",
            icon_name_default="systemctl",
            title="systemctl status",
            auto_visibility=True,
        )

    def _render(self, msg: SocketMessage[SystemCtlInfo]):
        if msg.data.ok:
            self._hidden.value = True
        else:
            self._hidden.value = False
        self._update_visibility()

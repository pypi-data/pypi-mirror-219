# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2022-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
from subprocess import CalledProcessError, CompletedProcess

from es7s.shared.dto import SystemCtlInfo
from ._base import DataProvider
from ..shared import get_logger, run_subprocess


class SystemCtlProvider(DataProvider[SystemCtlInfo]):
    def __init__(self):
        super().__init__("systemctl", "systemctl", poll_interval_sec=30.0)

    def _collect(self) -> SystemCtlInfo:
        try:
            cp: CompletedProcess = run_subprocess("systemctl", "is-system-running")
        except CalledProcessError as e:
            get_logger().exception(e)
            return SystemCtlInfo(ok=False)
        if not cp.stdout:
            return SystemCtlInfo(ok=False)

        status = cp.stdout.splitlines().pop(0)
        ok = (status == 'running')
        return SystemCtlInfo(status, ok)

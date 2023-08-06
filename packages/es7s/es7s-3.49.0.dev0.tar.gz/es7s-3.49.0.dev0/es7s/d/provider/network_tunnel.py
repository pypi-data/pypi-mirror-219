# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2022-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import subprocess as sub

from ._base import DataProvider
from es7s.shared.dto import NetworkTunnelInfo


# @deprecated
class NetworkTunnelProvider(DataProvider[NetworkTunnelInfo]):
    def __init__(self):
        super().__init__("network-tunnel", "network-tunnel", 2.0)

    def _reset(self):
        return NetworkTunnelInfo()

    def _collect(self) -> NetworkTunnelInfo:
        p: sub.CompletedProcess = sub.run(['pgrep', '-f', 'tor.*__SocksPort|ssh\\s.*-L'], stdout=sub.PIPE)
        return NetworkTunnelInfo(len(p.stdout.splitlines()))

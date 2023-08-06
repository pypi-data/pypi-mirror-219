# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
from es7s.shared import get_stdout
from ..._base import CliCommand
from ..._base_opts_params import CMDTRAIT_X11, CMDTYPE_BUILTIN
from ..._decorators import _catch_and_log_and_exit, cli_command, cli_option
from .tmux import TmuxBindCollector, TmuxFormatter
from .x11 import X11BindCollector
from ._base import Formatter


class CombinedFormatter(Formatter):
    def print(self):
        self.print_legend()
        tmux_formatter = TmuxFormatter(self._bind_collectors.pop(0))
        tmux_formatter.print_binds()
        tmux_formatter.print_extras()
        get_stdout().echo()
        self.print_binds()


@cli_command(
    name=__file__,
    cls=CliCommand,
    type=CMDTYPE_BUILTIN,
    traits=[CMDTRAIT_X11],
    short_help="all bindings combined",
)
@cli_option(
    "-d",
    "--details",
    is_flag=True,
    default=False,
    help="Include bind commands and other details",
)
@_catch_and_log_and_exit
class invoker:
    """
    a
    """

    def __init__(self, details: bool, **kwargs):
        self.run(details)

    def run(self, details: bool, **kwargs):
        collectors = [
            TmuxBindCollector(details),
            X11BindCollector(details),
        ]
        CombinedFormatter(*collectors).print()

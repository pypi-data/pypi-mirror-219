# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import enum
import io
import shutil
import sys
import typing as t
from abc import ABCMeta, abstractmethod
from collections import OrderedDict
from dataclasses import dataclass
from datetime import datetime
from typing import TypeVar

import psutil
import pytermor as pt
from pytermor import ColorTarget

from es7s.cli._base_opts_params import CMDTRAIT_ADAPTIVE, CMDTRAIT_X11, CMDTYPE_BUILTIN
from es7s.cli._decorators import _catch_and_log_and_exit, _preserve_terminal_state, cli_command
from es7s.cli._terminal_state import TerminalStateController
from es7s.shared import IoProxy, get_stdout
from es7s.shared.io import IoInterceptor, make_interceptor_io



@cli_command(
    __file__,
    type=CMDTYPE_BUILTIN,
    traits=[CMDTRAIT_ADAPTIVE],
    short_help="&process-&(gre)p-&kill(-&serial)",
)
@_catch_and_log_and_exit
class invoker:
    """
    Evolution of es7s/pgrek, which supported only one query at a
    time, without an option to alter it unless restarted. This one
    [...]
    """

    def __init__(self, **kwargs):
        self._automaton = PgreksAutomaton()
        self._run()

    def _run(self):
        self._automaton.run()


class State(enum.Enum):
    NON_INTERACTIVE = enum.auto()
    WAIT_COMMAND = enum.auto()
    INPUT_STRING = enum.auto()
    HELP = enum.auto()


HT = TypeVar("HT", bound=t.Callable[[], None])


@dataclass(frozen=True)
class ABFSAutoCommand:
    callback: HT
    spec_fmt: pt.FT = pt.NOOP_STYLE


class ABFSAutomaton(metaclass=ABCMeta):
    _CMD_KEY_HELP = "h"
    _CMD_KEY_EXIT = "q"
    _INPUT_AREA_ST = pt.Style(bg=pt.cv.GRAY_0, fg=pt.DEFAULT_COLOR)

    def __init__(self, fps: float = 1.0):
        self._stdout_origin = get_stdout()
        self._stdout_interceptor: IoInterceptor = make_interceptor_io()

        self._state = State.WAIT_COMMAND
        self._input_buf = io.StringIO()
        self._triggered_key = None

        self._commands = OrderedDict[str, ABFSAutoCommand]()
        self._commands.update(
            {
                self._CMD_KEY_HELP: ABFSAutoCommand(self._show_help),
                self._CMD_KEY_EXIT: ABFSAutoCommand(self._exit),
            }
        )
        self._commands_key_list: t.Iterable[pt.Fragment] = []

        self._render_interval = 1 / (fps or 1)
        self._prev_render_duration = 0.0

    @_preserve_terminal_state
    def run(self, tstatectl: TerminalStateController):
        tstatectl.hide_cursor()
        tstatectl.enable_alt_screen_buffer()
        tstatectl.disable_input()

        prev_frame_ts = datetime.now().timestamp()

        while True:
            self._prev_render_duration = -prev_frame_ts + (
                prev_frame_ts := datetime.now().timestamp()
            )
            self._stdout_interceptor.reset()
            self._tick()

            self._pre_render()
            self._render()
            self._post_render()

            rendered = self._stdout_interceptor.getvalue()
            self._stdout_origin.echo(rendered, nl=False)

            self._wait_input()

    @abstractmethod
    def _tick(self):
        raise NotImplementedError

    def _pre_render(self) -> t.NoReturn:
        #self._stdout_interceptor.echo(pt.make_reset_cursor())
        self._stdout_interceptor.echo(pt.make_clear_display())
        pass

    @abstractmethod
    def _render(self) -> t.NoReturn:
        raise NotImplementedError

    def _post_render(self) -> t.NoReturn:
        terminal_height = shutil.get_terminal_size().lines
        self._stdout_interceptor.echo(
            pt.term.compose_clear_line_fill_bg(
                self._INPUT_AREA_ST.bg.to_sgr(ColorTarget.BG),
                terminal_height,
            )
        )

        if self._state is State.NON_INTERACTIVE:
            return

        if self._state is State.WAIT_COMMAND:
            prompt = pt.Text().append(
                pt.Fragment("Select an action: (", self._INPUT_AREA_ST),
                *self._format_action_list(),
                pt.Fragment(")> ", self._INPUT_AREA_ST),
            )
            self._stdout_interceptor.echo_rendered(prompt)

    def _format_action_list(self) -> t.Iterable[pt.Fragment]:
        if not self._commands_key_list:
            separator = pt.Fragment("/", self._INPUT_AREA_ST)

            def _build():
                for idx, (key, cmd) in enumerate(self._commands.items()):
                    if idx > 0:
                        yield separator
                    yield pt.Fragment(key, self._INPUT_AREA_ST.merge_overwrite(cmd.spec_fmt))

            self._commands_key_list = [*_build()]
        return self._commands_key_list

    def _wait_input(self):
        import select

        i, _, _ = select.select([sys.stdin], [], [], self._render_interval)
        if not i:
            return
        match self._state:
            case State.WAIT_COMMAND:
                inp = sys.stdin.read(1)[0].lower()
                self._handle_command_keypress(inp)
            case State.INPUT_STRING:
                self._input_buf = sys.stdin.read(-1)
                self._handle_string_input()
            case State.HELP:
                self._print_help()

    def _handle_command_keypress(self, key: str):
        if cmd := self._commands.get(key):
            self._triggered_key = key
            cmd.callback()

    def _handle_string_input(self):
        inp = self._input_buf.getvalue()
        if "\n" in inp:
            self._state = State.WAIT_COMMAND

    def _print_help(self):
        self._stdout_interceptor.echo(
            "HeLP JRLP"
        )

    def _show_help(self):
        self._state = State.HELP

    def _exit(self):
        raise SystemExit


class PgreksAutomaton(ABFSAutomaton):
    def __init__(self):
        self.query = "xbind"

    def _tick(self):
        p: psutil.Process
        for p in psutil.process_iter():
            self._stdout_interceptor.echo(p.name())

    def _render(self) -> t.NoReturn:
        self._stdout_interceptor.echo(str(datetime.now()))

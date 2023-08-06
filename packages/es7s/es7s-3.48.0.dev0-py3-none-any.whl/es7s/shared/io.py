# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2022-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
from __future__ import annotations

import datetime
import io
import re
import sys
import typing as t
from dataclasses import dataclass
from io import StringIO
from threading import Lock

import click
import pytermor as pt
from pytermor import FT, OmniSanitizer, RT, NOOP_STYLE, SgrStringReplacer
from typing.io import TextIO

from es7s.shared.exception import ArgCountError
from es7s.shared.io_debug import IoDebugger

_stdout: IoProxy | None = None
_stderr: IoProxy | None = None


@dataclass
class IoParams:
    color: bool | None = None
    tmux: bool = False


def get_stdout(require: object = True) -> IoProxy | None:
    global _stdout
    if not _stdout:
        if require:
            raise RuntimeError("Stdout proxy is uninitialized")
        return None
    return _stdout


def get_stderr(require=True) -> IoProxy | None:
    global _stderr
    if not _stderr:
        if require:
            raise RuntimeError("Stderr proxy is uninitialized")
        return None
    return _stderr


def init_io(
    io_params: IoParams = IoParams(),
    stdout: t.IO = sys.stdout,
    stderr: t.IO = sys.stderr,
) -> tuple[IoProxy, IoProxy]:
    global _stdout, _stderr
    if _stdout:
        raise RuntimeError("Stdout proxy is already initialized")
    if _stderr:
        raise RuntimeError("Stderr proxy is already initialized")

    _stdout = IoProxy(io_params, stdout)
    _stderr = IoProxy(IoParams(color=io_params.color, tmux=False), stderr)
    pt.RendererManager.set_default(_stdout.renderer)

    from . import get_logger

    get_logger().setup_stderr_proxy(_stderr)

    return _stdout, _stderr


def destroy_io():
    global _stdout, _stderr
    if _stdout:
        _stdout.destroy()
    if _stderr:
        _stderr.destroy()
    _stdout = None
    _stderr = None


def make_dummy_io() -> IoProxy:
    io = StringIO()
    io.name = "dummy_io"
    return IoProxy(IoParams(), io)


def make_interceptor_io(io: StringIO = None) -> IoInterceptor:
    if not io:
        io = StringIO()
    io.name = "interceptor_io"
    actual_io = get_stdout()
    return IoInterceptor(actual_io._io_params, io, actual_io._io)


class IoProxy:
    CSI_EL0 = pt.make_clear_line_after_cursor().assemble()

    PBAR_MODE_ANY_MSG_START = pt.make_set_cursor_column(1).assemble() + CSI_EL0
    PBAR_MODE_ANY_MSG_END = pt.SeqIndex.BG_COLOR_OFF.assemble()

    _progress_bar_mode = False

    _UNITITIALIZED = object()
    _INITIALIZING = object()

    def __init__(self, io_params: IoParams, io: t.IO, actual_io: t.IO = None):
        self._io_params = io_params
        self._color = io_params.color
        self._tmux = io_params.tmux

        self._renderer = self._make_renderer(actual_io or io)
        # pass original output device for correct autodetection

        self._io: t.IO = io
        self._is_stderr = io == sys.stderr
        self._broken = False
        self._click_available = False
        self._debug_io: TextIO|object|None = self._UNITITIALIZED
        self._debug_io_recnum = 0

        if actual_io:
            return  # disable click output proxying

        try:
            import click

            self._click_available = isinstance(click.echo, t.Callable)
        except ImportError:
            pass

    def __repr__(self):
        return pt.get_qname(self)+f'[{self.io}, {self.renderer}]'

    @property
    def io(self) -> t.IO:
        return self._io

    @property
    def renderer(self) -> pt.IRenderer:
        return self._renderer

    @property
    def color(self) -> bool:
        return self._color

    @property
    def tmux(self) -> bool:
        return self._tmux

    @property
    def sgr_allowed(self) -> bool:
        if isinstance(self._renderer, pt.SgrRenderer):
            return self._renderer.is_format_allowed
        return False

    @property
    def is_broken(self) -> bool:
        return self._broken

    def as_dict(self) -> dict:
        return {
            "renderer": self._renderer,
            "color": self._color,
            "tmux": self._tmux,
        }

    def render(self, string: RT | list[RT] = "", fmt: FT = NOOP_STYLE) -> str:
        return pt.render(string, fmt, self._renderer) # no_log=self._is_stderr

    @t.overload
    def echo_rendered(self, inp: str, style: pt.Style, *, nl=True) -> None:
        ...

    @t.overload
    def echo_rendered(self, inp: str | pt.IRenderable, *, nl=True) -> None:
        ...

    def echo_rendered(self, *args, nl=True) -> None:
        if 1 <= len(args) <= 2:
            rendered = self.render(*args[:2])
            self.echo(rendered, nl=nl)
        else:
            raise ArgCountError(len(args), 1, 2)

    def echo_raw(self, string: str | pt.ISequence = "", *, nl=True) -> None:
        """ Remove all SGRs """
        if isinstance(string, pt.ISequence):
            string = ""
        else:
            string = pt.apply_filters(string, pt.EscSeqStringReplacer)
        self.echo(string, nl=nl)

    def echo_direct(self, string: str | pt.ISequence = "", *, nl=True):
        """ Bypass --color restrictions """
        self.echo(string, nl=nl, bypass=True)

    def echo(self, string: str | pt.ISequence = "", *, nl=True, bypass=False) -> None:
        self._debug_echo(string, nl)

        if isinstance(string, pt.ISequence):
            string = string.assemble()
            nl = False

        if IoProxy._progress_bar_mode:
            string = self.PBAR_MODE_ANY_MSG_START + string + self.PBAR_MODE_ANY_MSG_END

        try:
            if isinstance(self._io, OneLineStringIO):  # fucking fuck... @REFINE IoInterceptor was introduced later
                self._io.truncate()

            if self._click_available and not bypass:
                click.echo(string, file=self._io, color=self._color, nl=nl)
            else:
                print(
                    string,
                    file=self._io,
                    end=("\n" if nl else ""),
                    flush=not bool(string),
                )

            if isinstance(self._io, OneLineStringIO):
                self._io.seek(0)

        except BrokenPipeError:
            self._broken = True
            self._pacify_flush_wrapper()

    def echo_progress_bar(self, string: str = ""):
        self.echo(string + self.CSI_EL0, nl=False)

    def enable_progress_bar(self):
        IoProxy._progress_bar_mode = True

    def disable_progress_bar(self):
        self.echo(nl=False)  # clear the bar
        IoProxy._progress_bar_mode = False

    def write(self, s: str) -> None:
        self.echo(s)

    def destroy(self):
        if isinstance(self._debug_io, IoDebugger):
            self._debug_io.destroy()

    def _debug_echo(self, string: str| pt.ISequence, nl: bool):
        if self._debug_io == self._UNITITIALIZED:
            from es7s.shared import get_merged_uconfig
            if not get_merged_uconfig(False):
                return
            if (debug_io := get_merged_uconfig().get_cli_debug_io_mode()):
                # rulers?
                self._debug_io = self._INITIALIZING
                self._debug_io = IoDebugger(self._io)
            else:
                self._debug_io = None

        if isinstance(self._debug_io, IoDebugger):
            self._debug_io.mirror_echo(string, nl)

    def _make_renderer(self, io: t.IO) -> pt.IRenderer:
        if self.tmux:
            if self.color is False:
                return pt.renderer.NoOpRenderer()
            return pt.renderer.TmuxRenderer()
        return pt.SgrRenderer(self._output_mode, io)

    def _pacify_flush_wrapper(self) -> None:
        sys.stdout = t.cast(t.TextIO, click.utils.PacifyFlushWrapper(sys.stdout))
        sys.stderr = t.cast(t.TextIO, click.utils.PacifyFlushWrapper(sys.stderr))

    @property
    def _output_mode(self) -> pt.OutputMode:
        if self.color is None:
            return pt.OutputMode.AUTO
        if self.color:
            return pt.OutputMode.TRUE_COLOR
        return pt.OutputMode.NO_ANSI


class IoInterceptor(IoProxy):
    def __init__(self, io_params: IoParams, io: StringIO, actual_io: t.IO = None):
        self._io: StringIO = io
        super().__init__(io_params, io, actual_io)

    def reset(self) -> None:
        self._io.truncate(0)
        self._io.seek(0)

    def getvalue(self) -> str:
        return self._io.getvalue()


class BrokenPipeEvent(Exception):
    pass


class OneLineStringIO(StringIO):
    pass

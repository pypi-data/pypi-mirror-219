# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import enum
import io
import math
import os.path
import re
import sys
import time
import typing as t
from collections import deque

import click
import pytermor as pt
from pytermor import get_terminal_width

from es7s.cli._base_opts_params import CMDTYPE_BUILTIN, EnumChoice
from es7s.cli._decorators import _preserve_terminal_state, cli_argument, cli_command
from es7s.cli._terminal_state import TerminalStateController
from es7s.shared import FrozenStyle, Styles as BaseStyles, get_logger, get_stderr, get_stdout
from es7s.shared.path import ESQDB_DATA_PIPE


class _Styles(BaseStyles):
    STATUSBAR_LEFT_BG = pt.cv.DARK_RED_2
    STATUSBAR_SEP_BG = pt.cvr.SPACE_CADET
    STATUSBAR_RIGHT_BG = pt.cvr.DARK_MIDNIGHT_BLUE

    STATUSBAR_LEFT_BASE = FrozenStyle(bg=STATUSBAR_LEFT_BG)
    STATUSBAR_SEP_BASE = FrozenStyle(fg=pt.cv.GRAY_0, bg=STATUSBAR_SEP_BG)
    STATUSBAR_RIGHT_BASE = FrozenStyle(fg=pt.cv.GRAY_0, bg=STATUSBAR_RIGHT_BG)

    CUR_PART_FMT = FrozenStyle(STATUSBAR_RIGHT_BASE, fg=pt.cv.HI_BLUE, bold=True)
    TOTAL_PARTS_FMT = FrozenStyle(STATUSBAR_RIGHT_BASE, fg=pt.cv.BLUE)


class Mode(str, enum.Enum):
    SEND = "send"
    RECEIVE = "recv"

    def __str__(self):
        return self.value


@cli_command(
    __file__,
    type=CMDTYPE_BUILTIN,
    short_help="byte stream step-by-step inspector/throttler",
    command_examples=[
        "// with named pipe:",
        "   %s send file1",
        "   %s recv",
        "// with explicitly set file:",
        "   %s send file1 file2",
        "   %s recv file2",
    ],
)
@cli_argument("mode", type=EnumChoice(Mode), required=True)
@cli_argument("infile", type=click.File(mode="rb"), required=False)
@cli_argument("outfile", type=click.File(mode="wb"), required=False)
@_preserve_terminal_state  # @TODO send to stderr?
class invoker:
    """
    ¯Send mode¯

    Open specified INFILE in binary mode and start reading the content to the buffer.
    If omitted or specified as ''-'', the stdin will be used as data input instead.\n\n

    Split the data by ESC control bytes (0x1b) and feed the parts one-by-one to
    OUTFILE, or to a prepared named pipe in a system temporary directory, if no
    OUTFILE is specified.\n\n

    Manual control is available only if stdin of the process is a terminal, otherwise
    the automatic data writing is performed.\n\n

    ¯Recv mode¯

    Open specified INFILE in binary mode, start reading the content and immediately
    write the results to stdout. If INFILE is omitted, read from the same named pipe
    as in send mode instead (the filename is always the same). OUTFILE argument is
    ignored. No stream control is implemented. Terminate on EOF.
    """
    MANUAL_CONTROL_HINT = "Press any key to send next part of the data, or Ctrl+C to exit. "
    AUTO_CONTROL_HINT = "Press Ctrl+C to exit. "

    def __init__(
        self,
        tstatectl: TerminalStateController,
        mode: Mode,
        infile: io.RawIOBase | None,
        outfile: io.IOBase,
        **kwargs,
    ):
        self._mode_manual_control = sys.stdin.isatty()
        self._mode_stats_display = sys.stdout.isatty()

        if self._mode_manual_control:
            tstatectl.hide_cursor()
            tstatectl.disable_input()
        if self._mode_stats_display:
            tstatectl.assign_proxy(get_stderr())
            tstatectl.enable_alt_screen_buffer()

        logger = get_logger()
        self._stream_types = {"out": "F", "in": "F"}

        try:
            if mode is Mode.SEND:
                logger.debug(f"Input is set to {infile}")
                self._run_send(
                    outfile or self._get_default_fifo(read=False),
                    infile or sys.stdin.buffer,
                )
            else:
                self._run_rcv(
                    infile or self._get_default_fifo(read=True),
                )
        finally:
            if infile and not infile.closed:
                infile.close()
            if outfile and not outfile.closed:
                outfile.close()

    def _wrap_buffer(self, stream: io.RawIOBase) -> tuple[t.BinaryIO, int | None]:
        max_offset = None
        buf = stream
        if stream.seekable():
            stream.seek(0, os.SEEK_END)
            max_offset = stream.tell()
            stream.seek(0)
            buf = io.BufferedReader(stream)
        if isinstance(buf, io.TextIOWrapper):
            buf = buf.buffer
        return buf, max_offset

    def _get_default_fifo(self, *, read: bool) -> t.BinaryIO:
        default = ESQDB_DATA_PIPE
        if not os.path.exists(default):
            get_logger().debug(f"Creating FIFO: '{default}'")
            os.mkfifo(default, 0o600)

        get_stderr().echo(f"{'Source' if read else 'Destination'} stream ", nl=False)
        get_stderr().echo(f"is a NAMED PIPE:  '{default}'")
        if read:
            get_stderr().echo("Waiting for the sender to start transmitting.")
            return open(default, "rb")
        get_stderr().echo("Waiting for the receiver to connect.")
        return open(default, "wb")

    def _run_send(self, outfile: io.IOBase = None, infile: io.RawIOBase = None):
        stderr = get_stderr()
        logger = get_logger()
        get_logger().debug(f"SEND mode, {infile} -> {outfile}")

        if self._mode_stats_display:
            stderr.echo(pt.make_clear_display())
            stderr.echo(pt.make_move_cursor_down(9999))
        else:
            stderr.echo(
                "It seems like stderr stream is not connected to a terminal, "
                "so statistics are disabled."
            )
            if self._mode_manual_control:
                stderr.echo(self.MANUAL_CONTROL_HINT)
            else:
                stderr.echo(self.AUTO_CONTROL_HINT)

        buf_offset = 0
        inbuf, max_offset = self._wrap_buffer(infile)
        infilename = getattr(infile, "name", "?")

        ps: deque[bytes] = deque()
        pll: int = 1
        offset: int = 0
        oll: int = 2 * math.ceil(len(f"{max_offset or 0:x}") / 2)

        idx = -1 if self._mode_manual_control else 0

        letters = [
            self._get_fletter("in", infile),
            self._get_fletter("out", outfile),
            " " if self._mode_manual_control else "A",
        ]
        letters_str = " ".join(['', *letters, ''])

        while not inbuf.closed or len(ps):
            if not inbuf.closed and (len(ps) < 3 or buf_offset - offset < 1024):
                psp = inbuf.readline()
                if not len(psp):
                    inbuf.close()
                buf_offset += len(psp)
                pspl = re.split(rb"([\x1b])", psp)
                while len(pspl):
                    p = pspl.pop(0)
                    if not len(ps) or re.search(rb"[^\x1b]", ps[-1]):
                        ps.append(p)
                    else:
                        ps[-1] += p
                pll = max(pll, len(str(len(ps))))

            if self._mode_stats_display:
                stderr.echo(pt.make_set_cursor_column(1), nl=False)
                stderr.echo(pt.SeqIndex.RESET, nl=False)
                stderr.echo(pt.make_clear_line_after_cursor(), nl=False)

            if len(ps) and idx > 0:
                p = ps.popleft()
                offset += outfile.write(p)
                outfile.flush()
                stderr.echo(self._decode(p))

            if self._mode_stats_display:
                twidth: int = get_terminal_width(pad=0)
                stderr.echo(pt.make_move_cursor_down_to_start(1), nl=False)

                left_st = _Styles.STATUSBAR_SEP_BG if idx < 0 else _Styles.STATUSBAR_LEFT_BG
                stderr.echo(left_st.to_sgr(pt.ColorTarget.BG), nl=False)
                stderr.echo(pt.make_clear_line_after_cursor(), nl=False)
                if self._mode_manual_control and idx == -1:
                    stderr.echo_rendered(self.MANUAL_CONTROL_HINT, FrozenStyle(bg=left_st), nl=False)
                    stderr.echo(pt.make_set_cursor_column(), nl=False)

                else:
                    examplestr = self._decode(ps[0] if len(ps) else b"")

                    status_right_flex = ""
                    if max_fname_len := self._get_max_fname_len(twidth):
                        status_right_flex += (
                            pt.Fragment(" ", _Styles.STATUSBAR_RIGHT_BASE)
                            + pt.Fragment(pt.cut(infilename, max_fname_len, ">"), _Styles.TOTAL_PARTS_FMT)
                            + pt.Fragment(" ", _Styles.STATUSBAR_RIGHT_BASE)
                            + pt.Fragment("→", _Styles.CUR_PART_FMT)
                            + pt.Fragment(" ", _Styles.STATUSBAR_RIGHT_BASE)
                            + pt.Fragment(pt.cut(getattr(outfile, "name", "-"), max_fname_len, ">"), _Styles.TOTAL_PARTS_FMT)
                        )

                    status_right_flex += (
                        pt.Fragment(" ", _Styles.STATUSBAR_RIGHT_BASE)
                        + pt.Fragment(" ", _Styles.STATUSBAR_SEP_BASE)
                        + pt.Fragment(letters_str, _Styles.TOTAL_PARTS_FMT)
                    )
                    status_right_fixed = (
                        pt.Fragment(" ", _Styles.STATUSBAR_SEP_BASE)
                        + pt.Fragment(" ", _Styles.STATUSBAR_RIGHT_BASE)
                        + pt.Fragment(str(idx).rjust(pll), _Styles.CUR_PART_FMT)
                        + pt.Fragment("+" + str(len(ps)).rjust(pll), _Styles.TOTAL_PARTS_FMT)
                        + pt.Fragment(" ", _Styles.STATUSBAR_RIGHT_BASE)
                        + pt.Fragment(" ", _Styles.STATUSBAR_SEP_BASE)
                        + pt.Fragment(" ", _Styles.STATUSBAR_RIGHT_BASE)
                        + pt.Fragment(f"{offset:{oll}d}", _Styles.CUR_PART_FMT)
                        + pt.Fragment(f"/{max_offset:{oll}d}" if max_offset else "", _Styles.TOTAL_PARTS_FMT)
                    )

                    status_right_flex_start: int = twidth
                    if twidth < len(status_right_fixed):
                        examplestr = ""
                        status_right_flex = ""
                        status_right_fixed.set_width(min(twidth, len(status_right_fixed)))
                    elif (free := twidth - len(status_right_fixed)) < len(status_right_flex):
                        examplestr = ""
                        status_right_flex.set_width(min(free, len(status_right_fixed)))
                        status_right_flex_start = free
                    else:
                        free = twidth - len(status_right_flex) - len(status_right_fixed)
                        examplestr = pt.cut(examplestr, free - 1)
                        status_right_flex_start = free

                    stderr.echo_rendered(examplestr, FrozenStyle(bg=left_st), nl=False)
                    stderr.echo(pt.make_set_cursor_column(status_right_flex_start), nl=False)
                    stderr.echo(_Styles.STATUSBAR_RIGHT_BG.to_sgr(pt.ColorTarget.BG), nl=False)
                    stderr.echo(pt.make_clear_line_after_cursor(), nl=False)
                    stderr.echo_rendered(status_right_flex, nl=False)
                    stderr.echo_rendered(status_right_fixed, nl=False)
                    stderr.echo(pt.make_set_cursor_column(), nl=False)

            self._wait(infile)

            logger.debug(f"State: (idx={idx}, offset={offset}/{max_offset})")
            if max_offset and offset == max_offset:
                if not self._mode_manual_control:
                    break
                stderr.echo_rendered("Done. Press any key to exit", FrozenStyle(bg=_Styles.STATUSBAR_SEP_BG), nl=False)
                stderr.echo(_Styles.STATUSBAR_SEP_BG.to_sgr(pt.ColorTarget.BG), nl=False)
                stderr.echo(pt.make_clear_line_after_cursor(), nl=False)
                self._wait(infile)
                break

            idx += 1

    def _run_rcv(self, infile: io.RawIOBase = None):
        get_logger().debug(f"RCV mode, {infile} -> stdout")
        if not infile:
            infile = self._get_default_fifo(read=True)
        inbuf, max_offset = self._wrap_buffer(infile)
        if self._mode_stats_display:
            get_stdout().echo(pt.make_clear_display(), nl=False)
            get_stdout().echo(pt.make_reset_cursor(), nl=False)

        while i := inbuf.readline(1):
            get_stdout().io.buffer.write(i)
            get_stdout().io.flush()

    def _decode(self, b: bytes) -> str:
        return re.sub(
            r"(\x1b)|(\n+)",
            lambda m: (len(m[1] or "") * "ǝ") + (len(m[2] or "") * "↵"),
            b.decode(errors="replace_with_qmark"),
        )

    def _wait(self, infile: io.IOBase):
        if self._mode_manual_control:
            pt.wait_key()
        else:
            time.sleep(0.4)

    def _get_fletter(self, stype_key: str, file: io.IOBase) -> str:
        if file.isatty():
            return "T"
        elif getattr(file, "seekable", lambda: False)():
            return self._stream_types[stype_key]
        return "P"

    def _get_max_fname_len(self, twidth: int) -> int|None:
        if twidth < 60:
            return None
        return 10 + max(0, min((twidth - 80)//5, 20))

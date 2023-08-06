# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2021-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
from __future__ import annotations

from functools import cached_property
import io
import logging
import os
import pathlib
import re
import sys
import threading
import typing as t
from contextlib import contextmanager
from dataclasses import dataclass, field
from logging import (
    CRITICAL,
    DEBUG,
    ERROR,
    Formatter,
    INFO,
    LogRecord as BaseLogRecord,
    Logger as BaseLogger,
    StreamHandler,
    WARNING,
    handlers,
)
from os import devnull
from typing import Any

import click
import pytermor as pt

from .io import get_stderr
from .styles import Styles
from .. import APP_DAEMON_DEBUG, APP_NAME, APP_VERSION

TRACE = 5
NONE = 100
logging.addLevelName(TRACE, "TRACE")
logging.addLevelName(NONE, "NONE")

VERBOSITY_TO_LOG_LEVEL_MAP = {
    #  stderr syslog
    0: [WARNING, INFO],
    1: [INFO, DEBUG],
    2: [DEBUG, TRACE],
    3: [TRACE, TRACE],
}


@dataclass
class LoggerParams:
    """ Initializing DTO """
    verbosity: int = 0
    quiet: bool = False
    out_stderr: bool = True
    out_syslog: bool = True
    out_file: str | None = None

    # @property
    # def trace(self) -> bool:
    #     return self.verbosity >= 2


@dataclass(frozen=True)
class LoggerSettings:
    """ Runtime DTO """

    _verbosity: int
    _quiet: bool
    _stderr_level: int
    _syslog_level: int

    @cached_property
    def print_usage_errors(self) -> bool: return not self._quiet
    @cached_property
    def print_click_errors(self) -> bool: return not self._quiet
    @cached_property
    def print_exception_stack_traces(self) -> bool: return self._verbosity > 0
    @cached_property
    def print_non_fatal_exceptions(self) -> bool: return self._verbosity > 0
    @cached_property
    def print_non_fatal_exception_stack_traces(self) -> bool: return self._verbosity > 1
    @cached_property
    def display_monitor_debugging_markup(self) -> bool: return self._verbosity > 0
    @cached_property
    def progress_bar_mode_allowed(self) -> bool: return True  # not(0 < self._verbosity < 3)
    @cached_property
    def print_subprocess_stderr_data(self) -> bool: return self._verbosity > 0
    @cached_property
    def log_subprocess_arg_nonprints(self) -> bool: return self._verbosity > 2

    @cached_property
    def stderr_allowed_any(self) -> bool: return self._stderr_level < NONE
    @cached_property
    def stderr_allowed_debug(self) -> bool: return self._stderr_level <= DEBUG
    @cached_property
    def stderr_allowed_trace(self) -> bool: return self._stderr_level <= TRACE


def get_logger(require=True) -> Logger | DummyLogger:
    if logger := Logger.get_instance(require):
        return logger
    return DummyLogger()


def init_logger(app_name="es7s", ident_part="core", params=LoggerParams()) -> Logger:
    return Logger(app_name, ident_part, params)


def destroy_logger():
    Logger.destroy()


class Writeable:
    def write(self, s: str) -> None:
        ...


class DummyLogger:
    quiet = False

    def __getattribute__(self, name: str) -> Any:
        return lambda msg="", *_, **__: print(f"{name.upper()}: {msg!s}")


class Logger(BaseLogger):
    _logger: Logger | None = None
    _setup: LoggerSettings | None = None

    @classmethod
    def get_instance(cls, require: bool) -> Logger | DummyLogger | None:
        if not cls._logger:
            if require:
                raise RuntimeError("Logger is uninitialized")
            return None
        return cls._logger

    @classmethod
    def destroy(cls):
        cls._logger = None

    @property
    def setup(self) -> LoggerSettings:
        return self._setup


    HTTP_RESPONSE_FILTERS = [
        pt.StringLinearizer(),
    ]
    TRACE_EXTRA_FILTERS: t.List[pt.IFilter] = [
        pt.SgrStringReplacer(),
        pt.StringMapper({ord("\n"): " "}),
        pt.OmniSanitizer(),
    ]

    def __init__(self, app_name: str, ident_part: str, params: LoggerParams):
        """
        :param app_name:
        :param ident_part:
        :param params:
        """
        super().__init__(app_name)
        Logger._logger = self
        self._pt_logger = logging.getLogger("pytermor")

        stderr_level, syslog_level = VERBOSITY_TO_LOG_LEVEL_MAP[
            min(len(VERBOSITY_TO_LOG_LEVEL_MAP) - 1, params.verbosity)
        ]
        if params.quiet:
            stderr_level, syslog_level = NONE, NONE

        file_level = syslog_level
        min_level = min(stderr_level, stderr_level)
        self.setLevel(min_level)
        self._pt_logger.setLevel(min_level)

        self._setup = LoggerSettings(params.verbosity, params.quiet, stderr_level, syslog_level)
        self._log_audit_events = True

        self._stderr_handler = None
        self._sys_log_handler = None
        self._file_handler = None
        if params.out_stderr:
            self._stderr_formatter = _StderrFormatter(params, self.setup)
            self._stderr_handler = _StderrHandler(stream=sys.stderr)
            self._stderr_handler.setLevel(stderr_level)
            self._stderr_handler.setFormatter(self._stderr_formatter)
            self.addHandler(self._stderr_handler)
            self._pt_logger.addHandler(self._stderr_handler)

        if params.out_syslog:
            sys_log_handler = _SysLogHandler(ident=f"{app_name}/{ident_part}")
            try:
                sys_log_handler.ensure_available()
            except (FileNotFoundError, RuntimeError):
                pass
            else:
                self._sys_log_handler = sys_log_handler
                self._sys_log_handler.setLevel(syslog_level)
                self._sys_log_handler.setFormatter(_SyslogFormatter())
                self.addHandler(self._sys_log_handler)
                self._pt_logger.addHandler(self._sys_log_handler)

        if params.out_file:
            self._file_handler = _FileHandler(params.out_file, "a")
            self._file_handler.setLevel(file_level)
            self._file_handler.setFormatter(_FileFormatter())
            self.addHandler(self._file_handler)
            self._pt_logger.addHandler(self._file_handler)

        self.log_init_info()

    def setup_stderr_proxy(self, io_proxy: Writeable):
        if self._stderr_handler:
            self._stderr_handler.setup_proxy(io_proxy)

    def exception(self, msg: object, **kwargs):
        msg = f"{msg.__class__.__qualname__}: {msg!s}"
        super().exception(msg, **kwargs)

    def non_fatal_exception(self, msg: object, **kwargs):
        msg = f"{msg} [non-fatal]"
        if self.setup.print_non_fatal_exceptions:
            exc_info=self.setup.print_non_fatal_exception_stack_traces
            self.exception(msg, exc_info=exc_info, **kwargs)
        else:
            self.debug(msg, exc_info=True, **kwargs)

    def log_http_request(self, req_id: int | str, url: str, method: str = "GET"):
        self.info(f"[#{req_id}] > {method} {url}")

    def log_http_response(self, req_id: int | str, response: "requests.Response", with_body: bool):
        msg_resp = f"[#{req_id}] < HTTP {response.status_code}"
        msg_resp += ", " + pt.format_si(response.elapsed.total_seconds(), "s")
        msg_resp += ", " + pt.format_si_binary(len(response.text))
        if with_body:
            msg_resp += ': "'
            msg_resp += pt.apply_filters(response.text, *self.HTTP_RESPONSE_FILTERS)
            msg_resp += '"'
        self.info(msg_resp)

    def log_audit_event(self, ev: str, *args):
        if not self._log_audit_events:
            return
        self.log(TRACE, f"(AEV) {ev}: {format_attrs(*args)}", extra={"aev_triggered": True})

    def log_init_info(self):
        appver = f"{APP_NAME} {os.getenv('ES7S_DOMAIN')} v{APP_VERSION} "
        appver += "[debug]" if APP_DAEMON_DEBUG else ""
        self.info(appver)
        self.info(
            format_attrs(
                {
                    "PID": os.getpid(),
                    "PPID": os.getppid(),
                    "UID": os.getuid(),
                    "CWD": os.getcwd(),
                }
            )
        )
        self.info("Logging system initialized")

    def log_init_params(self, *params_desc: tuple[str, object]):
        for (label, params) in params_desc:
            params_str = format_attrs(params, keep_classname=False) if params else ""
            self.debug(label.ljust(20) + params_str)

    def trace(
        self,
        data: str | bytes,
        label: str = None,
        out_plain: bool = True,
        out_sanitized: bool = False,
        out_ucp: bool = False,
        out_utf8: bool = False,
        out_hex: bool = False,
        addr_shift: int = None,
    ):
        if not data or not self.isEnabledFor(TRACE):
            return
        label = f"{label.upper()} " if label else ""
        dump = []

        if not isinstance(data, (str, bytes)):
            data = str(data)

        if isinstance(data, str):
            if out_plain:
                dump += [data]
            if out_sanitized:
                dump += [pt.apply_filters(data, *self.TRACE_EXTRA_FILTERS)]
            if out_ucp:
                dump += [pt.dump(data)]
            if out_utf8:
                dump += [pt.StringTracer().apply(data)]
        else:
            if out_hex:
                dump += [pt.BytesTracer().apply(data)]

        if len(dump) == 0:
            return

        if len(dump) > 1 or "\n" in dump[0]:
            dump.insert(0, label + "::")
        else:
            dump[0] = label + ": " + dump[0]

        self.log(TRACE, "\n".join(dump))

    def makeRecord(
        self,
        name: str,
        level: int,
        fn: str,
        lno: int,
        msg: object,
        args: t.Any,
        exc_info: t.Any,
        func: str | None = ...,
        extra: t.Mapping[str, object] | None = ...,
        sinfo: str | None = ...,
    ) -> LogRecord:
        if not isinstance(extra, dict):
            extra = {}
        rv = LogRecord(name, level, fn, lno, msg, args, exc_info, func, sinfo, **extra)
        return rv

    @contextmanager
    def ignore_audit_events(self) -> None:
        self._log_audit_events = False
        self.debug("Disabled audit events logging")
        yield
        self._log_audit_events = True
        self.debug("Enabled audit events logging")


class LogRecord(BaseLogRecord):
    def __init__(
        self,
        name: str,
        level: int,
        pathname: str,
        lineno: int,
        msg: object,
        args: t.Any,
        exc_info: t.Any,
        func: str | None = ...,
        sinfo: str | None = ...,
        pid=None,
        stream=None,
        aev_triggered=False,
    ) -> None:
        super().__init__(name, level, pathname, lineno, msg, args, exc_info, func, sinfo)
        domain = os.getenv("ES7S_DOMAIN")

        source_1 = domain.upper() if domain else (self.name + "." + self.module)
        self.source = "[" + source_1 + "]"
        if source_2 := self._get_command_name():
            self.source += "[" + re.sub(r"[^a-zA-Z0-9.:-]+", "", source_2[:24]) + "]"

        self.pid = pid
        self.stream = stream

        self.sep_stream = ""
        if self.stream:
            if self.pid:
                self.sep_stream = f"[{self.pid} {self.stream.upper()}]"
            else:
                self.sep_stream = f"[{self.stream.upper()}]"

        self.rel_created_str = '(+'+pt.format_time_delta(self.relativeCreated / 1000, 6)+')'
        self.aev_triggered = aev_triggered

    def _get_command_name(self) -> str | None:
        name = None
        if ctx := click.get_current_context(silent=True):
            name = ctx.command.name
        if thread := threading.current_thread():
            if not name or thread != threading.current_thread():
                name = thread.name
        return name



class _StderrHandler(StreamHandler):
    def __init__(self, stream):
        super().__init__(stream)
        self._io_proxy: Writeable | None = None

    def setup_proxy(self, io_proxy: Writeable):
        self._io_proxy = io_proxy

    def handle(self, record: LogRecord):
        if not hasattr(record, "source"):
            setattr(record, "source", '')
        if not hasattr(record, "sep_stream"):
            setattr(record, "sep_stream", f'[pytermor.{record.module}]')
        if not hasattr(record, "rel_created_str"):
            setattr(record, "rel_created_str", '')
        super().handle(record)
        # reset cached exc_text after _Es7sStderrFormatter
        # so that syslog won't receive SGRs
        record.exc_text = None

    def emit(self, record: LogRecord) -> None:
        if not self._io_proxy:  # uninitialized
            super().emit(record)
            return
        try:
            msg = self.format(record)
            self._io_proxy.write(msg)
        except RecursionError:  # See issue 36272
            raise
        except Exception:
            self.handleError(record)

    def __repr__(self):
        return f"{pt.get_qname(self)}[{logging.getLevelName(self.level)}]"


class _FileHandler(logging.FileHandler):
    def __repr__(self):
        return f"{pt.get_qname(self)}[{logging.getLevelName(self.level)}]"


class _SysLogHandler(handlers.SysLogHandler):
    level_overrides = {
        "TRACE": "DEBUG",
    }

    def __init__(
        self,
        ident: str,
        address: str = "/dev/log",
        facility: int = handlers.SysLogHandler.LOG_LOCAL7,
        **kwargs,
    ):
        super().__init__(address=address, facility=facility, **kwargs)
        self.ident = f"{ident}[{os.getpid()}]: "

    def ensure_available(self):
        if not os.path.exists(self.address):
            raise FileNotFoundError(self.address)
        if not pathlib.Path(self.address).is_socket():
            raise RuntimeError(f"Syslog receiver is found, but is not a socket: {self.address}")

    def mapPriority(self, levelName):
        levelName = self.level_overrides.get(levelName, levelName)
        return super().mapPriority(levelName)

    def __repr__(self):
        return f"{pt.get_qname(self)}[{logging.getLevelName(self.level)}]"


class _SyslogFormatter(Formatter):
    def __init__(self, **kwargs) -> None:
        super().__init__(
            fmt=f"%(source)s%(sep_stream)s%(rel_created_str)s %(message)s", **kwargs
        )


class _FileFormatter(Formatter):
    def __init__(self, **kwargs) -> None:
        super().__init__(
            fmt=f"[%(asctime)s]%(source)s%(sep_stream)s%(rel_created_str)s %(message)s", **kwargs
        )


class _StderrFormatter(Formatter):
    COLOR_DEFAULT = pt.NOOP_COLOR
    COLOR_EXCEPTION = Styles.ERROR.fg
    COLOR_AUDIT_EVENT = Styles.STDERR_AEVNT.fg

    LEVEL_TO_COLOR_MAP = {
        CRITICAL: Styles.CRITICAL.fg,
        ERROR: Styles.ERROR_ACCENT.fg,
        WARNING: Styles.WARNING.fg,
        INFO: Styles.TEXT_DEFAULT.fg,
        DEBUG: Styles.STDERR_DEBUG.fg,
        TRACE: Styles.STDERR_TRACE.fg,
    }

    FORMAT_DEFAULT = "%(levelname)s: %(message)s"
    FORMAT_VERBOSE = "[%(levelname)-5.5s]%(source)s%(sep_stream)s%(rel_created_str)s %(message)s"

    def __init__(self, params: LoggerParams, setup: LoggerSettings, **kwargs):
        fmt = self.FORMAT_DEFAULT
        if params.verbosity > 0:
            fmt = self.FORMAT_VERBOSE
        super().__init__(fmt=fmt, **kwargs)

        self._show_exc_info = setup.print_exception_stack_traces

    def formatMessage(self, record: LogRecord) -> str:
        formatted_msg = super().formatMessage(record)
        color = self._resolve_color(record)
        return self._render_or_raw(formatted_msg, color)

    def formatException(self, ei):
        if not self._show_exc_info:
            return None
        formatted = super().formatException(ei)
        result = "\n".join(
            self._render_or_raw(line, self.COLOR_EXCEPTION)
            for line in formatted.splitlines(keepends=False)
        )
        return result

    def _render_or_raw(self, msg, color: pt.IColor):
        if stderr := get_stderr(False):
            return color.to_sgr().assemble() + msg + pt.SeqIndex.RESET.assemble()
        return msg

    def _resolve_color(self, record: LogRecord) -> pt.IColor:
        if isinstance(record, LogRecord) and record.aev_triggered:
            return self.COLOR_AUDIT_EVENT
        return self.LEVEL_TO_COLOR_MAP.get(record.levelno, self.COLOR_DEFAULT)


def format_attrs(*o: object, keep_classname=True, level=0, flat=False) -> str:
    def _to_str(a) -> str:
        if (s := str(a)).startswith(cn := a.__class__.__name__):
            if keep_classname:
                return s
            return s.removeprefix(cn)
        return f"'{s}'" if s.count(" ") else s

    def _wrap(s):
        if flat:
            return s
        return f"({s})"

    if len(o) == 1:
        o = o[0]
    if isinstance(o, str):
        return o
    elif isinstance(o, t.Mapping):
        return _wrap(" ".join(f"{_to_str(k)}={format_attrs(v, flat=flat)}" for k, v in o.items()))
    elif issubclass(type(o), (io.IOBase, click.utils.LazyFile)):
        return f"{pt.get_qname(o)}['{getattr(o, 'name', '?')}', {getattr(o, 'mode', '?')}]"
    elif isinstance(o, t.Iterable):
        return _wrap(" ".join(format_attrs(v, level=level + 1, flat=flat) for v in o))
    return _to_str(o)


# resulting syslog output (partial):

# _TRANSPORT=syslog             # logs filtering:
# PRIORITY=7                    #
# SYSLOG_FACILITY=23            #    "journalctl --facility=local7" (all es7s logs are sent to this facility)
# _UID=1001                     # or "journalctl --ident=es7s/corectl" (that's "syslog_ident" argument)
# _GID=1001                     # or "journalctl --grep MONITOR:docker" (filter by group or/and command)
# _EXE=/usr/bin/python3.10
# _CMDLINE=/home/a.shavykin/.local/pipx/venvs/es7s/bin/python /home/a.shavykin/.local/bin/es7s corectl install
# _COMM=es7s
# SYSLOG_PID=846461
# SYSLOG_IDENTIFIER=es7s/corectl
# MESSAGE=[MONITOR:docker] Initialized with (verbose=0 quiet=False c=False color=None) [log.py:92]

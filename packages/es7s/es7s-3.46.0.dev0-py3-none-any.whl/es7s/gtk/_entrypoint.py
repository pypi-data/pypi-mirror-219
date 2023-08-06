# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2022-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import os
import pydoc
import signal
import sys
import typing

from es7s.shared import (
    IoParams,
    LoggerParams,
    get_stderr,
    get_stdout,
    init_config,
    init_io,
    init_logger,
)
from es7s.shared.uconfig import UserConfigParams, get_merged as get_merged_uconfig
from es7s.shared.threads import exit_gracefully
from . import Gtk
from ._base import _BaseIndicator
from .indicator_manager import IndicatorManager
from .indicator_systemctl import IndicatorSystemCtl
from .. import APP_VERBOSITY


def invoke():
    os.environ.update({"ES7S_DOMAIN": "GTK"})
    _init()
    try:
        ic = IndicatorController()
        ic.run()
    except SystemExit:
        if stdout := get_stdout(False):
            stdout.echo()
        raise


def _init():
    logger_params = LoggerParams(verbosity=APP_VERBOSITY)
    io_params = IoParams()

    logger = init_logger(params=logger_params)
    _, _ = init_io(io_params)
    init_config(UserConfigParams())

    logger.log_init_params(
        ("Log configuration:", logger_params),
        ("Logger setup:", {"handlers": logger.handlers}),
        ("IO configuration:", io_params),
        ("Stdout proxy setup:", get_stdout().as_dict()),
        ("Stderr proxy setup:", get_stderr().as_dict()),
    )


class IndicatorController:
    def __init__(self):
        # signal.signal(signal.SIGINT, signal.SIG_DFL)
        signal.signal(signal.SIGINT, self._exit)
        signal.signal(signal.SIGUSR1, self._exit)
        signal.signal(signal.SIGTERM, self._exit)

        self._indicators: list[_BaseIndicator] = []
        self._indicator_mgr: IndicatorManager | None = None

    def run(self):
        self._init_threads()
        Gtk.main()
        for indicator in self._indicators:
            indicator.join()

    def _init_threads(self):
        fact = IndicatorFactory()
        self._indicators = [
            *fact.make_from_config(),
            *fact.make_fixed(),
        ]
        self._indicator_mgr = IndicatorManager(indicators=self._indicators)
        self._indicators.insert(0, self._indicator_mgr)

    def _exit(self, signal_code: int, *args):
        exit_gracefully(signal_code, callback=None)
        Gtk.main_quit()
        sys.exit(signal_code)


class IndicatorFactory:
    def make_fixed(self) -> typing.Iterable[_BaseIndicator]:
        yield IndicatorSystemCtl()

    def make_from_config(self) -> typing.Iterable[_BaseIndicator]:
        config = get_merged_uconfig()
        layout_cfg = filter(None, config.get("indicator", "layout").strip().split("\n"))

        for el in reversed([*layout_cfg]):
            module_name, origin_name = el.rsplit(".", 1)
            if (module := pydoc.safeimport(module_name)) is None:
                continue

            origin: type = getattr(module, origin_name)
            #from .indicator_timestamp import IndicatorTimestamp
            #if origin == IndicatorTimestamp:
            yield origin()

# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------

from __future__ import annotations

import os.path
import re

from pytermor import NOOP_STYLE

from ..._base_opts_params import CMDTRAIT_X11, CMDTYPE_BUILTIN
from ..._decorators import cli_option
from es7s.shared import USER_XBINDKEYS_RC_FILE
from ._base import (
    BindCommand,
    BindKeyTable,
    IBindCollector,
    Formatter,
    Style,
    StyleRegistry,
)
from ..._base import CliCommand
from ..._decorators import _catch_and_log_and_exit, cli_command


class X11BindCommand(BindCommand):
    def get_command_part_style(self, co: str, idx) -> Style:
        if idx == 0:
            return StyleRegistry.COMMAND_PROG_STYLE
        return super().get_command_part_style(co, idx)

    def get_raw_seq_part_style(self, rc: str, idx: int) -> Style:
        if not rc:
            return NOOP_STYLE
        if rc.strip() in ('+', ":"):
            #if rc.startswith("0x"):
                #raise MultipartInputError(split_idx=1)
            return StyleRegistry.RAW_SEQ_STYLE
        return super().get_raw_seq_part_style(rc, idx)


class X11BindCollector(IBindCollector):
    """
    Set of bindings grouped by key table.
    """

    def __init__(self, details: bool) -> None:
        super().__init__({}, details)
        self.collect()

    def _get_raw_binds(self) -> str:
        if os.path.isfile(USER_XBINDKEYS_RC_FILE):
            with open(USER_XBINDKEYS_RC_FILE) as f:
                return f.read()
        raise RuntimeError(f"Failed to read config: '{USER_XBINDKEYS_RC_FILE}'")

    def collect(self):
        xbk_data = self._get_raw_binds()
        key_table = BindKeyTable("xbindkeys", label="SUPPLEMENTARY GLOBALS")
        self._key_tables = {key_table.name: key_table}
        self._parse_table(xbk_data, key_table)

        key_table.sort()
        key_table.update_attrs_col_width()

    def _parse_table(self, table_data: str, key_table: BindKeyTable):
        #  (L#)_(start)______________(example)___________________.
        #  |1| '# @x11' |# @x11  W-x    [xbindkeys] Launch xterm'|
        #  |2| '"'      |"xbindkeys_show"                        |
        #  |3| ' '      |   Mod4 + slash                         |
        #  +-+----------+----------------------------------------+
        for record in table_data.split("@x11"):
            split = record.splitlines()
            if len(split) < 3:
                continue
            if not split[1].startswith('"') or not re.match(r"\s", split[2]):
                continue
            bind = self._bind_factory.from_tmux(split.pop(0).strip(), key_table)

            command_raw = re.sub(r'"|^\s+|\s+$', "", split.pop(0))
            seq_raw = split.pop(0).strip()
            bind.command = X11BindCommand(command_raw, False, seq_raw)

            self._add_bind(key_table, bind)


@cli_command(
    name=__file__,
    cls=CliCommand,
    type=CMDTYPE_BUILTIN,
    traits=[CMDTRAIT_X11],
    short_help="current X11/desktop bindings",
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
        collector = X11BindCollector(details)
        Formatter(collector).print()

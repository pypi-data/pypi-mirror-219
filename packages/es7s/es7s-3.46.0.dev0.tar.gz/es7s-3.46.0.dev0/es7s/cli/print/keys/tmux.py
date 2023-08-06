# ------------------------------------------------------------------------------
#  es7s/core (G2)
#  (c) 2021-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
from __future__ import annotations

import re
from subprocess import CalledProcessError, CompletedProcess, SubprocessError
from typing import List

from pytermor import Style, flatten

from es7s.cli._base_opts_params import CMDTRAIT_ADAPTIVE, CMDTYPE_BUILTIN
from es7s.cli._decorators import cli_option
from es7s.shared import FrozenStyle, get_logger, run_subprocess
from es7s.shared.path import TMUX_PATH
from es7s.shared.typext import only
from ._base import (
    BindCommand,
    BindKeyTable,
    IBindCollector,
    Key,
    KeyCombo,
    ModifierRegistry,
    PopupFormatter,
    Sequence,
    StyleRegistry,
)
from ..._base import CliCommand
from ..._decorators import _catch_and_log_and_exit, cli_command


class TmuxStyleRegistry(StyleRegistry):
    CURLY_BRACE_LEVELS = [
        FrozenStyle(fg="air-superiority-blue"),
        FrozenStyle(fg="steel-blue-3"),
        FrozenStyle(fg="sky-blue-2"),
        FrozenStyle(fg="light-sky-blue-3"),
        FrozenStyle(fg="superuser"),
    ]
    # QUOTE_LEVELS = [65, 66, 108, 109, 150, 114, 116, 193, 157]
    # EXPERIMENTAL_LEVELS = [
    #     203, 215, 87, 227, 75, 155, 99, 171, 85, 205, 81, 209, 63, 135, 221, 207
    # ]

    @classmethod
    def get_curly_brace_level(cls, level: int) -> Style:
        return cls.CURLY_BRACE_LEVELS[level % (len(cls.CURLY_BRACE_LEVELS) - 1)]

    # @classmethod
    # def get_quote_level(cls, level: int) -> Style:
    #     return FrozenStyle(fg=Color256.get_by_code(cls.QUOTE_LEVELS[level % (len(cls.QUOTE_LEVELS)-1)]))


class TmuxBindCommand(BindCommand):
    command_prog_list = []
    curly_brace_levels = []
    curly_brace_shift = 0

    def get_command_part_style(self, co: str, idx) -> Style:
        if co in self.command_prog_list:
            return TmuxStyleRegistry.COMMAND_PROG_STYLE
        elif co in ("|", "|&", "&", "&&", "||"):
            return TmuxStyleRegistry.RAW_SEQ_STYLE
        elif co == "{":
            lvl = self.curly_brace_shift
            self.curly_brace_levels.append(lvl)
            self.curly_brace_shift += 1
            return TmuxStyleRegistry.get_curly_brace_level(lvl)
        elif co == "}":
            lvl = self.curly_brace_levels.pop()
            return TmuxStyleRegistry.get_curly_brace_level(lvl)
        return super().get_command_part_style(co, idx)


class TmuxBindCollector(IBindCollector):
    """
    Set of bindings grouped by key table.
    """

    INVOKER_PRIMARY = "a"
    INVOKER_COMPAT = "b"

    INVOKER_MAP = {
        "root": None,
        "prefix": KeyCombo(Key(INVOKER_PRIMARY), [ModifierRegistry.MODIFIER_CTRL], True),
        "compat": KeyCombo(Key(INVOKER_COMPAT), [ModifierRegistry.MODIFIER_CTRL], True),
        "copy-mode": None,
    }

    def __init__(self, details: bool):
        super().__init__(self.INVOKER_MAP, details)
        self._details = details

    def collect(self, tmux_data: List[str]):
        self._key_tables = {}

        for td in tmux_data:
            tmux_data = [s.strip() for s in td.splitlines()]
            self._parse_table(tmux_data)

            if self._details:
                cp = run_subprocess(TMUX_PATH, "list-commands", check=False)
                if cp.returncode == 0:
                    for s in cp.stdout.splitlines():
                        if (st := s.strip()) and (sp := st.split(" ")):
                            TmuxBindCommand.command_prog_list.append(sp.pop(0))

    def _parse_table(self, table_data: List[str]):
        key_table_name = table_data.pop(0)
        if key_table_name not in self.get_key_table_names():
            raise KeyError(f'Unknown key table "{key_table_name}"')
        key_table = BindKeyTable(key_table_name, self.INVOKER_MAP.get(key_table_name))
        self._key_tables[key_table_name] = key_table

        commands, raw_binds = dict(), []
        for s in table_data:
            if not s.startswith("bind-key"):
                raw_binds.append(s)
            else:
                try:
                    cmd, seq = self.parse_table_command(s, key_table)
                except RuntimeError as e:
                    get_logger().warning(str(e))
                    continue
                commands[seq] = cmd
                # we cannot get BOTH binds' descriptions and commands at the
                # same time, only as two separate lists. that's why we store
                # commands in a map indexed by sequence - to easily find the
                # corresponding one for each bind.

        for raw_bind in raw_binds:
            bind = self._bind_factory.from_tmux(raw_bind, key_table)
            try:
                bind.command = commands.pop(bind.sequence)
            except KeyError as e:
                get_logger().warning(f"Failed to get details for {bind}: {e}")
            self._add_bind(key_table, bind)

        key_table.sort()
        key_table.update_attrs_col_width()

    def parse_table_command(
        self, raw_command: str, key_table: BindKeyTable
    ) -> tuple[TmuxBindCommand, Sequence]:
        split = [s.strip() for s in re.split(r"\x1f|\s+", raw_command)]
        junk_list = ["bind-key", "-T"]
        repeatable = "-r" in split
        if repeatable:
            junk_list.append("-r")
        for junk in junk_list:
            try:
                split.remove(junk)
            except ValueError as e:
                raise RuntimeError(
                    f'String "{junk}" not found in "{raw_command}" -- malformed input'
                ) from e

        split = [s for s in split if s]
        if key_table.name != (cmd_kt := split.pop(0)):
            raise ValueError(f"Key table name mismatch, expected {key_table.name}, got {cmd_kt}")

        key_combo = self._key_combo_factory.from_tmux(split.pop(0))
        seq = Sequence(only(KeyCombo, [key_table.invoker, key_combo]))
        command = " ".join(split)
        return TmuxBindCommand(command, repeatable), seq


@cli_command(
    name=__file__,
    cls=CliCommand,
    type=CMDTYPE_BUILTIN,
    traits=[CMDTRAIT_ADAPTIVE],
    short_help="current tmux bindings",
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
    Get a list of current tmux bindings, format it and display. Intended to run as
    a tmux popup, but can be invoked directly as well.
    """

    def __init__(self, details: bool, **kwargs):
        self._collector = TmuxBindCollector(details)
        self.run()

    def run(self):
        tmux_data = self.get_raw_binds()
        tmux_data = self.inject_manual_binds(tmux_data)
        self._collector.collect(tmux_data)

        formatter = PopupFormatter(self._collector)
        formatter.print_legend()
        formatter.print_binds()
        formatter.print_cheatsheet()

    def get_raw_binds(self) -> List[str]:
        args = [TMUX_PATH]
        for key_table in self._collector.get_key_table_names():
            args += ["display-message", "-p", f"\x1e{key_table};"]
            args += ["list-keys", "-a", "-T", f"{key_table};"]
            args += ["list-keys", "-aN", "-P", f"\x1f", "-T", f"{key_table};"]
        try:
            p: CompletedProcess = run_subprocess(*args)
        except CalledProcessError as _e:
            raise SubprocessError("Failed to get raw binds from tmux") from _e
        return p.stdout.split("\x1e")

    def inject_manual_binds(self, data: list[str]):
        for idx, line in enumerate(data):
            if line.startswith("root\n"):
                data[idx] = data[idx].replace("root\n", "root\nbind-key    -T root C-a\n")
                data[idx] += "C-a      [mode] Invoke prefix key table\n"
                break
        return data

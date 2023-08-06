# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2022-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import os
import re
import typing as t
from math import floor
from os import getcwd
from pathlib import Path

import click
import pytermor as pt
from pytermor import NOOP_STYLE

from es7s.shared import FrozenStyle, Styles, get_logger, get_stdout
from es7s.shared import SubprocessExitCodeError
from es7s.shared.git import GitRepo
from es7s.shared.plang import PLang
from .._decorators import _catch_and_log_and_exit, cli_argument, cli_command, cli_option
from es7s.shared.linguist import Linguist


@cli_command(__file__, short_help="programming language statistics")
@cli_argument("path", type=click.Path(exists=True), nargs=-1, required=False)
@cli_option(
    "-D",
    "--docker",
    is_flag=True,
    default=False,
    help="Run github-linguist in a docker container.",
)
@cli_option(
    "-N",
    "--no-cache",
    is_flag=True,
    default=False,
    help="Calculate the value regardless of the cache state and do not update it.",
)
@_catch_and_log_and_exit
class invoker:
    """
    ...
    """

    COL_PAD = pt.pad(2)
    SHARED_SCALE_LEN = 40
    SHARED_SCALE_CHAR = "▔"  # "━▁"

    def __init__(
        self,
        docker: bool,
        no_cache: bool,
        path: tuple[Path, ...] | None = None,
        **kwargs,
    ):
        self._use_cache = not no_cache

        stdout = get_stdout()
        if not path:
            path = [
                getcwd(),
            ]

        psetd = dict()
        psetf = set()
        for p in path:
            absp = Path(p).resolve()
            if os.path.isdir(absp):
                try:
                    repo = GitRepo(absp)
                except ValueError as e:
                    get_logger().warning(f"Skipping: {e}")
                    continue
                psetd.setdefault(absp, repo)
            else:
                psetf.add(absp)

        for absp, repo in psetd.items():
            self._run(absp, docker, repo)
        if psetd and psetf:
            stdout.echo()
        for absp in sorted(psetf):
            self._run(absp, docker, None)

    def _run(self, absp: Path, docker: bool, repo: GitRepo = None):
        stdout = get_stdout()
        target = absp
        target_is_dir = repo is not None

        title = str(target)
        data = None

        if repo:
            target = repo.path
            if self._use_cache:
                data = repo.get_cached_stats()
            if str(absp) == os.path.commonpath([absp, repo.path]):
                if repo_name := repo.get_repo_name():
                    title = repo_name
                    if target_is_dir:
                        self._echo_dir_title(title, Styles.TEXT_SUBTITLE)
                        title = None

        if not data:
            try:
                data = Linguist.get_lang_statistics(target, docker, breakdown=target_is_dir)
            except SubprocessExitCodeError as e:
                stdout.echo_rendered(f"Error: {title}", Styles.ERROR)
                get_logger().non_fatal_exception(e)
                return
            if data and repo and self._use_cache:
                repo.update_cached_stats(data)

        if not data:
            stdout.echo((title + ": " if title else ''), nl=False)
            stdout.echo_rendered("<no data>", Styles.TEXT_DEFAULT)
            get_logger().debug("Empty stdout -- no data")
            return

        if target_is_dir:
            get_logger().debug(f"Rendering as directory stats: {absp}")
            self._render_dir_info(data, absp, repo, title)
        else:
            for file_path, file_data in data.items():
                get_logger().debug(f"Rendering as file stats: {file_path}")
                self._render_file_info(file_data, title)
                stdout.echo()

    def _render_dir_info(self, data: dict, absp: Path, repo: GitRepo, title: str|None):
        stdout = get_stdout()
        result: t.List[t.Sequence[pt.RT, ...]] = []
        shared_scale: pt.Text = pt.Text()

        data_flat = [{**v, "lang": k, "linenum": 0} for k, v in data.items()]

        lines_total = 0
        logger = get_logger()
        for lang_data in data_flat:
            linenum = 0
            for filename in lang_data.get("files"):
                stat_file = os.path.abspath(os.path.join(repo.path, filename))
                if str(absp) == os.path.commonpath([absp, Path(stat_file)]):
                    if os.path.isfile(stat_file):
                        logger.debug(f"Counting lines in:'{stat_file}'")
                        try:
                            with open(stat_file, "rt") as fd:
                                linenum += len(fd.readlines())
                        except UnicodeDecodeError as e:
                            logger.non_fatal_exception(
                                f"Failed to count lines (non-UTF8?): '{stat_file}': {e}"
                            )
                            logger.debug(f"Counting lines (BINARY MODE) in:'{stat_file}'")
                            with open(stat_file, "rb") as fd:
                                linenum += len(fd.readlines())
            if not linenum:
                continue
            lang_data.update({"linenum": linenum})
            lines_total += linenum

        data_filtered = filter(lambda v: v["linenum"] > 0, data_flat)

        for lang_data in sorted(data_filtered, key=lambda v: -v.get("linenum")):
            lang = lang_data.get("lang")
            # perc = lang_data.get("percentage")
            # sizeratio = float(perc.removesuffix("%")) / 100
            linenum = lang_data.get("linenum")
            lineratio = linenum / lines_total

            lang_st = self._get_lang_st(lang)
            scale = Scale(lineratio, NOOP_STYLE, lang_st)

            shared_scale += Scale(
                lineratio,
                NOOP_STYLE,
                lang_st,
                self.SHARED_SCALE_LEN,
                False,
                self.SHARED_SCALE_CHAR,
            ).blocks

            result.append(
                (
                    scale,
                    pt.highlight(str(linenum)),
                    pt.Fragment(lang, lang_st),
                )
            )

        if not result:
            return

        if title:
            self._echo_dir_title(title)

        if len(shared_scale) and len(frags := shared_scale.as_fragments()):
            if (chars_short := self.SHARED_SCALE_LEN - len(shared_scale)) > 0:
                if first_frag := frags.pop(0):
                    shared_scale.prepend(
                        pt.Fragment(first_frag.raw()[0] * chars_short, first_frag.style)
                    )
            stdout.echo_rendered(shared_scale)

        def col_lens():
            for col in range(len(result[0])):
                yield max(len(r[col]) for r in result)

        col_len = [*col_lens()]
        for line in result:
            for idx, cell in enumerate(line):
                val = cell
                vpad = pt.pad(col_len[idx] - len(cell))
                if idx in (0, 1):
                    val = vpad + val
                else:
                    val += vpad
                val += self.COL_PAD
                stdout.echo_rendered(val, nl=False)
            stdout.echo()
        stdout.echo()

    def _render_file_info(self, data: dict, title: str):
        stdout = get_stdout()
        col_lens = [9, 9, PLang.get_longest_key_len(), None]
        data_row = []

        code_lines, logic_lines = data["lines"], data["sloc"]
        if zero_len := (code_lines == 0 or logic_lines == 0):
            zfrag = pt.Fragment("-", pt.Highlighter.STYLE_NUL)
            data_row.extend([zfrag] * 2)
        else:
            data_row.extend((pt.highlight(str(code_lines)), pt.highlight(str(logic_lines))))

        ftype = data["type"]
        lang = data["language"]

        if not lang:
            lang_st = NOOP_STYLE if not zero_len else pt.Highlighter.STYLE_NUL
            lang_frag = pt.Fragment(ftype, lang_st)
        else:
            lang_st = self._get_lang_st(lang)
            lang_frag = pt.Fragment(lang, lang_st)
        data_row.append(lang_frag)

        for idx, cell in enumerate(data_row):
            vpad = pt.pad((col_lens[idx] or 0) - len(cell))
            if idx < 2:
                val = vpad + cell
            else:
                val = cell + vpad
            stdout.echo_rendered(self.COL_PAD + val, nl=False)

        stdout.echo(title, nl=False)

    def _echo_dir_title(self, title: str, st: pt.FT = NOOP_STYLE) -> None:
        get_stdout().echo()
        get_stdout().echo_rendered(pt.FrozenText(
            pt.cut(title, self.SHARED_SCALE_LEN, align=pt.Align.RIGHT),
            # print only the ending if title is longer than limit...
            st,
            width=self.SHARED_SCALE_LEN,
            align=pt.Align.CENTER,
            # ...while keeping it centered otherwise.
        ))

    def _get_lang_st(self, lang_str: str) -> FrozenStyle:
        if lang_color := PLang.get(lang_str.strip()):
            return FrozenStyle(fg=pt.ColorRGB(pt.rgb_to_hex(lang_color)))
        return NOOP_STYLE


class Scale(pt.Text):
    SCALE_LEN = 10

    def __init__(
        self,
        ratio: float,
        label_st: pt.FT,
        scale_st: pt.FT,
        length: int = SCALE_LEN,
        allow_partials: bool = True,
        full_block_char: str = "█",
    ):
        self._ratio = ratio
        self._label_st = label_st
        self._scale_st = scale_st
        self._length = length
        self._allow_partials = allow_partials
        self._full_block_char = full_block_char

        self.label: str
        self.blocks: str
        super().__init__(*self._make())

    def _make(self) -> t.Iterable[pt.Fragment]:
        label_str = pt.format_auto_float(100 * self._ratio, 3) + "% "
        self.label = pt.Fragment(" " + label_str, self._label_st)

        char_num: float = self._length * self._ratio
        full_block_num = floor(char_num)
        blocks_str = self._full_block_char * full_block_num
        if self._allow_partials:
            blocks_str += self._get_partial_block(char_num - full_block_num)
        self.blocks = pt.Fragment(blocks_str, self._scale_st)

        yield self.label
        yield self.blocks
        yield pt.Fragment(" " * (self._length - len(self.blocks)), self._scale_st)

    def _get_partial_block(self, val: float) -> str:
        if val >= 7 / 8:
            return "▉"
        elif val >= 6 / 8:
            return "▊"
        elif val >= 5 / 8:
            return "▋"
        elif val >= 4 / 8:
            return "▌"
        elif val >= 3 / 8:
            return "▍"
        elif val >= 2 / 8:
            return "▎"
        elif val >= 1 / 8:
            return "▏"
        return ""

# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2022-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
from __future__ import annotations

import importlib.resources
import inspect
import os.path
import re
from collections.abc import Iterable
from importlib.abc import Traversable
from re import compile
import typing as t
from contextlib import contextmanager
from dataclasses import dataclass
from os.path import basename, dirname, splitext
from typing import ClassVar, cast

import Levenshtein
import click
import pytermor as pt

from es7s import APP_NAME
from es7s.shared import FrozenStyle, Styles, format_attrs, get_logger, get_stdout
from ._base_opts_params import (
    CMDTRAIT_NONE,
    CMDTYPE_BUILTIN,
    CMDTYPE_GROUP,
    CMDTYPE_INTEGRATED,
    CommandAttribute,
    CommandTrait,
    CommandType,
    EPILOG_ARGS_NOTE,
    EPILOG_COMMAND_HELP,
    EPILOG_COMMON_OPTIONS,
    EpilogPart,
    OptionScope,
    ScopedOption,
)
from es7s.shared.strutil import NamedGroupsRefilter, RegexValRefilter
from ..shared.log import LoggerSettings
from ..shared.path import get_config_yaml

AutoDiscoverExtras = t.Callable[[], Iterable["CliBaseCommand"]]


@dataclass(frozen=True)
class Examples:
    title: str
    content: t.Sequence[str]

    def __bool__(self) -> bool:
        return len(self.content) > 0


# fmt: off
class HelpStyles(Styles):
    TEXT_HEADING = FrozenStyle(fg=pt.cv.YELLOW, bold=True)          # SYNOPSIS      |   | explicit manual usage only      # noqa
    TEXT_COMMAND_NAME = FrozenStyle(fg=pt.cv.BLUE)                  # es7s exec     |   | auto-detection                  # noqa
    TEXT_OPTION_DEFAULT = FrozenStyle(fg=pt.cv.HI_YELLOW)           # [default: 1]  |[ ]| requires wrapping in [ ]        # noqa
    TEXT_LITERAL = FrozenStyle(bold=True)                           # 'ls | cat'    | ' | non-es7s commands (punctuation) # noqa
    TEXT_LITERAL_WORDS = FrozenStyle(underlined=True)               # 'ls | cat'    | ' | non-es7s commands (words)       # noqa
    TEXT_EXAMPLE = FrozenStyle(fg=pt.cv.CYAN, bg='full-black')      # ` 4 11`       | ` | input/output example            # noqa
    TEXT_ENV_VAR = FrozenStyle(fg=pt.cv.GREEN, bold=True)           # {ES7S_LE_VAR} |{ }| environment variable name       # noqa
    TEXT_ABOMINATION = FrozenStyle(pt.Style(bg='blue').autopick_fg()) # ::NOTE::    |:: | needs to be wrapped in ::       # noqa
    TEXT_DEPENDENCY = FrozenStyle(fg=pt.cv.RED, underlined=True)    # ++REQ++       |++ | ++required dependency++         # noqa
    TEXT_INLINE_CONFIG_VAR = FrozenStyle(fg=pt.cv.MAGENTA)          # <section.opt> |< >| config variable name            # noqa
    TEXT_PLACEHOLDER = FrozenStyle(italic=True, dim=True)           # <<filename>> |<< >>| placeholder                    # noqa
    TEXT_ALTER_MODE = FrozenStyle(italic=True)                      # ^ALT MODE^    |^ ^| alt monitor mode                # noqa
    TEXT_COMMENT = FrozenStyle(fg=pt.cv.GRAY)                       # // COMMENT    |// | till end of the line            # noqa
    TEXT_WALL = FrozenStyle(fg=pt.cv.WHITE)                         # ░░░░░░░░      |░░░| "░" char in tables              # noqa
    TEXT_ABBREV = FrozenStyle(fg=pt.cv.YELLOW, bold=True)           # &Ab &aB       |&Ww| highlighed part of abbrev       # noqa
    TEXT_ARGUMENT = FrozenStyle(underlined=True)                    # FILE ARGUMENT |   | auto-detection                  # noqa
    TEXT_ACCENT = FrozenStyle(bold=True)                            # *important*   | * | needs to be wrapped in *        # noqa
                                                                      #  '--option' | ' | auto-detection if wrapped in '  # noqa
                                                                      #  "--option" | " | " -> space instead of removing  # noqa
# fmt: on


class HelpFormatter(click.HelpFormatter):
    OPTION_REGEX = compile(R"(?P<val>--?[\w-]+)")
    ARGUMENT_REGEX = compile(R"(?P<val>(?<![{@`´<])\b[A-Z][A-Z0-9_]{3,})(s?\b)")
    WRAP_REGEX = compile(R"(?P<noop>\n\s*|)")

    command_names: ClassVar[list[str]]

    class CommandTypeReplacer(pt.StringReplacer):
        COMMAND_TYPE_NAME_MAP: t.Dict[str, CommandAttribute] = {
            ct.name.lower(): ct for ct in CommandAttribute._values if ct.name
        }

        def __init__(self):
            names = "|".join(self.COMMAND_TYPE_NAME_MAP.keys())
            super().__init__(rf"\[\[({names})\]\]", self.replace)

        def replace(self, m: t.Match) -> str:
            if ct := self.COMMAND_TYPE_NAME_MAP.get(m.group(1), None):
                return get_stdout().render(HelpFormatter.format_command_type_inlined(ct))
            return m.group()

    class LiteralReplacer(pt.StringReplacer):
        def __init__(self):
            super().__init__(
                compile(Rf"'{HelpFormatter.WRAP_REGEX.pattern}([\w./ \n|=-]+?)'"),
                self.replace,
            )

        def replace(self, sm: re.Match) -> str:
            text_literal_is_present = False
            word_count = 0

            def replace_literal(wm: re.Match) -> str:
                nonlocal text_literal_is_present, word_count
                word_count += 1
                word = wm.group()
                if len(word) < 2 and not word.isalpha():  # bold instead of underline
                    text_literal_is_present = True  # for 1-character non-letters,
                    style = HelpStyles.TEXT_LITERAL  # e.g. for '|' pipe symbol.
                elif word in HelpFormatter.command_names or word.startswith(APP_NAME):
                    style = HelpStyles.TEXT_COMMAND_NAME
                elif word.startswith("-"):
                    style = HelpStyles.TEXT_ACCENT
                else:
                    text_literal_is_present = True
                    style = HelpStyles.TEXT_LITERAL_WORDS
                return get_stdout().render(word, style)

            replaced = re.sub(r"(\S+)", replace_literal, (sm.group(1) or "") + sm.group(2))
            if text_literal_is_present and word_count > 1:
                replaced = f"'{replaced}'"
            return replaced

    def __init__(
        self,
        indent_increment: int = 2,
        width: t.Optional[int] = None,
        max_width: t.Optional[int] = None,
    ):
        width = pt.get_preferable_wrap_width(False)
        super().__init__(indent_increment, width, max_width)

        self.help_filters: t.List[pt.StringReplacer] = [
            RegexValRefilter(
                compile(Rf"¯{self.WRAP_REGEX.pattern}(?P<val>.+?)¯"),
                HelpStyles.TEXT_HEADING,
            ),
            RegexValRefilter(self.ARGUMENT_REGEX, HelpStyles.TEXT_ARGUMENT),
            RegexValRefilter(
                compile(R"(^|)?\*(?P<val>[\w!/.-]+?)\*"),
                HelpStyles.TEXT_ACCENT,
            ),
            self.LiteralReplacer(),
            RegexValRefilter(
                compile(Rf"`{self.WRAP_REGEX.pattern}(?P<val>.+?)`"),
                HelpStyles.TEXT_EXAMPLE,
            ),
            pt.filter.StringReplacerChain(
                compile(Rf"´.+?´"),
                RegexValRefilter(
                    compile(Rf"´{self.WRAP_REGEX.pattern}(?P<val>.+?)´"),
                    HelpStyles.TEXT_EXAMPLE,
                ),
                pt.OmniPadder(),
            ),
            pt.StringReplacerChain(
                compile(Rf"(?<!<)<{self.WRAP_REGEX.pattern}([\w\s.-]+?)>"),
                pt.StringReplacer(compile("[<>]"), ""),
                RegexValRefilter(
                    compile(R"(?P<val>[^.]+)"),
                    HelpStyles.TEXT_INLINE_CONFIG_VAR,
                ),
            ),
            pt.StringReplacerChain(
                compile(Rf"(\{{){self.WRAP_REGEX.pattern}([\w.-]+?)(}})"),
                pt.StringReplacer(compile("{(.+)}"), r" \1 "),
                RegexValRefilter(
                    compile(R"(?P<val>.+)"),
                    HelpStyles.TEXT_ENV_VAR,
                ),
            ),
            RegexValRefilter(
                compile(r"\+\+(?P<val>[\w./-]+?:*)\+\+"),
                HelpStyles.TEXT_DEPENDENCY,
            ),
            RegexValRefilter(
                compile(r"@(?P<val>[()\w._-]+?)@"),
                HelpStyles.TEXT_ENV_VAR,
            ),
            pt.StringReplacerChain(
                compile(R"::(?P<val>[\w./-]+?:*)::"),
                pt.OmniPadder(2),
                NamedGroupsRefilter(
                    compile(R"(?P<s1>\s)(\s)::(.+)::(\s)(?P<s2>\s)"),
                    {"": HelpStyles.TEXT_ABOMINATION},  # any
                ),
            ),
            RegexValRefilter(
                compile(R"(^|\s+)//(?P<val>\s.+)"),
                HelpStyles.TEXT_COMMENT,
            ),
            RegexValRefilter(
                compile(R"/\*(?P<val>.+?)\*/", flags=re.DOTALL),
                HelpStyles.TEXT_COMMENT,
            ),
            self.CommandTypeReplacer(),
            NamedGroupsRefilter(
                compile(R"<?(<)(?P<noop>\n\s*|)([\w\s.-]+?)(>)>?"),
                {"": HelpStyles.TEXT_PLACEHOLDER},  # any
            ),
            RegexValRefilter(
                compile(Rf"'{self.WRAP_REGEX.pattern}{self.OPTION_REGEX.pattern}'"),
                HelpStyles.TEXT_ACCENT,
            ),
            pt.filter.StringReplacerChain(
                compile(Rf'"[^\x1b]+?"'),
                RegexValRefilter(
                    compile(Rf'"{self.WRAP_REGEX.pattern}(?P<val>.+?)"'),
                    HelpStyles.TEXT_ACCENT,
                ),
                pt.OmniPadder(),
            ),
            RegexValRefilter(
                compile(Rf"(default:){self.WRAP_REGEX.pattern}(?P<val>.+?)([];])"),
                HelpStyles.TEXT_OPTION_DEFAULT,
            ),
            RegexValRefilter(
                compile(Rf"(\[)([\w\s]+)(?P<val>default)(])"),
                HelpStyles.TEXT_OPTION_DEFAULT,
            ),
            pt.filter.StringReplacerChain(
                compile(Rf"\^.+?\^"),
                RegexValRefilter(
                    compile(Rf"\^{self.WRAP_REGEX.pattern}(?P<val>.+?)\^"),
                    HelpStyles.TEXT_ALTER_MODE,
                ),
                pt.OmniPadder(),
            ),
            RegexValRefilter(
                compile(R"(?P<val>░{2,})"),
                HelpStyles.TEXT_WALL,
            ),
            NamedGroupsRefilter(
                compile(r"&(?:(?P<sval>\w)|\((?P<mval>\w+)\))"),
                {"sval": HelpStyles.TEXT_ABBREV, "mval": HelpStyles.TEXT_ABBREV},
            ),
        ]

        if not hasattr(HelpFormatter, "command_names"):
            HelpFormatter.command_names = [APP_NAME]
            if (ctx := click.get_current_context(True)) is None:
                return
            HelpFormatter.command_names = self._find_all_command_names(ctx.find_root().command)

    def _find_all_command_names(self, command: click.Command) -> set[str]:
        names = set()
        names.add(command.name)
        if hasattr(command, "commands") and isinstance(command.commands, dict):
            for nested_command in command.commands.values():
                names = names.union(self._find_all_command_names(nested_command))
        return names

    @classmethod
    def format_command_name(cls, arg: re.Match | str) -> str:
        if isinstance(arg, re.Match):
            arg = arg.group(1)
        return get_stdout().render(arg, HelpStyles.TEXT_COMMAND_NAME)

    def format_accent(self, arg: re.Match | str) -> str:
        if isinstance(arg, re.Match):
            arg = arg.group(1) + arg.group(2)
        return get_stdout().render(arg, HelpStyles.TEXT_ACCENT)

    @contextmanager
    def section(self, name: str | None) -> t.Iterator[None]:
        # modified version of parent implementation; could not inject otherwise
        # changes: `name` is nullable now; do not write heading if `name` is empty
        self.write_paragraph()
        if name:
            self.write_heading(name)
        self.indent()
        try:
            yield
        finally:
            self.dedent()

    @classmethod
    def format_command_icon(cls, cmd: CliBaseCommand) -> pt.Fragment:
        ct = cmd.get_command_type()
        icon_char = ct.char
        icon_color = ct.get_icon_char_fmt(cmd.get_command_trait().fmt)
        return pt.Fragment(icon_char, icon_color)

    @classmethod
    def format_command_icon_and_name(cls, cmd: CliBaseCommand) -> pt.Text:
        return cls.format_command_icon(cmd) + " " + cls.format_command_name(cmd.name)

    @classmethod
    def format_command_attribute_legend(cls, ct: CommandType | CommandTrait) -> pt.Text:
        if isinstance(ct, CommandType):
            return (
                pt.Fragment("[")
                + pt.Fragment(ct.char, ct.get_icon_char_fmt())
                + pt.Fragment("] " + ct.name)
            )
        return pt.Fragment(f" {ct.char} ", ct.fmt) + pt.Fragment(" " + ct.name)

    @classmethod
    def format_command_type_inlined(cls, ct: CommandType) -> pt.Text:
        return cls.format_command_own_type(ct) + pt.Fragment(" " + ct.name)

    @classmethod
    def format_command_own_type(cls, ct: CommandAttribute) -> pt.Fragment:
        return pt.Fragment(ct.get_own_char(), ct.get_own_fmt())

    def write_heading(
        self,
        heading: str,
        newline: bool = False,
        colon: bool = True,
        st: pt.Style = HelpStyles.TEXT_HEADING,
    ):
        heading = get_stdout().render(heading + (colon and ":" or ""), st)
        self.write(f"{'':>{self.current_indent}}{heading}")
        self.write_paragraph()
        if newline:
            self.write_paragraph()

    def write_text(self, text: str) -> None:
        self.write(
            pt.wrap_sgr(
                text,
                self.width,
                indent_first=self.current_indent,
                indent_subseq=self.current_indent,
            )
        )

    def write_squashed_text(self, string: str):
        wrapped_text = pt.wrap_sgr(
            string,
            self.width,
            indent_first=self.current_indent,
            indent_subseq=self.current_indent,
        )
        self.write(wrapped_text.replace("\n\n", "\n"))  # @REFACTOR wat
        self.write("\n")

    # def write(self, string: str) -> None:
    #     ...
    #     self.buffer.append(string)

    def _postprocess(self, string: str) -> str:
        stripped = string.strip()
        if stripped in HelpFormatter.command_names:
            string = get_stdout().render(string, HelpStyles.TEXT_COMMAND_NAME)
        return pt.apply_filters(string, *self.help_filters)

    def getvalue(self) -> str:
        return self._postprocess(super().getvalue())


class Context(click.Context):
    formatter_class = HelpFormatter

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.failed = False
        self.color = get_stdout().color
        self.logger_setup: LoggerSettings = get_logger().setup

    def fail(self, message: str):
        self.failed = True
        raise UsageError(message, ctx=self)


class UsageError(click.UsageError):
    def __init__(self, message: str, ctx: t.Optional[Context] = None) -> None:
        super().__init__(message, ctx)
        self.ctx = ctx

    def show(self, file: t.Optional[t.IO] = None) -> None:
        if not self.ctx.logger_setup.print_usage_errors:
            return
        super().show(file)


class CliBaseCommand(click.Command):
    context_class = Context

    def __init__(self, name, **kwargs):
        kwargs.setdefault("type", CMDTYPE_BUILTIN)
        self._include_common_options_epilog = kwargs.pop("include_common_options_epilog", True)
        self._command_type: CommandType = kwargs.pop("type")
        self._command_traits: t.Sequence[CommandTrait] = kwargs.pop("traits", [])
        self._usage_section_name = kwargs.pop("usage_section_name", "Usage")

        base_name = name or kwargs.get("name")
        if ".py" in base_name:
            base_name = splitext(basename(base_name))
            self._file_name_parts = base_name[0].lstrip("_").split("_")
        else:
            self._file_name_parts = [base_name]

        context_settings = kwargs.pop("context_settings", {})
        context_settings_extras = {
            "ignore_unknown_options": kwargs.pop("ignore_unknown_options", None),
            "allow_extra_args": kwargs.pop("allow_extra_args", None),
        }
        context_settings.update(
            **{k: v for k, v in context_settings_extras.items() if v is not None}
        )

        super().__init__(name, context_settings=context_settings, **kwargs)

    def get_command_type(self) -> CommandType:
        return self._command_type

    def get_command_trait(self) -> CommandTrait:
        if self._command_traits:
            return self._command_traits[-1]
        return CMDTRAIT_NONE

    def parse_args(self, ctx: Context, args: t.List[str]) -> t.List[str]:
        get_logger().debug(f"Pre-click args:  {format_attrs(args)}")
        try:
            return super().parse_args(ctx, args)
        except click.UsageError as e:
            ctx.fail(e.message)

    def invoke(self, ctx: Context) -> t.Any:
        get_logger().debug(f"Post-click args: {format_attrs(ctx.params)}")
        try:
            return super().invoke(ctx)
        except click.ClickException as e:
            ctx.failed = True
            self.show_error(ctx, e)

    def show_error(self, ctx: Context, e: click.ClickException):
        logger = get_logger()
        logger.error(e.format_message())
        if not logger.setup.print_click_errors:
            return

        hint = ""
        if ctx.command.get_help_option(ctx):
            hint = f"\nTry '{ctx.command_path} {ctx.help_option_names[0]}' for help."
        get_stdout().echo(f"{ctx.get_usage()}\n{hint}")

    def _make_command_name(self, orig_name: str) -> str:
        dir_name = basename(dirname(orig_name))
        filename_parts = splitext(basename(orig_name))[0].rstrip("_").split("_")
        if filename_parts[0] == "":  # because of '_group' -> ['', 'group']
            filename_parts = [dir_name.rstrip("_")]  # 'exec_' -> 'exec'
        return "-".join(filename_parts)

    def _make_short_help(self, **kwargs) -> str:
        help_str = kwargs.get("help")
        if not help_str:
            if logger := get_logger(require=False):
                logger.warning(f"Missing help for '{kwargs.get('name')}' command")
            help_str = "..."

        short_help = kwargs.get("short_help")
        short_help_auto = help_str.lower().removesuffix(".")
        if isinstance(short_help, t.Callable):
            return short_help(short_help_auto)
        elif short_help:
            return short_help
        return short_help_auto

    def format_usage(self, ctx: Context, formatter: HelpFormatter) -> None:
        pieces = self.collect_usage_pieces(ctx)
        with formatter.section(self._usage_section_name):
            formatter.write_usage(
                formatter.format_command_name(ctx.command_path), " ".join(pieces), prefix=""
            )

    def format_own_type(self, ctx: Context, formatter: HelpFormatter):
        stdout = get_stdout()

        with formatter.indentation():
            descriptions = []
            for ct in [self.get_command_type(), self.get_command_trait()]:
                ct_icon = stdout.render(formatter.format_command_own_type(ct))
                ct_description = (
                    ct.description % ct_icon if "%s" in ct.description else ct.description
                )

                if ct_description.count("|") == 2:
                    left, hightlight, right = ct_description.split("|", 2)
                    descriptions.append(
                        (
                            stdout.render(left, HelpStyles.TEXT_COMMENT)
                            + stdout.render(" " + hightlight + " ", ct.get_own_label_fmt())
                            + stdout.render(right, HelpStyles.TEXT_COMMENT)
                        )
                    )
                else:
                    descriptions.append(ct_description)

            formatter.write_paragraph()
            formatter.write_text("\n\n".join(filter(None, descriptions)))

    def format_common_options(self, ctx: Context, formatter: HelpFormatter, add_header: bool):
        if self._include_common_options_epilog:
            with formatter.section("Options" if add_header else ""):
                if add_header:
                    formatter.write_text("No specific options.")
                    formatter.write_paragraph()
                formatter.write_text(EPILOG_COMMON_OPTIONS.text)

    def format_epilog(self, ctx: Context, formatter: HelpFormatter) -> None:
        self._format_epilog_parts(formatter, [*self._get_epilog_parts(ctx)])

    def _get_epilog_parts(self, ctx: Context) -> t.Generator[list]:
        if self.epilog:
            if not isinstance(self.epilog, list):
                self.epilog = [self.epilog]
            yield from self.epilog

    def _format_epilog_parts(self, formatter: HelpFormatter, parts: list[EpilogPart]):
        squashed_parts = []
        for idx, part in enumerate(parts):
            if (
                len(squashed_parts)
                and not part.title
                and part.group
                and part.group == squashed_parts[-1].group
            ):
                squashed_parts[-1].text += "\n\n" + part.text
                continue
            squashed_parts.append(part)

        for part in squashed_parts:
            self._format_epilog_part(formatter, part)

    def _format_epilog_part(self, formatter: HelpFormatter, part: EpilogPart):
        formatter.write_paragraph()
        if part.title:
            formatter.write_heading(part.title.capitalize(), newline=False, colon=False)

        with formatter.indentation():
            formatter.write_text(part.text)

    def _is_option_with_argument(self, option: click.Parameter) -> bool:
        if isinstance(option, ScopedOption):
            return option.has_argument()
        return False


class CliCommand(CliBaseCommand):
    option_scopes: list[OptionScope] = [
        OptionScope.COMMAND,
        OptionScope.GROUP,
    ]

    def __init__(self, **kwargs):
        kwargs.update(
            {
                "name": self._make_command_name(kwargs.get("name")),
                "params": self._build_options(kwargs.get("params", [])),
                "short_help": self._make_short_help(**kwargs),
            }
        )
        self._command_examples = Examples("Command examples", kwargs.pop("command_examples", []))
        self._output_examples = Examples("Output examples", kwargs.pop("output_examples", []))
        self._ext_help_invoker: t.Callable[[Context], str] = kwargs.pop("ext_help_invoker", None)

        super().__init__(**kwargs)

    def _build_options(self, subclass_options: list[ScopedOption]) -> list[ScopedOption]:
        return [
            *subclass_options,
            *self._get_group_options(),
        ]

    def _get_group_options(self) -> list[ScopedOption]:
        return []

    def format_help(self, ctx: Context, formatter: HelpFormatter) -> None:
        super().format_help(ctx, formatter)

        if self._ext_help_invoker is None:
            return
        result_generic = formatter.getvalue()
        formatter.buffer.clear()

        seq_color_bg = f"{pt.cv.GRAY_15.to_sgr(pt.ColorTarget.BG)}"
        seq_color_bg_line = f"{seq_color_bg}{pt.make_clear_line_after_cursor()}"

        inject_bg_rr = pt.StringReplacer(
            pt.SGR_SEQ_REGEX,
            lambda m: m.group(0) + (seq_color_bg if self._has_bg_or_reset_param(m) else ""),
        )
        enclose_bg_rr = pt.StringReplacer(compile("(^|\n|$)"), rf"\1{seq_color_bg_line}")
        result_generic = pt.apply_filters(result_generic, inject_bg_rr, enclose_bg_rr) + str(
            pt.SeqIndex.RESET
        )
        get_stdout().echo(result_generic)
        get_stdout().echo()

        if result_component := self._ext_help_invoker(ctx):
            get_stdout().echo(result_component)
        else:
            formatter.write_heading(f"Component help")
            with formatter.indentation():
                formatter.write_text("<<Empty>>")
            get_stdout().echo(formatter.getvalue())
        formatter.buffer.clear()

    @staticmethod
    def _has_bg_or_reset_param(m: t.Match) -> bool:
        for c in m.group(3).split(";"):
            if not c:  # ""="0"
                return True
            try:
                i = int(c)
            except ValueError:
                continue
            if i in (pt.IntCode.RESET, pt.IntCode.BG_COLOR_OFF, pt.IntCode.INVERSED_OFF):
                return True

    def format_help_text(self, ctx: Context, formatter: HelpFormatter) -> None:
        super().format_help_text(ctx, formatter)
        self.format_examples(ctx, formatter, self._output_examples)
        self.format_own_type(ctx, formatter)

    def format_options(self, ctx: Context, formatter: HelpFormatter):
        opt_scope_to_opt_help_map: dict[str, list[tuple[str, str]] | None] = {
            k: [] for k in OptionScope
        }
        for param in self.get_params(ctx):
            rv = param.get_help_record(ctx)
            if rv is not None and hasattr(param, "scope"):
                opt_scope_to_opt_help_map[param.scope].append(rv)

        has_header = False
        for opt_scope in self.option_scopes:
            opt_helps = opt_scope_to_opt_help_map[opt_scope]
            if not opt_helps:
                continue
            if opt_scope.value:
                has_header = True
                with formatter.section(opt_scope.value):
                    formatter.write_dl(opt_helps)
            else:
                formatter.write_paragraph()
                with formatter.indentation():
                    formatter.write_dl(opt_helps)

        if any(self._is_option_with_argument(opt) for opt in ctx.command.params):
            formatter.write_paragraph()
            with formatter.indentation():
                formatter.write_text(inspect.cleandoc(EPILOG_ARGS_NOTE.text))

        self.format_common_options(ctx, formatter, not has_header)

    def format_epilog(self, ctx: Context, formatter: HelpFormatter) -> None:
        super().format_epilog(ctx, formatter)
        self.format_examples(ctx, formatter, self._command_examples)

    def format_examples(self, ctx: Context, formatter: HelpFormatter, examples: Examples) -> None:
        if not examples:
            return
        with formatter.section(examples.title.capitalize()):
            for example in examples.content:
                example = re.sub(
                    r"(\s)" + formatter.OPTION_REGEX.pattern,  # костыль; сам по себе OPTION_REGEX
                    formatter.format_accent(r"\1\2"),  # матчит "-15" в "--date Nov-15"
                    example,
                )
                if "%s" in example:
                    example %= formatter.format_command_name(ctx.command_path)
                formatter.write_text(example)


class CliGroup(click.Group, CliBaseCommand):
    TEXT_COMMAND_MATCHED_PART = FrozenStyle(fg=pt.cv.HI_BLUE, underlined=True)
    TEXT_COMMAND_SUGGEST_1ST_CHR = FrozenStyle(fg=pt.cv.HI_RED, bold=True, underlined=False)
    TEXT_COMMAND_SUGGEST_OTHERS = HelpStyles.TEXT_COMMAND_NAME

    _integrated_cfgs: t.ClassVar[dict[str, dict]] = None
    _autogroup_cfgs: t.ClassVar[dict[str, dict]] = None

    def __new__(cls, *args, **kwargs):
        if not cls._integrated_cfgs:
            cls._integrated_cfgs = get_config_yaml("cmd-integrated").get("commands")
        if not cls._autogroup_cfgs:
            cls._autogroup_cfgs = get_config_yaml("cmd-autogroup").get("groups")
        return super().__new__(cls)

    def __init__(self, **kwargs):
        self._filepath = kwargs.get("name")
        autodiscover_extras: AutoDiscoverExtras = kwargs.pop("autodiscover_extras", None)

        kwargs["name"] = self._make_command_name(self._filepath)
        kwargs["short_help"] = self._make_short_help(**kwargs)
        kwargs.setdefault("type", CMDTYPE_GROUP)

        super().__init__(**kwargs)
        self.autodiscover(autodiscover_extras)

    def autodiscover(self, extras: AutoDiscoverExtras = None):
        subpkg = os.path.relpath(os.path.dirname(self._filepath), os.path.dirname(__file__))
        pkg = (__package__ + "." + subpkg.replace("/", ".")).rstrip(".")

        for el in importlib.resources.files(pkg).iterdir():
            if el.is_dir() or (el.is_file() and el.name.startswith("_group")):
                self._register_group(el, pkg)
            elif el.is_file() and re.fullmatch(r"[^_].*\.py", el.name):
                self._register_builtin(el, pkg)
            elif el.is_file() and re.fullmatch(r"[^_].+\.sh", el.name):
                self._register_integrated(el, pkg)

        if extras:
            self.add_commands(extras())

    def _register_group(self, el: Traversable, pkg: str):
        name = el.name.removesuffix(".py")
        mod = importlib.import_module("." + name, pkg)
        if fn := getattr(mod, "group", None):
            self.add_command(fn)
        elif not name.startswith("_"):
            from ._decorators import cli_group

            cfgkey = pkg + "." +name
            cfg = self._autogroup_cfgs.get(cfgkey)
            assert cfg is not None, f"No config for autogroup {cfgkey}"
            extras = getattr(mod, "autodiscover_extras", None)
            filepath = os.path.abspath(str(el.joinpath("__init__.py")))
            grp = cli_group(name=filepath, autodiscover_extras=extras, **cfg)(lambda: None)
            self.add_command(grp)

    def _register_builtin(self, el: Traversable, pkg: str):
        mod = importlib.import_module("." + el.name.removesuffix(".py"), pkg)
        if fn := getattr(mod, "invoker", None):
            self.add_command(fn)

    def _register_integrated(self, el: Traversable, pkg: str):
        from ._foreign import ForeignCommand

        cfgkey = pkg + "." +el.name.removesuffix(".sh")
        cfg = self._integrated_cfgs.get(cfgkey)
        assert cfg is not None, f"No config for integrated command {cfgkey}"
        fcmd = ForeignCommand(os.path.abspath(str(el)), cfg, CMDTYPE_INTEGRATED)
        self.add_command(fcmd)

    def format_help_text(self, ctx: Context, formatter: HelpFormatter) -> None:
        super().format_help_text(ctx, formatter)
        # self.format_own_type(ctx, formatter)

    def format_options(self, ctx: Context, formatter: HelpFormatter) -> None:
        # no options for groups
        self.format_commands(ctx, formatter)
        # self.format_subcommand_attributes(formatter)

    def format_subcommand_attributes(self, formatter: HelpFormatter):
        cts = [
            *filter(
                lambda ct: not ct.hidden,
                {*self.get_command_attributes()},
            )
        ]
        if not len(cts):
            return

        formatter.write_paragraph()
        with formatter.indentation():
            formatter.write_text(
                "   ".join(
                    get_stdout().render(formatter.format_command_attribute_legend(ct))
                    for ct in sorted(cts, key=lambda ct: ct.sorter)
                )
            )
        formatter.write_paragraph()

    def format_commands(self, ctx: Context, formatter: HelpFormatter) -> None:
        # modified version of parent implementation; could not inject otherwise
        commands = []
        for subcommand in self.list_commands(ctx):
            cmd = self.get_command(ctx, subcommand)
            # What is this, the tool lied about a command.  Ignore it
            if cmd is None:
                continue
            if cmd.hidden:
                continue
            commands.append((subcommand, cmd))

        if len(commands):
            # +2 for command type
            limit = formatter.width - 6 - max(2 + len(cmd[0]) for cmd in commands)

            rows = []
            for subcommand, cmd in commands:
                help = cmd.get_short_help_str(limit)
                cmd_name = get_stdout().render(formatter.format_command_icon_and_name(cmd))
                rows.append((cmd_name, help))

            if rows:
                with formatter.section("Commands"):
                    formatter.write_dl(rows, col_spacing=4)

    def add_commands(self, commands: Iterable[click.Command]):
        for cmd in commands:
            self.add_command(cmd)

    def get_commands(self) -> dict[str, CliBaseCommand]:
        return cast(dict[str, CliBaseCommand], self.commands)

    def get_command(self, ctx, cmd_name) -> CliBaseCommand | None:
        """
        When there is no exact match, search for commands that begin
        with the string the user has been typed, and return the matched
        command if it is the only one matching (e.g., 'es7s e' -> 'es7s exec').
        Otherwise print the closest by levenshtein distance command if no
        matches were found ('es7s ez' -> 'es7s exec'), or print all the partial
        matches if there are more than 1 of them ('es7s m' -> 'es7s manage',
        'es7s monitor').
        """
        rv = super().get_command(ctx, cmd_name)
        if rv is not None:
            return cast(CliBaseCommand, rv)

        matches = []
        lev_match, lev_match_dist = None, None
        for c in self.list_commands(ctx):
            if c.startswith(cmd_name):
                matches.append(c)
            ld = Levenshtein.distance(cmd_name, c)
            if not lev_match or ld <= lev_match_dist:
                lev_match, lev_match_dist = c, ld

        if not matches:
            get_logger().debug(f"No matches")
            lev_msg = ""
            if lev_match:
                get_logger().debug(f"Closest by lev. distance: {lev_match}")
                lev_msg = f"\n\nThe most similar command is:\n    {lev_match}"
            ctx.fail(f"No such command: '{cmd_name}'{lev_msg}")
            return None
        elif len(matches) == 1:
            get_logger().debug(f"Matched by prefix: {matches[0]}")
            return super().get_command(ctx, matches[0])
        # elif len(matches) > 1:

        stdout = get_stdout()

        def format_suggestions(m: t.Iterable[str]) -> str:
            suggs = [*map(lambda s: s.removeprefix(cmd_name), m)]
            same_chars_after = max(map(len, suggs))
            for i in range(same_chars_after):
                if any(len(s) <= i for s in suggs):
                    same_chars_after = i
                    break
                if len({*map(lambda s: s[i], suggs)}) > 1:  # unique characters at position <i>
                    same_chars_after = i + 1
                    break
            get_logger().debug(f"Shortest unique seq. length = {same_chars_after:d}")
            return ", ".join(map(lambda s: format_suggestion(s, same_chars_after), suggs))

        def format_suggestion(s: str, same_chars_after: int) -> str:
            return (
                stdout.render(cmd_name, self.TEXT_COMMAND_MATCHED_PART)
                + stdout.render(s[:same_chars_after], self.TEXT_COMMAND_SUGGEST_1ST_CHR)
                + stdout.render(s[same_chars_after:], self.TEXT_COMMAND_SUGGEST_OTHERS)
            )

        get_logger().debug(f"Several matches ({len(matches)}): {format_attrs(matches)}")
        ctx.fail(f"Several matches: {format_suggestions(sorted(matches))}")

    def resolve_command(self, ctx, args):
        # always return the full command name
        _, cmd, args = super().resolve_command(ctx, args)
        return cmd.name, cmd, args

    def get_command_attributes(self, recursive: bool = False) -> t.Iterable[CommandAttribute]:
        for cmd in self.get_commands().values():
            if recursive and isinstance(cmd, CliGroup):
                yield from cmd.get_command_attributes(True)
            yield cmd.get_command_type()
            yield cmd.get_command_trait()

    def _get_epilog_parts(self, ctx: Context) -> t.Generator[list]:
        yield from super()._get_epilog_parts(ctx)
        yield EPILOG_COMMON_OPTIONS

        if not self.commands:
            return

        if non_group_subcmds := sorted(
            filter(lambda cmd: not isinstance(cmd, CliGroup), self.commands.values()),
            key=lambda v: v.name,
        ):
            example_cmd = non_group_subcmds[0]
        else:
            example_cmd = [*self.commands.values()][0]

        yield EpilogPart(
            EPILOG_COMMAND_HELP.text % (ctx.command_path, ctx.command_path, example_cmd.name),
            group=EPILOG_COMMAND_HELP.group,
        )

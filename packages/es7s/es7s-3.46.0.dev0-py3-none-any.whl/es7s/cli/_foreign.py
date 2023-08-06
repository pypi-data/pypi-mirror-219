# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import os
from importlib import resources
from os.path import expanduser

from es7s.shared import (
    SubprocessExitCodeError,
    format_attrs,
    get_color,
    get_logger,
    get_merged_uconfig,
    run_subprocess,
)
from es7s.shared import RESOURCE_PACKAGE, SHELL_COMMONS_FILE, SHELL_PATH, USER_ES7S_BIN_DIR
from ._base import CliCommand
from ._base_opts_params import CommandType, EpilogPart
from ._decorators import _catch_and_log_and_exit, cli_command, cli_pass_context


class ForeignCliCommand(CliCommand):
    """
    Launch the external/integrated component. PASSARGS are the arguments that
    will be passed to an external app. Long options can also be used, but make
    sure to prepend the "transit" options with "--" to help `click` library to
    distinguish them from its own options. Short options are known to be buggy,
    better just avoid using them on indirect invocations of standalone apps.
    """

    EPILOG_PARTS = [
        EpilogPart(
            "This first command will result in 'es7s' command help text, along with "
            "embedded help from the external component, while the second will result in "
            "'watson's direct call and only its own usage being displayed:",
            title="Invocation (generic):",
            group="ex1",
        ),
        EpilogPart("  (1) 'es7s exec watson --help'", group="ex1"),
        EpilogPart("  (2) 'es7s exec watson -- --help'", group="ex1"),
        EpilogPart(
            "Another way to invoke an external component is to call it directly:",
            group="ex2",
        ),
        EpilogPart("  (3) 'watson --help'", group="ex2"),
    ]

    def __init__(self, **kwargs):
        kwargs.update(
            {
                "help": self.__doc__,
                "epilog": self.EPILOG_PARTS,
            }
        )
        super().__init__(**kwargs)


class ForeignInvoker:
    def __init__(self, target: str = "bash"):
        self._target = target

    def spawn(self, *args: str, wait=True) -> None:
        cmd_target, cmd_args = self._get_spawn_cmd(*args)
        get_logger().info(f"Launching: {cmd_target} {format_attrs(cmd_args)}")
        code = os.spawnvpe(
            os.P_WAIT if wait else os.P_NOWAIT,
            cmd_target,
            cmd_args,
            self._build_env(),
        )
        # if code == 127:
        #    raise ExecutableNotFoundError(self._target)
        if wait and code != 0:
            raise SubprocessExitCodeError(code, args)
        if not wait:
            get_logger().debug(f"Spawned PID: {code}")

    def _get_spawn_cmd(self, *args: str) -> tuple[str, list]:
        return self._target, [self._target, *args]

    def get_help(self) -> str:
        _, cmd_args, cmd_shell = self._get_help_cmd()
        cp = run_subprocess(
            " ".join(cmd_args),
            shell=cmd_shell,
            env=self._build_env(),
            timeout=10,
        )
        if cp.stderr:
            get_logger().non_fatal_exception(cp.stderr)
        return cp.stdout

    def _get_help_cmd(self) -> tuple[str, list, bool]:
        return SHELL_PATH, [self._target, "--help"], True

    def _build_env(self) -> dict:
        logger = get_logger()
        commons_path = resources.path(RESOURCE_PACKAGE, SHELL_COMMONS_FILE)
        user_repos_path = get_merged_uconfig().get("general", "user-repos-path", fallback="")
        theme_seq = get_color().get_theme_color().to_sgr()
        result = {
            # ---[@temp]--- filter out all G1/G2 es7s env vars:
            **{k: v for (k, v) in os.environ.items() if not k.lower().startswith("es7s")},
            # ---[@temp]---
            "PATH": self._build_path(),
            # "COLORTERM": os.environ.get("COLORTERM"),
            # "TERM": os.environ.get("TERM"),
            "ES7S_SHELL_COMMONS": commons_path,
            "ES7S_USER_REPOS_PATH": user_repos_path,
            "ES7S_THEME_COLOR_SGR": ";".join(map(str, theme_seq.params)),
        }
        logger.debug("Setting up the environment")
        for k, v in sorted(result.items(), key=lambda k: k):
            logger.trace(format_attrs(v), k, out_plain=False, out_sanitized=True)
        return result

    def _build_path(self) -> str:
        current = os.environ.get("PATH", "").split(":")
        filtered = ":".join(
            [
                # ---[@temp]----- remove all deprecated es7s parts from PATH:
                *filter(lambda s: "es7s" not in s, current),
                expanduser("~/bin/es7s"),
                # ---[@temp]----- ^ restore legacy path
                USER_ES7S_BIN_DIR,  # add G3 path
            ]
        )
        return filtered


def ForeignCommand(target: str, attributes: dict, type: CommandType):
    inv = ForeignInvoker(target)
    cmd = lambda ctx, inv=inv: inv.spawn(*ctx.args)
    cmd = _catch_and_log_and_exit(cmd)
    cmd = cli_pass_context(cmd)
    cmd = cli_command(
        **attributes,
        name=target.removesuffix(".sh"),
        cls=ForeignCliCommand,
        type=type,
        ignore_unknown_options=True,
        allow_extra_args=True,
        ext_help_invoker=lambda ctx, inv=inv: inv.get_help(),
        usage_section_name="Usage (generic)",
        include_common_options_epilog=False,
    )(cmd)
    return cmd

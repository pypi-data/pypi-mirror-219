# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2021-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
from __future__ import annotations

import os
import typing as t
from configparser import ConfigParser as BaseConfigParser
from contextlib import contextmanager
from dataclasses import dataclass
from importlib import resources
from os import makedirs, path
from os.path import dirname, isfile

from .log import get_logger
from .path import RESOURCE_PACKAGE, USER_ES7S_DATA_DIR
from .. import APP_NAME

_merged_uconfig: UserConfig | None = None
_dist_uconfig: UserConfig | None = None


@dataclass
class UserConfigParams:
    default: bool = False


class UserConfig(BaseConfigParser):
    def __init__(self, params: UserConfigParams = None):
        self.params = params or UserConfigParams()
        super().__init__(interpolation=None)

        self._invalid: RuntimeError | None = None
        self._already_logged_options: t.Set[t.Tuple[str, str]] = set()
        self._logging_enabled = True

    def get(self, section: str, option: str, *args, **kwargs) -> t.Any:
        self.ensure_validity()
        log_msg = f"Getting config value: {section}.{option}"
        result = None
        try:
            result = super().get(section, option, *args, **kwargs)
        except Exception:
            raise
        finally:
            if self._logging_enabled:
                log_msg += f" = " + (
                    '"' + result.replace("\n", " ") + '"' if result else str(result)
                )
                get_logger().debug(log_msg)
        return result

    def getintlist(self, section: str, option: str, *args, **kwargs) -> list[int]:
        try:
            return [*map(int, filter(None, self.get(section, option).splitlines()))]
        except ValueError as e:
            raise RuntimeError(f"Conversion to [int] failed for: {section}.{option}") from e

    def get_monitor_debug_mode(self) -> bool:
        if (env_var := os.getenv("ES7S_MONITOR_DEBUG", None)) is not None:
            return True if env_var != "" else False
        return self.getboolean("monitor", "debug", fallback=False)

    def get_indicator_debug_mode(self) -> bool:
        if (env_var := os.getenv("ES7S_INDICATOR_DEBUG", None)) is not None:
            return True if env_var != "" else False
        return self.getboolean("indicator", "debug", fallback=False)

    def get_cli_debug_io_mode(self) -> bool:
        if (env_var := os.getenv("ES7S_CLI_DEBUG_IO", None)) is not None:
            return True if env_var != "" else False
        with self._disabled_logging():
            return self.getboolean("cli", "debug-io", fallback=False)

    def invalidate(self):
        self._invalid = True

    def ensure_validity(self):
        if self._invalid:
            raise RuntimeError(
                "Config can be outdated. Do not cache config instances (at most "
                "-- store as local variables in the scope of the single function), "
                "call get_config() to get the fresh one instead."
            )

    def set(self, section: str, option: str, value: str | None = ...) -> None:
        raise RuntimeError(
            "Do not call set() directly, use rewrite_user_value(). "
            "Setting config values directly can lead to writing default "
            "values into user's config even if they weren't there at "
            "the first place."
        )

    def _set(self, section: str, option: str, value: str | None = ...) -> None:
        self.ensure_validity()
        if self._logging_enabled:
            log_msg = f'Setting config value: {section}.{option} = "{value}"'
            get_logger().info(log_msg)

        super().set(section, option, value)

    @contextmanager
    def _disabled_logging(self, **kwargs):
        self._logging_enabled = False
        try:
            yield
        finally:
            self._logging_enabled = True


def get_dist_filepath() -> str:
    filename = "es7s.conf.d"
    user_path = os.path.join(USER_ES7S_DATA_DIR, filename)
    get_logger(False).debug(f"User config path: '{user_path}'")

    if os.path.isfile(user_path):
        if os.path.islink(user_path):
            return os.readlink(user_path)
        return user_path
    else:
        dc_filepath = str(resources.path(RESOURCE_PACKAGE, "es7s.conf.d"))
        get_logger(False).warning(
            f"Dist(=default) config not found in user data dir, "
            f"loading from app data dir instead: '{dc_filepath}'"
        )
        return dc_filepath


def get_local_filepath() -> str:
    import click

    user_config_path = click.get_app_dir(APP_NAME)
    return path.join(user_config_path, f"{APP_NAME}.conf")


def get_merged(require=True) -> UserConfig | None:
    if not _merged_uconfig:
        if require:
            raise RuntimeError("Config is uninitialized")
        return None
    return _merged_uconfig


def get_dist() -> UserConfig | None:
    return _dist_uconfig


def init(params: UserConfigParams = None):
    global _dist_uconfig, _merged_uconfig
    dist_filepath = get_dist_filepath()
    local_filepath = get_local_filepath()

    if _dist_uconfig:
        _dist_uconfig.invalidate()
    _dist_uconfig = _make(dist_filepath)

    if not isfile(local_filepath):
        reset(False)

    filepaths = [dist_filepath]
    if params and not params.default:
        filepaths += [local_filepath]

    if _merged_uconfig:
        _merged_uconfig.invalidate()
    _merged_uconfig = _make(*filepaths, params=params)


def _make(*filepaths: str, params: UserConfigParams = None) -> UserConfig:
    uconfig = UserConfig(params)
    read_ok = uconfig.read(filepaths)
    get_logger().info("Reading configs files from: " + ", ".join(f'"{fp}"' for fp in filepaths))

    if len(read_ok) != len(filepaths):
        read_failed = set(filepaths) - set(read_ok)
        get_logger().warning("Failed to read config(s): " + ", ".join(read_failed))
    if len(read_ok) == 0:
        raise RuntimeError(f"Failed to initialize config")
    return uconfig


def reset(backup: bool = True) -> str | None:
    """Return path to backup file, if any."""
    user_config_filepath = get_local_filepath()
    makedirs(dirname(user_config_filepath), exist_ok=True)
    get_logger().debug(f'Making default config in: "{user_config_filepath}"')

    user_backup_filepath = None
    if backup and os.path.exists(user_config_filepath):
        user_backup_filepath = user_config_filepath + ".bak"
        os.rename(user_config_filepath, user_backup_filepath)
        get_logger().info(f'Original file renamed to: "{user_backup_filepath}"')

    header = True
    with open(user_config_filepath, "wt") as user_cfg:
        with open(get_dist_filepath(), "rt") as default_cfg:
            for idx, line in enumerate(default_cfg.readlines()):
                if header and line.startswith(("#", ";", "\n")):
                    continue  # remove default config header comments
                header = False

                if line.startswith(("#", "\n")):  # remove section separators
                    continue  # and empty lines
                elif line.startswith("["):  # keep section definitions, and
                    if user_cfg.tell():  # prepend the first one with a newline
                        line = "\n" + line
                elif line.startswith("syntax-version"):  # keep syntax-version
                    pass
                elif line.startswith(";"):  # keep examples, triple-comment out to distinguish
                    line = "###" + line.removeprefix(";")
                else:  # keep default values as commented out examples
                    line = "# " + line

                user_cfg.write(line)
                get_logger().trace(line.strip(), f"{idx+1}| ")

    return user_backup_filepath


def rewrite_value(section: str, option: str, value: str | None) -> None:
    local_filepath = get_local_filepath()
    source_uconfig = _make(local_filepath)

    if not source_uconfig.has_section(section):
        source_uconfig.add_section(section)
    source_uconfig._set(section, option, value)  # noqa

    get_logger().debug(f'Writing config to: "{local_filepath}"')
    with open(local_filepath, "wt") as user_cfg:
        source_uconfig.write(user_cfg)

    init(_merged_uconfig.params)

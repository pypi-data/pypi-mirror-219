# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import typing as t  # noqa

from . import *
from .._base import CliBaseCommand
from .._base_opts_params import CMDTYPE_EXTERNAL
from .._foreign import ForeignCommand
from ...shared.path import get_config_yaml


class _ExternalCommandFactory:
    @staticmethod
    def make_all() -> t.Iterable[CliBaseCommand]:
        for name, cfg in get_config_yaml('cmd-external').get('commands').items():
            yield ForeignCommand(cfg.pop('target'), cfg, CMDTYPE_EXTERNAL)


autodiscover_extras = _ExternalCommandFactory.make_all

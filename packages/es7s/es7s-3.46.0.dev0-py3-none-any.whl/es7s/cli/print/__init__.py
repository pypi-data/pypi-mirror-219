# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
from . import _static
from . import *  # noqa

autodiscover_extras = _static.StaticCommandFactory().make_all

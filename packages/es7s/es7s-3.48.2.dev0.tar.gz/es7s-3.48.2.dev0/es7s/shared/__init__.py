# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2022-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------

from .color import get_color
from .uconfig import (
    UserConfigParams,
    get_merged as get_merged_uconfig,
    get_dist as get_dist_uconfig,
    init as init_config,
    reset as reset_config,
)
from .dto import SocketMessage, BatteryInfo, DockerStatus, WeatherInfo
from .exception import (
    SubprocessExitCodeError,
    ExecutableNotFoundError,
    DataCollectionError,
    ArgCountError,
    NotInitializedError,
)
from .io import (
    IoParams,
    IoProxy,
    get_stdout,
    get_stderr,
    init_io,
    destroy_io,
)
from .ipc import SocketServer, SocketClient
from .log import (
    LoggerParams,
    Logger,
    get_logger,
    init_logger,
    destroy_logger,
    format_attrs,
)
from .path import (
    SHELL_PATH,
    ENV_PATH,
    GIT_PATH,
    RESOURCE_PACKAGE,
    USER_ES7S_BIN_DIR,
    USER_ES7S_DATA_DIR,
    USER_XBINDKEYS_RC_FILE,
    SHELL_COMMONS_FILE,
    get_config_yaml,
)
from .styles import Styles, FrozenStyle
from .threads import (
    ShutdownableThread,
    shutdown as shutdown_threads,
    shutdown_started,
)
from .demo import DemoHilightNumText
from .sub import run_subprocess, stream_subprocess, stream_pipe, run_detached
from .separator import UNIT_SEPARATOR
from .spinner import SpinnerBrailleSquareCenter
from .sun_calc import SunCalc
from .weather_icons import justify_wicon, get_wicon

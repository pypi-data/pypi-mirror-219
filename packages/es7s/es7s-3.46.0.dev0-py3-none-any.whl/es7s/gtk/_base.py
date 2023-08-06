# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import importlib.resources
import os
import pickle
import threading as th
import time
import typing as t
from abc import ABC, abstractmethod
from collections import OrderedDict, deque
from dataclasses import dataclass, field
from pathlib import Path
from typing import ClassVar

from es7s.shared import (
    RESOURCE_PACKAGE,
    ShutdownableThread,
    SocketClient,
    SocketMessage,
    format_attrs,
    get_logger,
    get_merged_uconfig,
)
from es7s.shared.ipc import IClientIPC
from es7s.shared.uconfig import rewrite_value
from . import AppIndicator, gi

DT = t.TypeVar("DT")

WAIT_PLACEHOLDER = ""  # "…"
_DEFAULT_TITLE = object()


@dataclass(frozen=True, eq=True)
class Notification:
    msg: str


@dataclass
class IndicatorUnboundState:
    abs_running_time_sec: float = 0
    tick_update_num: int = 0
    tick_render_num: int = 0
    timeout: int = 0
    wait_timeout: int = 0
    notify_timeout: int = 0
    notify_enqueue_timeout: int = 0
    notification_queue: deque[Notification] = deque()

    def __repr__(self):
        parts = (
            f"Å={self.abs_running_time_sec:.1f}",
            f"U={self.tick_update_num}",
            f"R={self.tick_render_num}",
            f"T={self.timeout:.1f}",
            f"W={self.wait_timeout:.1f}",
            f"N={self.notify_timeout:.1f}({len(self.notification_queue):d})",
            f"NQ={self.notify_enqueue_timeout:.1f}",
        )
        return f"{self.__class__.__qualname__}[{' '.join(parts)}]"

    @property
    def warning_switch(self) -> bool:
        return self.tick_update_num % 2 == 0

    @property
    def is_waiting(self) -> bool:
        return self.wait_timeout > 0

    def cancel_wait(self):
        self.wait_timeout = 0

    def log(self):
        get_logger().trace(repr(self), "State")


@dataclass
class _State:
    active = False
    gobject: gi.repository.Gtk.MenuItem = None
    gconfig: 'MenuItemConfig' = None

    @abstractmethod
    def click(self):
        ...


@dataclass
class _StaticState(_State):
    callback: t.Callable[[_State], None] = None

    def click(self):
        if self.callback:
            self.callback(self)

    def update_title(self, title: str):
        if not self.gobject:
            return
        self.gobject.set_label(title)


@dataclass
class _BoolState(_StaticState):
    value: bool = True
    config_var: tuple[str, str] = None  # (section, name)
    config_var_value: str = None  # for radios
    gobject: gi.repository.Gtk.CheckMenuItem | gi.repository.Gtk.RadioMenuItem = None

    def __post_init__(self):
        if self.config_var is not None and self.config_var[0]:
            uconfig = get_merged_uconfig()
            if self.config_var_value is None:
                self.value = uconfig.getboolean(*self.config_var)
            else:
                self.value = uconfig.get(*self.config_var) == self.config_var_value

    def __bool__(self):
        return self.value

    @property
    def active(self) -> bool:
        return self.value

    def click(self):
        self.value = not self.value
        self._update_config(self.value)
        super().click()

    def activate(self):
        if self.value:
            return
        self.gobject.set_active(True)

    def deactivate(self):
        if not self.value:
            return
        self.gobject.set_active(False)

    def _update_config(self, val: bool):
        if self.config_var is None:
            return
        if self.config_var_value is None:
            rewrite_value(*self.config_var, "on" if val else "off")
        else:
            if not val:
                return
            rewrite_value(*self.config_var, self.config_var_value)


@dataclass(frozen=True)
class MenuItemConfig:
    label: str
    sensitive: bool = True
    sep_before: bool = False

    def make(self, state: _State) -> gi.repository.Gtk.MenuItem:
        return gi.repository.Gtk.MenuItem.new_with_label(self.label)


@dataclass(frozen=True)
class CheckMenuItemConfig(MenuItemConfig):
    def make(self, state: _BoolState) -> gi.repository.Gtk.MenuItem:
        item = gi.repository.Gtk.CheckMenuItem.new_with_label(self.label)
        item.set_active(state.active)
        item.set_sensitive(self.sensitive)
        return item


@dataclass(frozen=True)
class RadioMenuItemConfig(MenuItemConfig):
    """
    Current implementation allows only one group.
    """

    group: str = ""

    def make(self, state: _BoolState) -> gi.repository.Gtk.MenuItem:
        item = gi.repository.Gtk.RadioMenuItem.new_with_label([], self.label)
        gi.repository.Gtk.RadioMenuItem.join_group(item, RadioMenuItemGroups.get(self.group))
        item.set_active(state.active)
        RadioMenuItemGroups.assign(self.group, item)
        return item


class RadioMenuItemGroups:
    _last: ClassVar[t.Dict[str, gi.repository.Gtk.RadioMenuItem]]

    @classmethod
    def get(cls, group: str) -> gi.repository.Gtk.RadioMenuItem | None:
        if not hasattr(cls, "_last"):
            return None
        return cls._last.get(group)

    @classmethod
    def assign(cls, group: str, item: gi.repository.Gtk.RadioMenuItem):
        if not hasattr(cls, "_last"):
            cls._last = dict()
        cls._last[group] = item


class SocketClientConn:
    SOCKRCV_INTERVAL_SEC = 1.0

    def __init__(self, socket_topic: str, indicator_name: str):
        self._socket_topic: str = socket_topic
        self._indicator_name: str = indicator_name
        self._monitor_data_buf: deque[bytes] = deque[bytes](maxlen=1)
        self._pause_event: th.Event = th.Event()
        self._ready_event: th.Event = th.Event()
        self._socket_client: SocketClient | None = None

        if not self._socket_topic:
            return
        self._socket_client = SocketClient(
            self._monitor_data_buf,
            eff_recv_interval_sec=self.SOCKRCV_INTERVAL_SEC,
            pause_event=self._pause_event,
            ready_event=self._ready_event,
            socket_topic=self._socket_topic,
            command_name=self._indicator_name,
        )

    @property
    def monitor_data_buf(self) -> deque[bytes]:
        return self._monitor_data_buf

    @property
    def pause_event(self) -> th.Event:
        return self._pause_event

    @property
    def ready_event(self) -> th.Event:
        return self._ready_event

    @property
    def socket_client(self) -> SocketClient | None:
        return self._socket_client


class _BaseIndicator(ShutdownableThread, t.Generic[DT], ABC):
    TICK_DURATION_SEC = 0.5

    RENDER_INTERVAL_SEC = 2.0
    RENDER_ERROR_TIMEOUT_SEC = 5.0
    NOTIFICATION_INTERVAL_SEC = 60.0
    NOTIFY_ENQUEUE_INTERVAL_SEC = 15.0

    APPINDICATOR_ID: str

    def __new__(cls, *args, **kwargs):
        inst = super().__new__(cls)
        inst._action_queue = deque()
        inst.config_section = None
        return inst

    def __init__(
        self,
        *,
        indicator_name: str,
        socket_topic: str | list[str] = None,
        icon_subpath: str = None,
        icon_name_default: str = None,
        icon_path_dynamic_tpl: str = None,
        icon_thresholds: list[int] = None,
        title: str = None,
        states: list[_State] = None,
        auto_visibility: bool = False,
    ):
        super().__init__(command_name=indicator_name, thread_name="ui")

        if not isinstance(socket_topic, list):
            socket_topic = [socket_topic]

        self._socket_client_conn: OrderedDict[str, SocketClientConn] = OrderedDict(
            {
                st: SocketClientConn(
                    socket_topic=st,
                    indicator_name=indicator_name,
                )
                for st in socket_topic
            }
        )

        self._theme_version = get_merged_uconfig().get("indicator", "theme-version")
        self._theme_path = importlib.resources.files(RESOURCE_PACKAGE).joinpath(
            Path("icons-v" + self._theme_version)
        )
        get_logger().debug(f"Theme resource path: '{self._theme_path}'")
        self._icon_name_default = icon_name_default
        self._icon_path_dynamic_tpl = icon_path_dynamic_tpl
        if icon_subpath:
            self._icon_name_default = os.path.join(icon_subpath, self._icon_name_default)
            self._icon_path_dynamic_tpl = os.path.join(icon_subpath, self._icon_path_dynamic_tpl)
        self._icon_thresholds = icon_thresholds
        self.title = title
        self._auto_visibility = auto_visibility

        self.public_hidden_state = th.Event()  # костыль

        if not self._auto_visibility:
            uconfig = get_merged_uconfig()
            display_config_val = None
            if uconfig.has_section(self.config_section):
                display_config_val = uconfig.getboolean(self.config_section, "display")
            initial_visibility = display_config_val is True
        else:
            initial_visibility = False

        if not initial_visibility:
            self.public_hidden_state.set()
        self._hidden = _BoolState(value=(not initial_visibility), callback=self._update_visibility)

        self._state_map = OrderedDict[MenuItemConfig, _State]()
        self._state_map.update(
            {
                CheckMenuItemConfig(
                    title or indicator_name,
                    sensitive=False,
                    sep_before=False,
                ): (title_state := _StaticState())
            }
        )
        self._title_state = title_state
        # self._state_map.update({CheckMenuItemConfig("Hide", separator_before=False): self._hidden})
        self._init_state(states)
        self.APPINDICATOR_ID = f"es7s-indicator-{indicator_name}"

        self._indicator: AppIndicator.Indicator = AppIndicator.Indicator.new(
            self.APPINDICATOR_ID,
            self._icon_name_default or "apport-symbolic",
            AppIndicator.IndicatorCategory.SYSTEM_SERVICES,
        )
        # ---------------------------↓--@debug-----------------------------
        def dbg(*args):
            get_logger().debug(
                "CONNECTION CHANGED: %s %s"
                % (args[0].get_property("connected"), format_attrs(str(a) for a in args)),
            )

        for ev in ["connection-changed"]:
            self._indicator.connect(ev, dbg)
        get_logger().debug("CONNECTED: %s" % self._indicator.get_property("connected"))
        # ---------------------------↑--@debug-----------------------------
        self._indicator.set_attention_icon("dialog-warning")
        self._indicator.set_icon_theme_path(str(self._theme_path))

        self._init_menu()
        self._update_visibility()

        gi.repository.Notify.init(self.APPINDICATOR_ID)
        for client in self._get_socket_clients():
            client.start()
        self.start()

    def _init_state(self, states: list[_State] = None):
        self._state = IndicatorUnboundState()
        get_logger().trace(f"{id(self._state):06x}", repr(self._state))

        if states:
            self._state_map.update({v.gconfig: v for v in states})

    def _init_menu(self):
        self._menu = gi.repository.Gtk.Menu()
        for config, state in self._state_map.items():
            self._make_menu_item(config, state)
        self._menu.show()
        self._indicator.set_menu(self._menu)

    def shutdown(self):
        super().shutdown()
        for client in self._get_socket_clients():
            client.shutdown()
        self._menu.hide()

    def _enqueue(self, fn: callable):
        self._action_queue.append(fn)

    def _make_menu_item(
        self, config: MenuItemConfig, state: _State = None
    ) -> gi.repository.Gtk.CheckMenuItem:
        if config.sep_before:
            sep = gi.repository.Gtk.SeparatorMenuItem.new()
            sep.show()
            self._menu.append(sep)

        item = config.make(state)
        item.connect("activate", lambda c=config: self._click_menu_item(config))
        item.show()
        self._menu.append(item)
        state.gobject = item

        return item

    def _click_menu_item(self, config: MenuItemConfig):
        if (state := self._state_map.get(config)) is not None:
            state.click()

    def _update_visibility(self, _: _State = None):
        if self._hidden:
            self._indicator.set_status(AppIndicator.IndicatorStatus.PASSIVE)
            self.public_hidden_state.set()
            if not self._auto_visibility:
                for scc in self._socket_client_conn.values():
                    scc.pause_event.set()
        else:
            self._indicator.set_status(AppIndicator.IndicatorStatus.ACTIVE)
            self.public_hidden_state.clear()
            if not self._auto_visibility:
                for scc in self._socket_client_conn.values():
                    scc.pause_event.clear()

    def run(self):
        super().run()

        if clients := [*self._get_socket_clients()]:
            sockrecvs = ", ".join(f"'{c.name}'" for c in clients)
            get_logger().info(f"Thread '{self.name}' waits for ({len(clients)}): {sockrecvs}")

        self._get_scc_current(rotate=True).ready_event.wait(self.TICK_DURATION_SEC)

        while True:
            self._on_before_update()
            if self.is_shutting_down():
                self.destroy()
                break
            self._notify()
            if self._state.timeout > self.TICK_DURATION_SEC:
                self._sleep(self.TICK_DURATION_SEC)
                continue
            self._sleep(self._state.timeout)

            if self.public_hidden_state.is_set() != self._hidden.value:
                self._hidden.click()

            try:
                act = self._action_queue.popleft()
            except IndexError:
                act = self._update
            act()

    def _sleep(self, timeout_sec: float):
        if timeout_sec == 0:
            return

        time.sleep(timeout_sec)
        self._state.abs_running_time_sec += timeout_sec
        self._state.timeout = max(0.0, self._state.timeout - timeout_sec)
        self._state.wait_timeout = max(0.0, self._state.wait_timeout - timeout_sec)
        self._state.notify_timeout = max(0.0, self._state.notify_timeout - timeout_sec)
        self._state.notify_enqueue_timeout = max(
            0.0, self._state.notify_enqueue_timeout - timeout_sec
        )
        self._state.log()

    def _add_timeout(self, timeout_sec: float = None):
        self._state.timeout += timeout_sec or self.RENDER_INTERVAL_SEC

    def _on_before_update(self):
        pass

    def _update(self):
        logger = get_logger()

        self._state.tick_update_num += 1
        if self._hidden.value and not self._auto_visibility:
            self._add_timeout()
            return

        monitor_data_buf = self._get_scc_current(rotate=True).monitor_data_buf
        try:
            try:
                msg_raw = monitor_data_buf[0]
            except IndexError:
                logger.warning("No data from daemon")
                self._add_timeout()
                self._render_no_data()
                return

            msg = self._deserialize(msg_raw)

            # msg_ttl = self._setup.message_ttl
            msg_ttl = 5.0  # @TODO
            now = time.time()

            if now - msg.timestamp > msg_ttl:
                monitor_data_buf.remove(msg_raw)
                raise RuntimeError(f"Expired socket message: {now} > {msg.timestamp}")

            else:
                # logger.trace(msg_raw, label="Received data dump")
                logger.debug("Deserialized changed message: " + repr(msg))
                self._add_timeout()
                self._state.tick_render_num += 1
                self._render(msg)

        except Exception as e:
            logger.exception(e)
            self._add_timeout(self.RENDER_ERROR_TIMEOUT_SEC)
            self._render_error()

    def _get_scc_current(self, *, rotate: bool) -> SocketClientConn | None:
        if len(self._socket_client_conn.keys()) == 0:
            return None
        first_key = [*self._socket_client_conn.keys()][0]
        if rotate:
            self._socket_client_conn.move_to_end(first_key)
        return self._socket_client_conn[first_key]

    def _get_socket_clients(self) -> t.Iterable[SocketClient]:
        for scc in self._socket_client_conn.values():
            if scc.socket_client:
                yield scc.socket_client

    def _deserialize(self, msg_raw: bytes) -> SocketMessage[DT]:
        msg = pickle.loads(msg_raw)
        return msg

    def _select_icon(self, carrier_value: float) -> str:
        if not self._icon_thresholds or not self._icon_path_dynamic_tpl:
            return self._icon_name_default

        icon_subtype = self._icon_thresholds[-1]
        for thr in self._icon_thresholds:
            icon_subtype = thr
            if carrier_value >= thr:
                break
        return self._icon_path_dynamic_tpl % icon_subtype

    @abstractmethod
    def _render(self, msg: SocketMessage[DT]):
        ...

    def _render_no_data(self):
        self._set(WAIT_PLACEHOLDER, None, AppIndicator.IndicatorStatus.ACTIVE)

    def _render_result(
        self, result: str, guide: str = None, warning: bool = False, icon: str = None
    ):
        # result = result.replace(' ', ' ')
        status = AppIndicator.IndicatorStatus.ACTIVE
        if warning and self._state.warning_switch:
            status = AppIndicator.IndicatorStatus.ATTENTION
        self._set(result, guide, status)

        if icon:
            get_logger().trace(icon, "SET Icon")
            self._indicator.set_icon_full(os.path.join(self._theme_path / icon), icon)

    def _render_error(self):
        self._set("ERR", None, AppIndicator.IndicatorStatus.ATTENTION)

    def _update_title(self, text: str, title: str = _DEFAULT_TITLE):
        if not isinstance(title, str):
            title = self.title
        self._title_state.update_title(title + "\t" + text)

    def _set(self, label: str, guide: str | None, status: AppIndicator.IndicatorStatus):
        if self._hidden:
            return
        logger = get_logger()
        logger.trace(label, "SET Label")
        logger.trace(status.value_name, "SET Status")

        if get_merged_uconfig().get_indicator_debug_mode():
            label = label.replace(" ", "␣")
        self._indicator.set_label(label, guide or label)
        self._indicator.set_status(status)

    def _enqueue_notification(self, msg: str) -> None:
        ...  # @TODO
        # if not self._state.notify_enqueue_timeout:
        #     self._state.notify_enqueue_timeout += self.NOTIFY_ENQUEUE_INTERVAL_SEC
        #     get_logger().trace(str(self._state.notify_enqueue_timeout), "ADD notify_enqueue_timeout")
        #     new = Notification(msg)
        #     for ex in self._state.notification_queue:
        #         if ex == new:
        #             return
        #     self._state.notification_queue.append(Notification(msg))
        #     get_logger().trace(msg, "ENQUEUE")

    def _notify(self) -> None:
        ...  # @TODO
        # if not self._state.notify_timeout and len(self._state.notification_queue):
        #     self._state.notify_timeout += self.NOTIFICATION_INTERVAL_SEC
        #     get_logger().trace(str(self._state.notify_timeout), "ADD notify_timeout")
        #
        #     notification = self._state.notification_queue.popleft()
        #     gi.repository.Notify.Notification.new(
        #         self.APPINDICATOR_ID,
        #         notification.msg,
        #         None
        #     ).show()
        #     get_logger().trace(notification.msg, "NOTIFY")

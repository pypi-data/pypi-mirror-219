import logging
from typing import TYPE_CHECKING, Literal, Optional

from .. import hookimpl, util
from ..types import Status
from . import (
    daemon_reload,
    disable,
    enable,
    get_property,
    install,
    installed,
    restart,
    start,
    stop,
    uninstall,
)

if TYPE_CHECKING:
    from ..ctx import Context
    from ..pm import PluginManager
    from ..settings import Settings


logger = logging.getLogger(__name__)


def register_if(settings: "Settings") -> bool:
    return settings.service_manager == "systemd"


def unit(service: str, qualname: Optional[str]) -> str:
    if qualname is not None:
        return f"pglift-{service}@{qualname}.service"
    else:
        return f"pglift-{service}.service"


@hookimpl
def enable_service(ctx: "Context", service: str, name: Optional[str]) -> Literal[True]:
    enable(ctx, unit(service, name))
    return True


@hookimpl
def disable_service(
    ctx: "Context", service: str, name: Optional[str], now: Optional[bool]
) -> Literal[True]:
    kwargs = {}
    if now is not None:
        kwargs["now"] = now
    disable(ctx, unit(service, name), **kwargs)
    return True


@hookimpl
def start_service(ctx: "Context", service: str, name: Optional[str]) -> Literal[True]:
    start(ctx, unit(service, name))
    return True


@hookimpl
def stop_service(ctx: "Context", service: str, name: Optional[str]) -> Literal[True]:
    stop(ctx, unit(service, name))
    return True


@hookimpl
def restart_service(ctx: "Context", service: str, name: Optional[str]) -> Literal[True]:
    restart(ctx, unit(service, name))
    return True


@hookimpl
def service_status(ctx: "Context", service: str, name: Optional[str]) -> Status:
    _, status = get_property(ctx, unit(service, name), "ActiveState").split("=", 1)
    status = status.strip()
    return Status.running if status == "active" else Status.not_running


@hookimpl
def site_configure_install(
    settings: "Settings", pm: "PluginManager", header: str, env: Optional[str]
) -> None:
    systemd_settings = settings.systemd
    assert systemd_settings is not None
    for outcome in pm.hook.systemd_unit_templates(
        settings=settings, env=env, content=True
    ):
        for name, content in outcome:
            install(name, util.with_header(content, header), systemd_settings)
    daemon_reload(systemd_settings)


@hookimpl
def site_configure_uninstall(settings: "Settings", pm: "PluginManager") -> None:
    systemd_settings = settings.systemd
    assert systemd_settings is not None
    for outcome in pm.hook.systemd_unit_templates(
        settings=settings, env=None, content=False
    ):
        for name in outcome:
            uninstall(name, systemd_settings)
    daemon_reload(systemd_settings)


@hookimpl
def site_configure_installed(settings: "Settings", pm: "PluginManager") -> bool:
    systemd_settings = settings.systemd
    assert systemd_settings is not None
    broken = False
    for outcome in pm.hook.systemd_unit_templates(
        settings=settings, env=None, content=False
    ):
        for name in outcome:
            if not installed(name, systemd_settings):
                logger.error("missing systemd unit '%s'", name)
                broken = True
    return not broken

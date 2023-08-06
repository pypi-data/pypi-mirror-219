import logging
import sys
from collections.abc import Iterator
from typing import TYPE_CHECKING, Optional, Union

from . import hookimpl, systemd
from .models import system
from .pgbackrest import repo_path

if TYPE_CHECKING:
    from .ctx import Context
    from .models import interface
    from .settings import Settings


logger = logging.getLogger(__name__)
service_name = "backup"
BACKUP_SERVICE_NAME = "pglift-backup@.service"
BACKUP_TIMER_NAME = "pglift-backup@.timer"


def register_if(settings: "Settings") -> bool:
    return (
        settings.service_manager == "systemd"
        and settings.scheduler == "systemd"
        and settings.pgbackrest is not None
        and repo_path.register_if(settings)
    )


@hookimpl
def systemd_unit_templates(
    settings: "Settings", env: Optional[str], content: bool
) -> Union[Iterator[str], Iterator[tuple[str, str]]]:
    if not content:
        yield BACKUP_SERVICE_NAME
        yield BACKUP_TIMER_NAME
        return

    environment = ""
    if env:
        environment = f"\nEnvironment={env}\n"
    if getattr(sys, "frozen", False):
        execpath = sys.executable
    else:
        execpath = f"{sys.executable} -m pglift"
    yield BACKUP_SERVICE_NAME, systemd.template(BACKUP_SERVICE_NAME).format(
        executeas=systemd.executeas(settings),
        environment=environment,
        execpath=execpath,
    )
    yield BACKUP_TIMER_NAME, systemd.template(BACKUP_TIMER_NAME)


@hookimpl
def instance_configured(ctx: "Context", manifest: "interface.Instance") -> None:
    """Enable scheduled backup job for configured instance."""
    instance = system.Instance.system_lookup(
        (manifest.name, manifest.version, ctx.settings)
    )
    ctx.hook.schedule_service(ctx=ctx, service=service_name, name=instance.qualname)


@hookimpl
def instance_dropped(ctx: "Context", instance: system.Instance) -> None:
    """Disable scheduled backup job when instance is being dropped."""
    ctx.hook.unschedule_service(
        ctx=ctx, service=service_name, name=instance.qualname, now=True
    )


@hookimpl
def instance_started(ctx: "Context", instance: system.Instance) -> None:
    """Start schedule backup job at instance startup."""
    ctx.hook.start_timer(ctx=ctx, service=service_name, name=instance.qualname)


@hookimpl
def instance_stopped(ctx: "Context", instance: system.Instance) -> None:
    """Stop schedule backup job when instance is stopping."""
    ctx.hook.stop_timer(ctx=ctx, service=service_name, name=instance.qualname)

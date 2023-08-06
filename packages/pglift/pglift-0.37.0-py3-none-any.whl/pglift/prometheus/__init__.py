import logging
from collections.abc import Iterator
from typing import TYPE_CHECKING, Any, Optional, Union

from pydantic import Field

from .. import hookimpl
from .. import service as service_mod
from .. import systemd
from ..models import interface
from ..types import Status
from . import impl, models
from .impl import apply as apply
from .impl import available as available
from .impl import get_settings
from .impl import start as start
from .impl import stop as stop
from .models import PostgresExporter as PostgresExporter
from .models import ServiceManifest

if TYPE_CHECKING:
    import click
    from pgtoolkit.conf import Configuration

    from ..ctx import Context
    from ..models import system
    from ..settings import Settings

__all__ = ["PostgresExporter", "apply", "available", "start", "stop"]

logger = logging.getLogger(__name__)


def register_if(settings: "Settings") -> bool:
    return available(settings) is not None


@hookimpl
def system_lookup(instance: "system.PostgreSQLInstance") -> Optional[models.Service]:
    settings = get_settings(instance._settings)
    return impl.system_lookup(instance.qualname, settings)


@hookimpl
def interface_model() -> tuple[str, Any, Any]:
    return (
        models.ServiceManifest.__service__,
        models.ServiceManifest,
        Field(
            default=models.ServiceManifest(),
            description="Configuration for the Prometheus service, if enabled in site settings.",
        ),
    )


@hookimpl
def get(instance: "system.Instance") -> Optional[models.ServiceManifest]:
    try:
        s = instance.service(models.Service)
    except ValueError:
        return None
    else:
        return models.ServiceManifest(port=s.port, password=s.password)


SYSTEMD_SERVICE_NAME = "pglift-postgres_exporter@.service"


@hookimpl
def systemd_unit_templates(
    settings: "Settings", content: bool
) -> Union[Iterator[str], Iterator[tuple[str, str]]]:
    if not content:
        yield SYSTEMD_SERVICE_NAME
        return
    s = get_settings(settings)
    configpath = str(s.configpath).replace("{name}", "%i")
    yield SYSTEMD_SERVICE_NAME, systemd.template(SYSTEMD_SERVICE_NAME).format(
        executeas=systemd.executeas(settings),
        configpath=configpath,
        execpath=s.execpath,
    )


@hookimpl
def instance_configured(
    ctx: "Context", manifest: "interface.Instance", config: "Configuration"
) -> None:
    """Install postgres_exporter for an instance when it gets configured."""
    settings = get_settings(ctx.settings)
    impl.setup_local(ctx, manifest, settings, config)


@hookimpl
def instance_started(ctx: "Context", instance: "system.Instance") -> None:
    """Start postgres_exporter service."""
    try:
        service = instance.service(models.Service)
    except ValueError:
        return
    impl.start(ctx, service)


@hookimpl
def instance_stopped(ctx: "Context", instance: "system.Instance") -> None:
    """Stop postgres_exporter service."""
    try:
        service = instance.service(models.Service)
    except ValueError:
        return
    impl.stop(ctx, service)


@hookimpl
def instance_dropped(ctx: "Context", instance: "system.Instance") -> None:
    """Uninstall postgres_exporter from an instance being dropped."""
    settings = get_settings(ctx.settings)
    impl.revert_setup(ctx, instance.qualname, settings)


@hookimpl
def role(
    settings: "Settings", manifest: "interface.Instance"
) -> Optional[interface.Role]:
    service_manifest = manifest.service_manifest(ServiceManifest)
    assert settings.prometheus is not None
    return interface.Role(
        name=settings.prometheus.role,
        password=service_manifest.password,
        login=True,
        in_roles=["pg_monitor"],
    )


@hookimpl
def cli() -> "click.Group":
    from .cli import postgres_exporter

    return postgres_exporter


@hookimpl
def instance_status(
    ctx: "Context", instance: "system.Instance"
) -> Optional[tuple[Status, str]]:
    try:
        service = instance.service(models.Service)
    except ValueError:
        return None
    return (service_mod.status(ctx, service), "prometheus")

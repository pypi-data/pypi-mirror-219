import logging
import shlex
from pathlib import Path
from typing import TYPE_CHECKING, Any, Literal, Optional

import pgtoolkit.conf as pgconf
from pydantic import Field
from pydantic.fields import FieldInfo

from .. import cmd, hookimpl, util
from ..models import interface, system
from . import base, models
from .base import available as available
from .base import get_settings as get_settings
from .base import iter_backups as iter_backups
from .base import restore as restore
from .models import ServiceManifest

if TYPE_CHECKING:
    import click

    from ..ctx import Context
    from ..settings import PgBackRestSettings, Settings


__all__ = ["available", "backup", "iter_backups", "restore"]

logger = logging.getLogger(__name__)


def register_if(settings: "Settings") -> bool:
    return available(settings) is not None


def dirs(settings: "PgBackRestSettings") -> list[Path]:
    return [
        settings.lockpath,
        settings.logpath,
        settings.spoolpath,
    ]


@hookimpl
def site_configure_install(settings: "Settings") -> None:
    logger.info("creating common pgbackrest directories")
    s = get_settings(settings)
    for d in dirs(s):
        d.mkdir(exist_ok=True, parents=True)


@hookimpl
def site_configure_uninstall(settings: "Settings") -> None:
    logger.info("deleting common pgbackrest directories")
    s = get_settings(settings)
    for d in dirs(s):
        util.rmdir(d)


@hookimpl
def site_configure_installed(settings: "Settings") -> bool:
    s = get_settings(settings)
    broken = False
    for d in dirs(s):
        if not d.exists():
            logger.error("pgBackRest directory '%s' not found", d)
            broken = True
    return not broken


@hookimpl
def system_lookup(instance: "system.PostgreSQLInstance") -> Optional[models.Service]:
    settings = get_settings(instance._settings)
    return base.system_lookup(instance.datadir, settings)


@hookimpl
def get(instance: "system.Instance") -> Optional[models.ServiceManifest]:
    try:
        s = instance.service(models.Service)
    except ValueError:
        return None
    else:
        return models.ServiceManifest(stanza=s.stanza)


@hookimpl
def instance_settings(
    ctx: "Context", manifest: "interface.Instance", instance: "system.BaseInstance"
) -> pgconf.Configuration:
    settings = get_settings(ctx.settings)
    service_manifest = manifest.service_manifest(ServiceManifest)
    return base.postgresql_configuration(
        service_manifest.stanza, settings, instance.datadir
    )


@hookimpl
def interface_model() -> tuple[str, Any, FieldInfo]:
    return (
        models.ServiceManifest.__service__,
        models.ServiceManifest,
        Field(
            required=True,
            readOnly=True,
            description="Configuration for the pgBackRest service, if enabled in site settings.",
        ),
    )


def initdb_restore_command(
    instance: "system.BaseInstance", manifest: "interface.Instance"
) -> Optional[list[str]]:
    settings = get_settings(instance._settings)
    service_manifest = manifest.service_manifest(ServiceManifest)
    service = base.service(instance, service_manifest, settings, None)
    if not base.backup_info(service, settings)["backup"]:
        return None
    cmd_args = [
        str(settings.execpath),
        "--log-level-file=off",
        "--log-level-stderr=info",
        "--config-path",
        str(settings.configpath),
        "--stanza",
        service_manifest.stanza,
        "--pg1-path",
        str(instance.datadir),
    ]
    if manifest.standby:
        cmd_args.append("--type=standby")
        # Double quote if needed (e.g. to escape white spaces in value).
        value = manifest.standby.full_primary_conninfo.replace("'", "''")
        cmd_args.extend(["--recovery-option", f"primary_conninfo={value}"])
        if manifest.standby.slot:
            cmd_args.extend(
                ["--recovery-option", f"primary_slot_name={manifest.standby.slot}"]
            )
    cmd_args.append("restore")
    return cmd_args


@hookimpl
def patroni_create_replica_method(
    manifest: "interface.Instance", instance: system.BaseInstance
) -> Optional[tuple[str, dict[str, Any]]]:
    if (args := initdb_restore_command(instance, manifest)) is None:
        return None
    return "pgbackrest", {
        "command": shlex.join(args),
        "keep_data": True,
        "no_params": True,
    }


@hookimpl
def initdb(
    ctx: "Context", manifest: "interface.Instance", instance: system.BaseInstance
) -> Optional[Literal[True]]:
    if (args := initdb_restore_command(instance, manifest)) is None:
        return None
    logger.info("restoring from a pgBackRest backup")
    cmd.run(args, check=True)
    return True


@hookimpl
def instance_promoted(ctx: "Context", instance: system.Instance) -> None:
    if service_manifest := get(instance):
        settings = get_settings(instance._settings)
        service = base.service(instance, service_manifest, settings, None)
        logger.info("checking pgBackRest configuration")
        base.check(ctx, instance, service, settings, None)


@hookimpl
def instance_env(ctx: "Context", instance: "system.Instance") -> dict[str, str]:
    pgbackrest_settings = base.get_settings(ctx.settings)
    try:
        service = instance.service(models.Service)
    except ValueError:
        return {}
    return base.env_for(service, pgbackrest_settings)


@hookimpl
def rolename(settings: "Settings") -> str:
    return settings.postgresql.backuprole.name


@hookimpl
def role(
    settings: "Settings", manifest: "interface.Instance"
) -> Optional["interface.Role"]:
    name = rolename(settings)
    service_manifest = manifest.service_manifest(ServiceManifest)
    extra = {}
    if settings.postgresql.auth.passfile is not None:
        extra["pgpass"] = settings.postgresql.backuprole.pgpass
    return interface.Role(
        name=name,
        password=service_manifest.password,
        login=True,
        superuser=True,
        **extra,
    )


@hookimpl
def logrotate_config(settings: "Settings") -> str:
    assert settings.logrotate is not None
    s = get_settings(settings)
    return util.template("pgbackrest", "logrotate.conf").format(logpath=s.logpath)


@hookimpl
def cli() -> "click.Command":
    from .cli import pgbackrest

    return pgbackrest


@hookimpl
def instance_cli(group: "click.Group") -> None:
    from .cli import instance_backups, instance_restore

    group.add_command(instance_backups)
    group.add_command(instance_restore)

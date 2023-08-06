import pathlib
from typing import Optional

import pytest

from pglift import exceptions
from pglift.models.system import Instance
from pglift.settings import Settings, TemboardSettings
from pglift.temboard import impl as temboard
from pglift.temboard import models, systemd_unit_templates


@pytest.fixture
def temboard_settings(settings: Settings) -> TemboardSettings:
    assert settings.temboard is not None
    return settings.temboard


def test_systemd_unit_templates(
    settings: Settings, temboard_execpath: Optional[pathlib.Path]
) -> None:
    assert temboard_execpath
    ((name, content),) = list(systemd_unit_templates(settings=settings, content=True))
    assert name == "pglift-temboard_agent@.service"
    lines = content.splitlines()
    assert (
        f"ExecStart={temboard_execpath} -c {settings.prefix}/etc/temboard-agent/temboard-agent-%i.conf"
        in lines
    )


def test_port(temboard_settings: TemboardSettings, instance: Instance) -> None:
    try:
        temboard_service = instance.service(models.Service)
    except ValueError:
        temboard_service = None
    if temboard_service:
        port = temboard.port(instance.qualname, temboard_settings)
        assert port == 2345
    else:
        with pytest.raises(exceptions.FileNotFoundError):
            temboard.port(instance.qualname, temboard_settings)

    configpath = pathlib.Path(
        str(temboard_settings.configpath).format(name=instance.qualname)
    )
    original_content = None
    if temboard_service:
        original_content = configpath.read_text()
    else:
        configpath.parent.mkdir(parents=True)  # exists not ok
    try:
        configpath.write_text("[empty section]\n")
        with pytest.raises(LookupError, match="port not found in temboard section"):
            temboard.port(instance.qualname, temboard_settings)
    finally:
        if original_content is not None:
            configpath.write_text(original_content)


def test_password(temboard_settings: TemboardSettings, instance: Instance) -> None:
    try:
        temboard_service = instance.service(models.Service)
    except ValueError:
        temboard_service = None
    if temboard_service:
        password = temboard.password(instance.qualname, temboard_settings)
        assert password == "dorade"
    else:
        with pytest.raises(exceptions.FileNotFoundError):
            temboard.password(instance.qualname, temboard_settings)

    configpath = pathlib.Path(
        str(temboard_settings.configpath).format(name=instance.qualname)
    )
    original_content = None
    if temboard_service:
        original_content = configpath.read_text()
    else:
        configpath.parent.mkdir(parents=True)  # exists not ok
    try:
        configpath.write_text("[postgresql]\n")
        assert temboard.password(instance.qualname, temboard_settings) is None
    finally:
        if original_content is not None:
            configpath.write_text(original_content)

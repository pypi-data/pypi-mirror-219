import sys

from pglift.backup import systemd_unit_templates
from pglift.settings import Settings


def test_systemd_unit_templates(settings: Settings) -> None:
    ((service_name, service_content), (timer_name, timer_content)) = list(
        systemd_unit_templates(settings, env="X-DEBUG=no", content=True)
    )
    assert service_name == "pglift-backup@.service"
    service_lines = service_content.splitlines()
    for line in service_lines:
        if line.startswith("ExecStart"):
            execstart = line.split("=", 1)[-1]
            assert execstart == f"{sys.executable} -m pglift instance backup %I"
            break
    else:
        raise AssertionError("ExecStart line not found")
    assert "Environment=X-DEBUG=no" in service_lines
    assert timer_name == "pglift-backup@.timer"
    timer_lines = timer_content.splitlines()
    assert "OnCalendar=daily" in timer_lines

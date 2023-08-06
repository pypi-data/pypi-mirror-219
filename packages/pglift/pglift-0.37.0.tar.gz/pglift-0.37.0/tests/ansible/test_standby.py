import json
import os
import pathlib
import subprocess
from collections.abc import Iterator
from typing import Callable

import psycopg
import pytest
import yaml


@pytest.fixture
def postgresql_socket_directory(tmp_path: pathlib.Path) -> pathlib.Path:
    return tmp_path / "pgsql"


@pytest.fixture
def site_settings(
    tmp_path: pathlib.Path,
    postgresql_socket_directory: pathlib.Path,
) -> Iterator[pathlib.Path]:
    settings = {
        "prefix": str(tmp_path),
        "postgresql": {
            "socket_directory": str(postgresql_socket_directory),
        },
    }
    settings_f = tmp_path / "config.json"
    with settings_f.open("w") as f:
        json.dump(settings, f)
    env = os.environ.copy() | {"SETTINGS": f"@{settings_f}"}
    subprocess.run(
        ["pglift", "--debug", "site-configure", "install"],
        capture_output=True,
        check=True,
        env=env,
    )
    yield settings_f
    subprocess.run(
        ["pglift", "--non-interactive", "--debug", "site-configure", "uninstall"],
        capture_output=True,
        check=True,
        env=env,
    )


@pytest.fixture
def call_playbook(
    tmp_path: pathlib.Path,
    site_settings: pathlib.Path,
    ansible_env: dict[str, str],
    ansible_vault: Callable[[dict[str, str]], pathlib.Path],
) -> Iterator[Callable[[pathlib.Path], None]]:
    vault = ansible_vault({"replication_role_password": "r3pl1c@t"})
    teardown_play = tmp_path / "teardown.yml"
    with teardown_play.open("w") as f:
        yaml.safe_dump(
            [
                {
                    "name": "teardown standby setup",
                    "hosts": "localhost",
                    "tasks": [
                        {
                            "name": "drop standby",
                            "dalibo.pglift.instance": {
                                "name": "pg2",
                                "state": "absent",
                            },
                        },
                        {
                            "name": "drop primary",
                            "dalibo.pglift.instance": {
                                "name": "pg1",
                                "state": "absent",
                            },
                        },
                    ],
                }
            ],
            f,
        )

    def call(playfile: pathlib.Path) -> None:
        subprocess.check_call(
            [
                "ansible-playbook",
                "--extra-vars",
                f"@{vault}",
                str(playfile),
            ],
            env=ansible_env.copy() | {"SETTINGS": f"@{site_settings}"},
        )

    yield call
    call(teardown_play)


def test(
    playdir: pathlib.Path,
    call_playbook: Callable[[pathlib.Path], None],
    postgresql_socket_directory: pathlib.Path,
) -> None:
    call_playbook(playdir / "standby-setup.yml")

    primary_conninfo = f"host={postgresql_socket_directory} user=replication password=r3pl1c@t dbname=postgres port=5433"
    with psycopg.connect(primary_conninfo) as conn:
        rows = conn.execute("SELECT * FROM pg_is_in_recovery()").fetchall()
    assert rows == [(True,)]

    call_playbook(playdir / "standby-promote.yml")

    primary_conninfo = f"host={postgresql_socket_directory} user=replication password=r3pl1c@t dbname=postgres port=5432"
    with psycopg.connect(primary_conninfo) as conn:
        rows = conn.execute("SELECT * FROM pg_is_in_recovery()").fetchall()
    assert rows == [(True,)]
    primary_conninfo = f"host={postgresql_socket_directory} user=postgres port=5433"
    with psycopg.connect(primary_conninfo) as conn:
        rows = conn.execute("SELECT * FROM pg_is_in_recovery()").fetchall()
    assert rows == [(False,)]

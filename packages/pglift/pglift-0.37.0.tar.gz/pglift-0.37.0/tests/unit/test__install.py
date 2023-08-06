import pytest

from pglift import _install
from pglift.pm import PluginManager
from pglift.settings import Settings


def test_check_uninstalled(pm: PluginManager, settings: Settings) -> None:
    assert not _install.check(pm, settings)


@pytest.mark.usefixtures("installed")
def test_check_installed(pm: PluginManager, settings: Settings) -> None:
    assert _install.check(pm, settings)

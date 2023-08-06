from pathlib import Path
from typing import Optional

from attrs import frozen
from pydantic import Field, SecretStr

from .. import types


@frozen
class Service:
    """A pgbackrest service bound to a PostgreSQL instance."""

    stanza: str
    """Name of the stanza"""

    path: Path
    """Path to configuration file for this stanza"""

    index: int = 1
    """index of pg-path option in the stanza"""


class ServiceManifest(types.ServiceManifest, service_name="pgbackrest"):
    stanza: str = Field(
        description=(
            "Name of pgBackRest stanza. "
            "Something describing the actual function of the instance, such as 'app'."
        ),
        readOnly=True,
    )
    password: Optional[SecretStr] = Field(
        default=None,
        description="Password of PostgreSQL role for pgBackRest.",
        exclude=True,
    )

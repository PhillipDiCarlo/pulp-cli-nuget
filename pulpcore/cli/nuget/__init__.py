import typing as t

import click
from pulp_cli.generic import pulp_group
from pulp_glue.common.i18n import get_translation
from pulp_glue.nuget.context import PulpNugetACSContext, PulpNugetRemoteContext
from pulpcore.cli.common.acs import acs_command

from pulpcore.cli.nuget.content import content
from pulpcore.cli.nuget.distribution import distribution
from pulpcore.cli.nuget.remote import remote
from pulpcore.cli.nuget.repository import repository

translation = get_translation(__package__)
_ = translation.gettext

__version__ = "0.1.0.dev"


@pulp_group(name="nuget")
def nuget_group() -> None:
    pass


def mount(main: click.Group, **kwargs: t.Any) -> None:
    nuget_group.add_command(repository)
    nuget_group.add_command(remote)
    nuget_group.add_command(distribution)
    nuget_group.add_command(content)
    nuget_group.add_command(
        acs_command(
            acs_contexts={"nuget": PulpNugetACSContext},
            remote_context_table={"nuget:nuget": PulpNugetRemoteContext},
        )
    )
    main.add_command(nuget_group)

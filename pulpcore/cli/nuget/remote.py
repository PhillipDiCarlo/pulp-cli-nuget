import typing as t

import click
import schema as s
from pulp_cli.generic import (
    common_remote_create_options,
    common_remote_update_options,
    create_command,
    destroy_command,
    href_option,
    json_callback,
    label_command,
    list_command,
    load_file_wrapper,
    name_option,
    pulp_group,
    remote_filter_options,
    remote_lookup_option,
    role_command,
    show_command,
    type_option,
    update_command,
)
from pulp_glue.common.i18n import get_translation
from pulp_glue.nuget.context import PulpNugetRemoteContext

translation = get_translation(__package__)
_ = translation.gettext

FILTER_LIST_SCHEMA = s.Schema([str])


@load_file_wrapper
def _filter_list_callback(ctx: click.Context, param: click.Parameter, value: str | None) -> t.Any:
    """Accept a JSON list of package filter entries (inline or @file)."""
    if value is None:
        return None
    result = json_callback(ctx, param, value)
    try:
        return FILTER_LIST_SCHEMA.validate(result)
    except s.SchemaError as e:
        raise click.ClickException(
            _("Validation of '{parameter}' failed: {error}").format(
                parameter=param.name, error=str(e)
            )
        )


@pulp_group()
@type_option(choices={"nuget": PulpNugetRemoteContext})
def remote() -> None:
    pass


lookup_options = [href_option, name_option, remote_lookup_option]
nested_lookup_options = [remote_lookup_option]
nuget_remote_options = [
    click.option("--policy", type=click.Choice(["immediate", "on_demand"], case_sensitive=False)),
    click.option(
        "--includes",
        callback=_filter_list_callback,
        help=_(
            "JSON list of packages to sync: package ids with optional NuGet version "
            """ranges, e.g. '["Serilog", "Newtonsoft.Json [13.0,14.0)"]'. The single """
            "entry '*' mirrors everything the upstream's search enumerates. The "
            "argument prefixed with '@' can be the path to a JSON file."
        ),
    ),
    click.option(
        "--excludes",
        callback=_filter_list_callback,
        help=_(
            "JSON list of packages to skip, in the same syntax as --includes. "
            "The argument prefixed with '@' can be the path to a JSON file."
        ),
    ),
]

remote.add_command(list_command(decorators=remote_filter_options))
remote.add_command(show_command(decorators=lookup_options))
remote.add_command(create_command(decorators=common_remote_create_options + nuget_remote_options))
remote.add_command(
    update_command(decorators=lookup_options + common_remote_update_options + nuget_remote_options)
)
remote.add_command(destroy_command(decorators=lookup_options))
remote.add_command(label_command(decorators=nested_lookup_options))
remote.add_command(role_command(decorators=lookup_options))

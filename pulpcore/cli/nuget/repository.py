import typing as t

import click
import schema as s
from pulp_cli.generic import (
    create_command,
    create_content_json_callback,
    destroy_command,
    href_option,
    label_command,
    label_select_option,
    list_command,
    name_option,
    option_group,
    pass_repository_context,
    pulp_group,
    pulp_labels_option,
    pulp_option,
    repository_content_command,
    repository_href_option,
    repository_lookup_option,
    resource_option,
    retained_versions_option,
    role_command,
    show_command,
    type_option,
    update_command,
    version_command,
)
from pulp_glue.common.context import (
    EntityFieldDefinition,
    PulpContentContext,
    PulpRemoteContext,
)
from pulp_glue.common.i18n import get_translation
from pulp_glue.nuget.context import (
    PulpNugetContentContext,
    PulpNugetRemoteContext,
    PulpNugetRepositoryContext,
    PulpNugetSymbolPackageContentContext,
)
from pulpcore.cli.core.generic import task_command

translation = get_translation(__package__)
_ = translation.gettext


remote_option = resource_option(
    "--remote",
    default_plugin="nuget",
    default_type="nuget",
    context_table={"nuget:nuget": PulpNugetRemoteContext},
    href_pattern=PulpRemoteContext.HREF_PATTERN,
    help=_("Remote used for syncing in the form '[[<plugin>:]<resource_type>:]<name>' or by href."),
)

CONTENT_LIST_SCHEMA = s.Schema([{"package_id": str, "version": str}])


@pulp_group()
@type_option(choices={"nuget": PulpNugetRepositoryContext})
def repository() -> None:
    pass


lookup_options = [href_option, name_option, repository_lookup_option]
nested_lookup_options = [repository_href_option, repository_lookup_option]
update_options = [
    click.option("--description"),
    remote_option,
    click.option(
        "--retain-package-versions",
        type=int,
        help=_(
            "Keep only this many versions of each package id in new repository versions "
            "(newest by NuGet precedence). 0 keeps all versions."
        ),
    ),
    retained_versions_option,
    pulp_labels_option,
]
create_options = update_options + [click.option("--name", required=True)]


def _content_callback(ctx: click.Context, value: dict[str, t.Any]) -> None:
    """Look the content unit up by package id and version, unless --href selects it."""
    if ctx.get_parameter_source("href") == click.core.ParameterSource.COMMANDLINE:
        raise click.UsageError(_("--href cannot be combined with --package-id and --version."))
    entity_ctx = ctx.find_object(PulpContentContext)
    assert entity_ctx is not None
    entity_ctx.entity = value


# A content unit is identified by its href, or by package id and version together.
content_options = [
    pulp_option("--package-id", help=_("Package id of the {entity} (case-insensitive).")),
    pulp_option("--version", help=_("NuGet-normalized version of the {entity}.")),
    option_group(
        "content", ["package_id", "version"], callback=_content_callback, expose_value=False
    ),
    href_option,
]
content_json_callback = create_content_json_callback(None, schema=CONTENT_LIST_SCHEMA)
modify_options = [
    pulp_option(
        "--add-content",
        callback=content_json_callback,
        help=_(
            """JSON string with a list of {entities} to add to the repository.
    Each {entity} must contain the following keys: "package_id", "version".
    The argument prefixed with the '@' can be the path to a JSON file with a list of {entities}."""
        ),
    ),
    pulp_option(
        "--remove-content",
        callback=content_json_callback,
        help=_(
            """JSON string with a list of {entities} to remove from the repository.
    Each {entity} must contain the following keys: "package_id", "version".
    The argument prefixed with the '@' can be the path to a JSON file with a list of {entities}."""
        ),
    ),
]

repository.add_command(
    list_command(
        decorators=[
            label_select_option,
            click.option("--name-startswith", "name__startswith"),
        ]
    )
)
repository.add_command(show_command(decorators=lookup_options))
repository.add_command(create_command(decorators=create_options))
repository.add_command(update_command(decorators=lookup_options + update_options))
repository.add_command(destroy_command(decorators=lookup_options))
repository.add_command(task_command(decorators=nested_lookup_options))
repository.add_command(version_command(decorators=nested_lookup_options))
repository.add_command(label_command(decorators=nested_lookup_options))
repository.add_command(role_command(decorators=lookup_options))
repository.add_command(
    repository_content_command(
        contexts={
            "package": PulpNugetContentContext,
            "symbol-package": PulpNugetSymbolPackageContentContext,
        },
        add_decorators=content_options,
        remove_decorators=content_options,
        modify_decorators=modify_options,
        base_default_plugin="nuget",
        base_default_type="nuget",
    )
)


@repository.command()
@name_option
@href_option
@repository_lookup_option
@remote_option
@click.option("--mirror/--no-mirror", default=None)
@click.option(
    "--optimize/--no-optimize",
    default=None,
    help=_("Skip the sync when the remote and the upstream are unchanged (default: optimize)."),
)
@pass_repository_context
def sync(
    repository_ctx: PulpNugetRepositoryContext,
    /,
    remote: EntityFieldDefinition,
    mirror: bool | None,
    optimize: bool | None,
) -> None:
    """
    Sync the repository from a remote source.

    If remote is not specified, sync uses the default remote associated with the
    repository.
    """
    body: dict[str, t.Any] = {}
    repository = repository_ctx.entity
    if mirror is not None:
        body["mirror"] = mirror
    if optimize is not None:
        body["optimize"] = optimize

    if remote:
        body["remote"] = remote
    elif repository["remote"] is None:
        raise click.ClickException(
            _(
                "Repository '{name}' does not have a default remote. "
                "Please specify with '--remote'."
            ).format(name=repository["name"])
        )

    repository_ctx.sync(body=body)

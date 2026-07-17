import typing as t

import click
from pulp_cli.generic import (
    create_command,
    destroy_command,
    href_option,
    label_command,
    label_select_option,
    list_command,
    name_option,
    pass_repository_context,
    pulp_group,
    pulp_labels_option,
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
from pulp_glue.common.context import EntityFieldDefinition, PulpRemoteContext
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
content_hrefs_options = [
    click.option("--href", help=_("Href of the nuget package/symbol package to use"))
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
        base_default_plugin="nuget",
        base_default_type="package",
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

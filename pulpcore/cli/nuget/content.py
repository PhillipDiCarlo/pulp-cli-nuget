import typing as t

import click
from pulp_cli.generic import (
    PulpCLIContext,
    chunk_size_option,
    content_filter_options,
    href_option,
    list_command,
    pass_entity_context,
    pass_pulp_context,
    pulp_group,
    resource_option,
    show_command,
    type_option,
)
from pulp_glue.common.context import PulpContentContext, PulpRepositoryContext
from pulp_glue.common.i18n import get_translation
from pulp_glue.nuget.context import (
    PulpNugetContentContext,
    PulpNugetRepositoryContext,
    PulpNugetSymbolPackageContentContext,
)

translation = get_translation(__package__)
_ = translation.gettext


repository_option = resource_option(
    "--repository",
    default_plugin="nuget",
    default_type="nuget",
    context_table={"nuget:nuget": PulpNugetRepositoryContext},
    href_pattern=PulpRepositoryContext.HREF_PATTERN,
    help=_(
        "Repository to add the content to in the form '[[<plugin>:]<resource_type>:]<name>' or by "
        "href."
    ),
)


@pulp_group()
@type_option(
    choices={
        "package": PulpNugetContentContext,
        "symbol-package": PulpNugetSymbolPackageContentContext,
    },
    default="package",
)
def content() -> None:
    pass


list_options = [
    click.option("--package-id", "package_id", help=_("Filter by package id (case-insensitive)")),
    click.option("--version", help=_("Filter by NuGet-normalized version")),
    *content_filter_options,
]

content.add_command(list_command(decorators=list_options))
content.add_command(show_command(decorators=[href_option]))


@content.command()
@click.option(
    "--file",
    type=click.File("rb"),
    required=True,
    help=_("The .nupkg (or .snupkg for --type=symbol-package) file to upload"),
)
@chunk_size_option
@repository_option
@pass_entity_context
@pass_pulp_context
def upload(
    pulp_ctx: PulpCLIContext,
    entity_ctx: PulpContentContext,
    /,
    file: t.IO[bytes],
    chunk_size: int,
    repository: PulpRepositoryContext | None,
) -> None:
    """
    Create a nuget content unit by uploading a package file.

    All metadata is parsed server-side from the manifest inside the package.
    """
    result = entity_ctx.upload(file=file, chunk_size=chunk_size, repository=repository)
    pulp_ctx.output_result(result)

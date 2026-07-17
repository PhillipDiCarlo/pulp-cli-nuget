import click
from pulp_cli.generic import (
    common_distribution_create_options,
    content_guard_option,
    create_command,
    destroy_command,
    distribution_filter_options,
    distribution_lookup_option,
    href_option,
    label_command,
    list_command,
    name_option,
    pulp_group,
    pulp_labels_option,
    resource_option,
    role_command,
    show_command,
    type_option,
    update_command,
)
from pulp_glue.common.i18n import get_translation
from pulp_glue.nuget.context import PulpNugetDistributionContext, PulpNugetRepositoryContext

translation = get_translation(__package__)
_ = translation.gettext


repository_option = resource_option(
    "--repository",
    default_plugin="nuget",
    default_type="nuget",
    context_table={"nuget:nuget": PulpNugetRepositoryContext},
    href_pattern=PulpNugetRepositoryContext.HREF_PATTERN,
    help=_(
        "Repository whose latest version is served by the distribution."
        " Specified as '[[<plugin>:]<type>:]<name>' or as href."
    ),
)


@pulp_group()
@type_option(choices={"nuget": PulpNugetDistributionContext})
def distribution() -> None:
    pass


lookup_options = [href_option, name_option, distribution_lookup_option]
nested_lookup_options = [distribution_lookup_option]
update_options = [
    repository_option,
    content_guard_option,
    pulp_labels_option,
]
create_options = common_distribution_create_options + update_options

distribution.add_command(list_command(decorators=distribution_filter_options))
distribution.add_command(show_command(decorators=lookup_options))
distribution.add_command(create_command(decorators=create_options))
distribution.add_command(
    update_command(decorators=lookup_options + update_options + [click.option("--base-path")])
)
distribution.add_command(destroy_command(decorators=lookup_options))
distribution.add_command(label_command(decorators=nested_lookup_options))
distribution.add_command(role_command(decorators=lookup_options))

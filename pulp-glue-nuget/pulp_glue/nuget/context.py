from pulp_glue.common.context import (
    PluginRequirement,
    PulpACSContext,
    PulpContentContext,
    PulpDistributionContext,
    PulpRemoteContext,
    PulpRepositoryContext,
    PulpRepositoryVersionContext,
)
from pulp_glue.common.i18n import get_translation

translation = get_translation(__package__)
_ = translation.gettext


class PulpNugetACSContext(PulpACSContext):
    PLUGIN = "nuget"
    RESOURCE_TYPE = "nuget"
    ENTITY = _("nuget ACS")
    ENTITIES = _("nuget ACSes")
    HREF = "nuget_nuget_alternate_content_source_href"
    ID_PREFIX = "acs_nuget_nuget"
    NEEDS_PLUGINS = [PluginRequirement("nuget")]
    CAPABILITIES = {"roles": [PluginRequirement("nuget")]}


class PulpNugetContentContext(PulpContentContext):
    PLUGIN = "nuget"
    RESOURCE_TYPE = "package"
    ENTITY = _("nuget package")
    ENTITIES = _("nuget packages")
    HREF = "nuget_nuget_package_content_href"
    ID_PREFIX = "content_nuget_packages"
    NEEDS_PLUGINS = [PluginRequirement("nuget")]
    CAPABILITIES = {"upload": []}


class PulpNugetSymbolPackageContentContext(PulpContentContext):
    PLUGIN = "nuget"
    RESOURCE_TYPE = "symbol_package"
    ENTITY = _("nuget symbol package")
    ENTITIES = _("nuget symbol packages")
    HREF = "nuget_nuget_symbol_package_content_href"
    ID_PREFIX = "content_nuget_symbol_packages"
    NEEDS_PLUGINS = [PluginRequirement("nuget")]
    CAPABILITIES = {"upload": []}


class PulpNugetDistributionContext(PulpDistributionContext):
    PLUGIN = "nuget"
    RESOURCE_TYPE = "nuget"
    ENTITY = _("nuget distribution")
    ENTITIES = _("nuget distributions")
    HREF = "nuget_nuget_distribution_href"
    ID_PREFIX = "distributions_nuget_nuget"
    NEEDS_PLUGINS = [PluginRequirement("nuget")]
    CAPABILITIES = {"roles": [PluginRequirement("nuget")]}
    NULLABLES = PulpDistributionContext.NULLABLES | {"repository", "content_guard"}


class PulpNugetRemoteContext(PulpRemoteContext):
    PLUGIN = "nuget"
    RESOURCE_TYPE = "nuget"
    ENTITY = _("nuget remote")
    ENTITIES = _("nuget remotes")
    HREF = "nuget_nuget_remote_href"
    ID_PREFIX = "remotes_nuget_nuget"
    NEEDS_PLUGINS = [PluginRequirement("nuget")]
    CAPABILITIES = {"roles": [PluginRequirement("nuget")]}


class PulpNugetRepositoryVersionContext(PulpRepositoryVersionContext):
    HREF = "nuget_nuget_repository_version_href"
    ID_PREFIX = "repositories_nuget_nuget_versions"
    NEEDS_PLUGINS = [PluginRequirement("nuget")]


class PulpNugetRepositoryContext(PulpRepositoryContext):
    PLUGIN = "nuget"
    RESOURCE_TYPE = "nuget"
    ENTITY = _("nuget repository")
    ENTITIES = _("nuget repositories")
    HREF = "nuget_nuget_repository_href"
    ID_PREFIX = "repositories_nuget_nuget"
    VERSION_CONTEXT = PulpNugetRepositoryVersionContext
    NEEDS_PLUGINS = [PluginRequirement("nuget")]
    CAPABILITIES = {
        "sync": [PluginRequirement("nuget")],
        "pulpexport": [PluginRequirement("nuget")],
        "roles": [PluginRequirement("nuget")],
    }
    NULLABLES = PulpRepositoryContext.NULLABLES | {"remote"}

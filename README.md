# pulp-cli-nuget

A [pulp-cli](https://pulpproject.org/pulp-cli/) plugin adding `pulp nuget` commands for
[pulp_nuget](https://github.com/PhillipDiCarlo/pulp_nuget), the NuGet plugin for Pulp 3.

```
pip install pulp-cli-nuget
```

## Usage

```bash
pulp nuget repository create --name foo --retain-package-versions 5
pulp nuget remote create --name upstream --url https://api.nuget.org/v3/index.json \
    --policy on_demand --includes '["Serilog [3.0,)", "Newtonsoft.Json"]'
pulp nuget repository sync --name foo --remote upstream
pulp nuget distribution create --name foo --base-path foo --repository foo
pulp nuget content upload --file my.package.1.0.0.nupkg --repository foo
pulp nuget content --type symbol-package upload --file my.package.1.0.0.snupkg --repository foo
pulp nuget content list --package-id serilog
pulp nuget repository content add --repository foo --package-id serilog --version 4.2.0
pulp nuget repository content remove --repository foo --package-id serilog --version 4.2.0
pulp nuget repository content modify --repository foo \
    --add-content '[{"package_id": "serilog", "version": "4.2.0"}]'
pulp nuget remote create --name mirror --url https://mirror.example.com/v3/index.json \
    --policy on_demand --includes '["*"]'
pulp nuget acs create --name mirror --remote mirror
pulp nuget acs refresh --name mirror
```

The repository ships two packages:

- **pulp-cli-nuget** — the click commands (`pulpcore.cli.nuget`), mounted into pulp-cli
  via the `pulp_cli.plugins` entry point.
- **pulp-glue-nuget** (in [`pulp-glue-nuget/`](pulp-glue-nuget/)) — the version-agnostic
  API layer (`pulp_glue.nuget`), usable on its own.

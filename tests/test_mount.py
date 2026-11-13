"""Smoke tests: the plugin mounts into pulp-cli and its commands parse offline."""

from click.testing import CliRunner


def test_nuget_group_mounts_and_help_renders():
    from pulp_cli import load_plugins, main

    load_plugins()
    runner = CliRunner()
    result = runner.invoke(main, ["nuget", "--help"], catch_exceptions=False)
    assert result.exit_code == 0
    for group in ("repository", "remote", "distribution", "content", "acs"):
        assert group in result.output


def test_subcommand_help_renders():
    from pulp_cli import load_plugins, main

    load_plugins()
    runner = CliRunner()
    for args in (
        ["nuget", "repository", "--help"],
        ["nuget", "repository", "sync", "--help"],
        ["nuget", "repository", "content", "add", "--help"],
        ["nuget", "repository", "content", "remove", "--help"],
        ["nuget", "repository", "content", "modify", "--help"],
        ["nuget", "remote", "create", "--help"],
        ["nuget", "distribution", "create", "--help"],
        ["nuget", "content", "upload", "--help"],
        ["nuget", "acs", "create", "--help"],
        ["nuget", "acs", "refresh", "--help"],
        ["nuget", "acs", "path", "add", "--help"],
    ):
        result = runner.invoke(main, args, catch_exceptions=False)
        assert result.exit_code == 0, args


def test_content_selectors_cannot_be_mixed():
    """--href and --package-id/--version are alternatives; the pair must be complete."""
    from pulp_cli import load_plugins, main

    load_plugins()
    runner = CliRunner()
    base = ["--base-url", "http://localhost:1", "nuget", "repository", "content"]
    href = "/pulp/api/v3/content/nuget/packages/0123/"
    for command in ("add", "remove"):
        for selector in (
            ["--href", href, "--package-id", "serilog", "--version", "4.0.0"],
            ["--package-id", "serilog"],
            ["--version", "4.0.0"],
        ):
            # Usage errors are raised before anything talks to the server.
            result = runner.invoke(main, base + [command, "--repository", "foo"] + selector)
            assert result.exit_code == 2, (command, selector, result.output)

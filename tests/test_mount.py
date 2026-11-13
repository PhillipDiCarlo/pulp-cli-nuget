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

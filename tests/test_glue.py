"""Offline tests for the request bodies pulp-glue-nuget builds."""

from unittest.mock import MagicMock

import pytest
from pulp_glue.common.exceptions import PulpException
from pulp_glue.nuget.context import PulpNugetDistributionContext

REPOSITORY = "/pulp/api/v3/repositories/nuget/nuget/0123/"


def test_distribution_version_pins_a_repository_version():
    context = PulpNugetDistributionContext(MagicMock())
    body = context.preprocess_entity({"repository": REPOSITORY, "version": 2})
    assert body == {"repository": None, "repository_version": f"{REPOSITORY}versions/2/"}


def test_distribution_repository_alone_clears_the_pin():
    context = PulpNugetDistributionContext(MagicMock())
    body = context.preprocess_entity({"repository": REPOSITORY}, partial=True)
    assert body == {"repository": REPOSITORY, "repository_version": None}


def test_distribution_version_needs_a_repository():
    context = PulpNugetDistributionContext(MagicMock())
    with pytest.raises(PulpException):
        context.preprocess_entity({"name": "foo", "base_path": "foo", "version": 2})


def test_distribution_update_without_repository_options_leaves_the_pin_alone():
    context = PulpNugetDistributionContext(MagicMock())
    assert context.preprocess_entity({"base_path": "bar"}, partial=True) == {"base_path": "bar"}

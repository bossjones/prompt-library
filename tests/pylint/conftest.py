"""Configuration for pylint tests."""

from __future__ import annotations

import sys

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
from types import ModuleType
from typing import TYPE_CHECKING

import pytest

from pylint.checkers import BaseChecker
from pylint.testutils.unittest_linter import UnittestLinter


if TYPE_CHECKING:
    from _pytest.capture import CaptureFixture
    from _pytest.fixtures import FixtureRequest
    from _pytest.logging import LogCaptureFixture
    from _pytest.monkeypatch import MonkeyPatch

    from pytest_mock.plugin import MockerFixture

BASE_PATH = Path(__file__).parents[2]


def _load_plugin_from_file(module_name: str, file: str) -> ModuleType:
    """Load plugin from file path.

    Args:
        module_name: Name of the module to load
        file: Path to the file relative to BASE_PATH

    Returns:
        ModuleType: The loaded module

    Raises:
        AssertionError: If the module spec or loader is not found
    """
    spec = spec_from_file_location(
        module_name,
        str(BASE_PATH.joinpath(file)),
    )
    assert spec and spec.loader, f"Could not load module {module_name} from {file}"

    module = module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture(name="marimo_cell_validator", scope="package")
def marimo_cell_validator_fixture() -> ModuleType:
    """Fixture to provide the Marimo cell validator module.

    Returns:
        ModuleType: The loaded Marimo cell validator module
    """
    return _load_plugin_from_file(
        "marimo_cell_validator",
        "pylint/plugins/marimo_cell_validator.py",
    )


@pytest.fixture(name="marimo_imports_validator", scope="package")
def marimo_imports_validator_fixture() -> ModuleType:
    """Fixture to provide the Marimo imports validator module.

    Returns:
        ModuleType: The loaded Marimo imports validator module
    """
    return _load_plugin_from_file(
        "marimo_imports_validator",
        "pylint/plugins/marimo_imports_validator.py",
    )


@pytest.fixture(name="marimo_function_validator", scope="package")
def marimo_function_validator_fixture() -> ModuleType:
    """Fixture to provide the Marimo function validator module.

    Returns:
        ModuleType: The loaded Marimo function validator module
    """
    return _load_plugin_from_file(
        "marimo_function_validator",
        "pylint/plugins/marimo_function_validator.py",
    )


@pytest.fixture(name="marimo_checker")
def marimo_checker_fixture(marimo_cell_validator: ModuleType, linter: UnittestLinter) -> BaseChecker:
    """Fixture to provide a Marimo checker instance.

    Args:
        marimo_cell_validator: The Marimo cell validator module
        linter: The pylint linter instance

    Returns:
        BaseChecker: An instance of the Marimo checker
    """
    marimo_checker = marimo_cell_validator.MarimoChecker(linter)
    marimo_checker.module = "prompt_library.marimo_test"
    return marimo_checker


@pytest.fixture(name="marimo_imports_checker")
def marimo_imports_checker_fixture(marimo_imports_validator: ModuleType, linter: UnittestLinter) -> BaseChecker:
    """Fixture to provide a Marimo imports checker instance.

    Args:
        marimo_imports_validator: The Marimo imports validator module
        linter: The pylint linter instance

    Returns:
        BaseChecker: An instance of the Marimo imports checker
    """
    marimo_imports_checker = marimo_imports_validator.MarimoImportsChecker(linter)
    marimo_imports_checker.module = "prompt_library.marimo_test"
    return marimo_imports_checker


@pytest.fixture(name="marimo_function_checker")
def marimo_function_checker_fixture(marimo_function_validator: ModuleType, linter: UnittestLinter) -> BaseChecker:
    """Fixture to provide a Marimo function checker instance.

    Args:
        marimo_function_validator: The Marimo function validator module
        linter: The pylint linter instance

    Returns:
        BaseChecker: An instance of the Marimo function checker
    """
    marimo_function_checker = marimo_function_validator.MarimoFunctionChecker(linter)
    marimo_function_checker.module = "prompt_library.marimo_test"
    return marimo_function_checker


@pytest.fixture(name="linter")
def linter_fixture() -> UnittestLinter:
    """Fixture to provide a pylint linter instance.

    Returns:
        UnittestLinter: A configured pylint linter instance
    """
    return UnittestLinter()


@pytest.fixture(name="type_hint_checker")
def type_hint_checker_fixture(hass_enforce_type_hints: ModuleType, linter: UnittestLinter) -> BaseChecker:
    """Fixture to provide a type hint checker instance.

    Args:
        hass_enforce_type_hints: The type hint checker module
        linter: The pylint linter instance

    Returns:
        BaseChecker: An instance of the type hint checker
    """
    type_hint_checker = hass_enforce_type_hints.HassTypeHintChecker(linter)
    type_hint_checker.module = "homeassistant.components.pylint_test"
    return type_hint_checker

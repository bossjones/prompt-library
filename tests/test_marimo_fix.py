"""Tests for marimo_fix.py notebook functionality.

Uses pytest and ipytest to test marimo notebook cells.
"""

from __future__ import annotations

import importlib

from pathlib import Path

import marimo as mo

import pytest

import marimo_fix


@pytest.fixture(scope="module")
def app():
    """Fixture providing the marimo app instance.

    Returns:
        marimo.App: The app instance from the notebook
    """
    # Force reload to get fresh instance
    importlib.reload(marimo_fix)
    app = marimo_fix.app
    app._initialized = True
    return app


def test_styles_cell(app):
    """Test the styles dictionary cell returns expected keys."""
    outputs = []
    globals = {}

    # Run all cells in order
    for cell in app._cell_manager._cells.values():
        result = cell._cell._cell()
        if result is not None:
            outputs.append(result)
            if isinstance(result, tuple) and len(result) == 1:
                globals[cell._cell._name] = result[0]
            elif isinstance(result, tuple):
                for i, name in enumerate(
                    cell._cell._cell.__code__.co_varnames[: cell._cell._cell.__code__.co_argcount]
                ):
                    globals[name] = result[i]
    styles = globals.get("styles")

    assert isinstance(styles, dict)
    assert "container" in styles
    assert "card" in styles
    assert "error" in styles
    assert "success" in styles
    assert "warning" in styles
    assert "prompt_display" in styles


def test_imports_cell(app):
    """Test the imports cell returns expected modules."""
    outputs = []
    globals = {}

    # Run cells in order
    for cell in app._cell_manager._cells.values():
        result = cell._cell._cell()
        if result is not None:
            outputs.append(result)
            if isinstance(result, tuple) and len(result) == 1:
                globals[cell._cell._name] = result[0]
            elif isinstance(result, tuple):
                for i, name in enumerate(
                    cell._cell._cell.__code__.co_varnames[: cell._cell._cell.__code__.co_argcount]
                ):
                    globals[name] = result[i]

    # Check imports are available
    assert any("Path" in str(output) for output in outputs)
    assert any("datetime" in str(output) for output in outputs)
    assert any("glob" in str(output) for output in outputs)
    assert any("importlib" in str(output) for output in outputs)
    assert any("llm_module" in str(output) for output in outputs)
    assert any("mo" in str(output) for output in outputs)
    assert any("os" in str(output) for output in outputs)
    assert any("prompt_library_module" in str(output) for output in outputs)
    assert any("pytz" in str(output) for output in outputs)
    assert any("re" in str(output) for output in outputs)


def test_directories_cell(app):
    """Test the directories cell returns expected directory paths."""
    outputs = []
    globals = {}

    # Run cells in order
    for cell in app._cell_manager._cells.values():
        result = cell._cell._cell()
        if result is not None:
            outputs.append(result)
            if isinstance(result, tuple) and len(result) == 1:
                globals[cell._cell._name] = result[0]
            elif isinstance(result, tuple):
                for i, name in enumerate(
                    cell._cell._cell.__code__.co_varnames[: cell._cell._cell.__code__.co_argcount]
                ):
                    globals[name] = result[i]

    # Check directory paths in outputs
    assert any("one-off-tasks/lore-writing/helldivers2/johnhelldiver/questions" in str(output) for output in outputs)
    assert any("one-off-tasks/lore-writing/helldivers2/johnhelldiver/compare" in str(output) for output in outputs)
    assert any("./src/prompt_library/data/prompt_lib" in str(output) for output in outputs)
    assert any("./one-off-tasks" in str(output) for output in outputs)


def test_models_cell(app):
    """Test the models cell returns expected model dictionary."""
    outputs = []
    globals = {}

    # Run cells in order
    for cell in app._cell_manager._cells.values():
        result = cell._cell._cell()
        if result is not None:
            outputs.append(result)
            if isinstance(result, tuple) and len(result) == 1:
                globals[cell._cell._name] = result[0]
            elif isinstance(result, tuple):
                for i, name in enumerate(
                    cell._cell._cell.__code__.co_varnames[: cell._cell._cell.__code__.co_argcount]
                ):
                    globals[name] = result[i]

    # Check model names in outputs
    assert any("gpt-4o-latest" in str(output) for output in outputs)
    assert any("o1-mini" in str(output) for output in outputs)
    assert any("o1-preview" in str(output) for output in outputs)
    assert any("gpt-4o-mini" in str(output) for output in outputs)

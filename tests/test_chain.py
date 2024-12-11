from __future__ import annotations

import json
import os

from pathlib import Path
from typing import TYPE_CHECKING, Any, Dict, List, Tuple

import pytest

from prompt_library.common.chain import FusionChain, MinimalChainable
from prompt_library.common.typings import FusionChainResult


if TYPE_CHECKING:
    from _pytest.capture import CaptureFixture
    from _pytest.fixtures import FixtureRequest
    from _pytest.logging import LogCaptureFixture
    from _pytest.monkeypatch import MonkeyPatch

    from pytest_mock.plugin import MockerFixture


class MockModel:
    """Mock model for testing."""

    def __init__(self, name: str, responses: list[str]) -> None:
        """Initialize mock model.

        Args:
            name: Model identifier.
            responses: List of responses to return in sequence.
        """
        self.name = name
        self._responses = responses
        self._response_index = 0

    def get_response(self, prompt: str) -> str:
        """Get next response from the model.

        Args:
            prompt: Input prompt text.

        Returns:
            str: Next response in sequence.
        """
        response = self._responses[self._response_index]
        self._response_index = (self._response_index + 1) % len(self._responses)
        return response


@pytest.fixture
def mock_models() -> list[MockModel]:
    """Create mock models for testing.

    Returns:
        List[MockModel]: List of mock models with predefined responses.
    """
    return [
        MockModel("model1", ["response1", "response2"]),
        MockModel("model2", ["response3", "response4"]),
        MockModel("model3", ["response5", "response6"]),
    ]


@pytest.fixture
def sample_context() -> dict[str, Any]:
    """Create sample context for testing.

    Returns:
        Dict[str, Any]: Sample context dictionary.
    """
    return {
        "name": "test",
        "value": 123,
        "nested": {"key": "value"},
    }


@pytest.fixture
def sample_prompts() -> list[str]:
    """Create sample prompts for testing.

    Returns:
        List[str]: List of sample prompts.
    """
    return [
        "First prompt with {{name}}",
        "Second prompt with {{output[-1]}}",
        "Third prompt with {{output[-1].key}} and {{value}}",
    ]


def mock_callable(model: MockModel, prompt: str) -> str:
    """Mock callable for testing.

    Args:
        model: Mock model instance.
        prompt: Input prompt.

    Returns:
        str: Model's response.
    """
    return model.get_response(prompt)


def mock_evaluator(outputs: list[str]) -> tuple[str, list[float]]:
    """Mock evaluator for testing.

    Args:
        outputs: List of model outputs.

    Returns:
        Tuple[str, List[float]]: Best response and performance scores.
    """
    # Simple evaluator that picks the first response and assigns descending scores
    scores = [1.0 - (i * 0.1) for i in range(len(outputs))]
    return outputs[0], scores


def mock_get_model_name(model: MockModel) -> str:
    """Mock function to get model name.

    Args:
        model: Mock model instance.

    Returns:
        str: Model name.
    """
    return model.name


def test_fusion_chain_run(
    mock_models: list[MockModel],
    sample_context: dict[str, Any],
    sample_prompts: list[str],
) -> None:
    """Test FusionChain.run method.

    Args:
        mock_models: List of mock models.
        sample_context: Sample context dictionary.
        sample_prompts: List of sample prompts.
    """
    result = FusionChain.run(
        context=sample_context,
        models=mock_models,
        callable=mock_callable,
        prompts=sample_prompts,
        evaluator=mock_evaluator,
        get_model_name=mock_get_model_name,
    )

    assert isinstance(result, FusionChainResult)
    assert len(result.all_prompt_responses) == len(mock_models)
    assert len(result.performance_scores) == len(mock_models)
    assert result.llm_model_names == ["model1", "model2", "model3"]


def test_fusion_chain_run_parallel(
    mock_models: list[MockModel],
    sample_context: dict[str, Any],
    sample_prompts: list[str],
) -> None:
    """Test FusionChain.run_parallel method.

    Args:
        mock_models: List of mock models.
        sample_context: Sample context dictionary.
        sample_prompts: List of sample prompts.
    """
    result = FusionChain.run_parallel(
        context=sample_context,
        models=mock_models,
        callable=mock_callable,
        prompts=sample_prompts,
        evaluator=mock_evaluator,
        get_model_name=mock_get_model_name,
        num_workers=2,
    )

    assert isinstance(result, FusionChainResult)
    assert len(result.all_prompt_responses) == len(mock_models)
    assert len(result.performance_scores) == len(mock_models)
    assert result.llm_model_names == ["model1", "model2", "model3"]


def test_minimal_chainable_run(
    mock_models: list[MockModel],
    sample_context: dict[str, Any],
    sample_prompts: list[str],
) -> None:
    """Test MinimalChainable.run method.

    Args:
        mock_models: List of mock models.
        sample_context: Sample context dictionary.
        sample_prompts: List of sample prompts.
    """
    outputs, filled_prompts = MinimalChainable.run(
        context=sample_context,
        model=mock_models[0],
        callable=mock_callable,
        prompts=sample_prompts,
    )

    assert len(outputs) == len(sample_prompts)
    assert len(filled_prompts) == len(sample_prompts)
    assert "test" in filled_prompts[0]  # Context variable replacement
    assert "response1" in filled_prompts[1]  # Previous output reference


def test_minimal_chainable_json_handling(mock_models: list[MockModel]) -> None:
    """Test MinimalChainable JSON handling.

    Args:
        mock_models: List of mock models.
    """
    json_model = MockModel(
        "json_model",
        [
            '{"key": "value"}',
            '```json\n{"nested": {"key": "value"}}\n```',
            "not json",
        ],
    )

    outputs, _ = MinimalChainable.run(
        context={},
        model=json_model,
        callable=mock_callable,
        prompts=["1", "2", "3"],
    )

    assert isinstance(outputs[0], dict)
    assert outputs[0]["key"] == "value"
    assert isinstance(outputs[1], dict)
    assert outputs[1]["nested"]["key"] == "value"
    assert isinstance(outputs[2], str)
    assert outputs[2] == "not json"


def test_minimal_chainable_to_delim_text_file(tmp_path: Path) -> None:
    """Test MinimalChainable.to_delim_text_file method.

    Args:
        tmp_path: Pytest fixture providing temporary directory path.
    """
    os.chdir(tmp_path)
    content = [
        "text response",
        {"json": "response"},
        ["list", "response"],
        123,
    ]

    result = MinimalChainable.to_delim_text_file("test_output", content)

    # Check file was created
    assert os.path.exists("test_output.txt")

    # Check content
    with open("test_output.txt") as f:
        file_content = f.read()

    # Verify delimiters and content
    assert "🔗 -------- Prompt Chain Result #1" in file_content
    assert "🔗🔗 -------- Prompt Chain Result #2" in file_content
    assert "text response" in file_content
    assert '"json": "response"' in file_content
    assert '["list", "response"]' in file_content
    assert "123" in file_content

    # Check returned string
    assert result == file_content


def test_fusion_chain_error_handling(
    mock_models: list[MockModel],
    sample_context: dict[str, Any],
    sample_prompts: list[str],
) -> None:
    """Test FusionChain error handling.

    Args:
        mock_models: List of mock models.
        sample_context: Sample context dictionary.
        sample_prompts: List of sample prompts.
    """

    def failing_callable(model: MockModel, prompt: str) -> str:
        raise ValueError("Test error")

    with pytest.raises(ValueError):
        FusionChain.run(
            context=sample_context,
            models=mock_models,
            callable=failing_callable,
            prompts=sample_prompts,
            evaluator=mock_evaluator,
            get_model_name=mock_get_model_name,
        )


def test_minimal_chainable_context_references() -> None:
    """Test MinimalChainable context reference handling."""
    context = {"var1": "value1", "var2": {"nested": "value2"}}
    model = MockModel("test", ["response1"])
    prompts = [
        "Simple var: {{var1}}",
        "Missing var: {{missing}}",  # Should remain unchanged
        "Nested var: {{var2}}",
    ]

    outputs, filled_prompts = MinimalChainable.run(
        context=context,
        model=model,
        callable=mock_callable,
        prompts=prompts,
    )

    assert "value1" in filled_prompts[0]
    assert "{{missing}}" in filled_prompts[1]
    assert str({"nested": "value2"}) in filled_prompts[2]


def test_minimal_chainable_output_references() -> None:
    """Test MinimalChainable output reference handling."""
    model = MockModel(
        "test",
        [
            '{"key": "value1"}',
            "response2",
            "response3",
        ],
    )
    prompts = [
        "First prompt",
        "Previous output: {{output[-1]}}",
        "Previous key: {{output[-1].key}}",
    ]

    outputs, filled_prompts = MinimalChainable.run(
        context={},
        model=model,
        callable=mock_callable,
        prompts=prompts,
    )

    assert filled_prompts[0] == "First prompt"
    assert '{"key": "value1"}' in filled_prompts[1]
    assert "value1" in filled_prompts[2]

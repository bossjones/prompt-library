from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union

from pydantic import ValidationError

import pytest

from prompt_library.common.typings import FusionChainResult, ModelRanking, MultiLLMPromptExecution


if TYPE_CHECKING:
    from _pytest.capture import CaptureFixture
    from _pytest.fixtures import FixtureRequest
    from _pytest.logging import LogCaptureFixture
    from _pytest.monkeypatch import MonkeyPatch

    from pytest_mock.plugin import MockerFixture


@pytest.fixture
def sample_fusion_chain_result_data() -> dict[str, Any]:
    """Create sample data for FusionChainResult testing.

    Returns:
        Dict[str, Any]: Sample data for FusionChainResult model.
    """
    return {
        "top_response": "Best response",
        "all_prompt_responses": [["response1", "response2"], ["response3"]],
        "all_context_filled_prompts": [["prompt1", "prompt2"], ["prompt3"]],
        "performance_scores": [0.9, 0.8, 0.7],
        "llm_model_names": ["model1", "model2", "model3"],
    }


@pytest.fixture
def sample_multi_llm_execution_data() -> dict[str, Any]:
    """Create sample data for MultiLLMPromptExecution testing.

    Returns:
        Dict[str, Any]: Sample data for MultiLLMPromptExecution model.
    """
    return {
        "prompt_responses": [
            {"model": "model1", "response": "response1"},
            {"model": "model2", "response": "response2"},
        ],
        "prompt": "Test prompt",
        "prompt_template": "test_template",
    }


def test_fusion_chain_result_creation(sample_fusion_chain_result_data: dict[str, Any]) -> None:
    """Test creating a FusionChainResult instance.

    Args:
        sample_fusion_chain_result_data: Fixture providing sample data.
    """
    result = FusionChainResult(**sample_fusion_chain_result_data)
    assert result.top_response == "Best response"
    assert len(result.all_prompt_responses) == 2
    assert len(result.all_context_filled_prompts) == 2
    assert len(result.performance_scores) == 3
    assert len(result.llm_model_names) == 3


def test_fusion_chain_result_with_dict_response() -> None:
    """Test FusionChainResult with dictionary top response."""
    data = {
        "top_response": {"key": "value", "nested": {"subkey": "subvalue"}},
        "all_prompt_responses": [["response1"]],
        "all_context_filled_prompts": [["prompt1"]],
        "performance_scores": [0.9],
        "llm_model_names": ["model1"],
    }
    result = FusionChainResult(**data)
    assert isinstance(result.top_response, dict)
    assert result.top_response["key"] == "value"
    assert result.top_response["nested"]["subkey"] == "subvalue"


def test_fusion_chain_result_validation() -> None:
    """Test FusionChainResult validation."""
    # Missing required field
    with pytest.raises(ValidationError):
        FusionChainResult(
            all_prompt_responses=[["response1"]],
            all_context_filled_prompts=[["prompt1"]],
            performance_scores=[0.9],
        )

    # Invalid type for performance_scores
    with pytest.raises(ValidationError):
        FusionChainResult(
            top_response="response",
            all_prompt_responses=[["response1"]],
            all_context_filled_prompts=[["prompt1"]],
            performance_scores=["not_a_float"],
            llm_model_names=["model1"],
        )


def test_multi_llm_prompt_execution_creation(sample_multi_llm_execution_data: dict[str, Any]) -> None:
    """Test creating a MultiLLMPromptExecution instance.

    Args:
        sample_multi_llm_execution_data: Fixture providing sample data.
    """
    execution = MultiLLMPromptExecution(**sample_multi_llm_execution_data)
    assert len(execution.prompt_responses) == 2
    assert execution.prompt == "Test prompt"
    assert execution.prompt_template == "test_template"


def test_multi_llm_prompt_execution_optional_template() -> None:
    """Test MultiLLMPromptExecution with optional template field."""
    data = {
        "prompt_responses": [{"model": "model1", "response": "response1"}],
        "prompt": "Test prompt",
    }
    execution = MultiLLMPromptExecution(**data)
    assert execution.prompt_template is None


def test_multi_llm_prompt_execution_validation() -> None:
    """Test MultiLLMPromptExecution validation."""
    # Missing required field
    with pytest.raises(ValidationError):
        MultiLLMPromptExecution(prompt_responses=[{"model": "model1"}])

    # Invalid type for prompt_responses
    with pytest.raises(ValidationError):
        MultiLLMPromptExecution(
            prompt_responses="not_a_list",
            prompt="Test prompt",
        )


def test_model_ranking_creation() -> None:
    """Test creating a ModelRanking instance."""
    ranking = ModelRanking(llm_model_id="test_model", score=10)
    assert ranking.llm_model_id == "test_model"
    assert ranking.score == 10


def test_model_ranking_validation() -> None:
    """Test ModelRanking validation."""
    # Missing required field
    with pytest.raises(ValidationError):
        ModelRanking(score=10)

    # Invalid type for score
    with pytest.raises(ValidationError):
        ModelRanking(llm_model_id="test_model", score="not_an_int")


def test_model_serialization() -> None:
    """Test model serialization to dict and JSON."""
    # Test FusionChainResult
    fusion_data = {
        "top_response": "response",
        "all_prompt_responses": [["r1"]],
        "all_context_filled_prompts": [["p1"]],
        "performance_scores": [0.9],
        "llm_model_names": ["m1"],
    }
    fusion = FusionChainResult(**fusion_data)
    assert fusion.model_dump() == fusion_data

    # Test MultiLLMPromptExecution
    execution_data = {
        "prompt_responses": [{"model": "m1"}],
        "prompt": "prompt",
        "prompt_template": None,
    }
    execution = MultiLLMPromptExecution(**execution_data)
    assert execution.model_dump() == execution_data

    # Test ModelRanking
    ranking_data = {"llm_model_id": "model1", "score": 5}
    ranking = ModelRanking(**ranking_data)
    assert ranking.model_dump() == ranking_data


def test_model_validation_types() -> None:
    """Test type validation for all models."""
    # Test FusionChainResult type validation
    with pytest.raises(ValidationError):
        FusionChainResult(
            top_response=123,  # Should be str or dict
            all_prompt_responses="not_a_list",
            all_context_filled_prompts=[1, 2, 3],  # Should be list of lists
            performance_scores={"not": "a_list"},
            llm_model_names=None,
        )

    # Test MultiLLMPromptExecution type validation
    with pytest.raises(ValidationError):
        MultiLLMPromptExecution(
            prompt_responses=123,  # Should be list
            prompt=["not", "a", "string"],
            prompt_template=123,  # Should be str or None
        )

    # Test ModelRanking type validation
    with pytest.raises(ValidationError):
        ModelRanking(
            llm_model_id=123,  # Should be str
            score="not_an_int",  # Should be int
        )

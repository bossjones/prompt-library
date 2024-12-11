from __future__ import annotations

import os

from typing import TYPE_CHECKING, Any, Dict, Generator

from _pytest.monkeypatch import MonkeyPatch

import pytest

from prompt_library.common.llm_module import (
    build_big_3_models,
    build_big_3_plus_mini_models,
    build_gemini_1_2_002,
    build_gemini_duo,
    build_latest_openai,
    build_mini_model,
    build_o1_series,
    build_ollama_models,
    build_ollama_slm_models,
    build_openai_latest_and_fastest,
    build_openai_model_stack,
    build_small_cheap_and_fast,
    build_sonnet_3_5,
    conditional_render,
    get_model_name,
    parse_markdown_backticks,
    prompt,
    prompt_with_temp,
)


if TYPE_CHECKING:
    from _pytest.capture import CaptureFixture
    from _pytest.fixtures import FixtureRequest
    from _pytest.logging import LogCaptureFixture

    from pytest_mock.plugin import MockerFixture


class MockResponse:
    """Mock response object for LLM responses."""

    def __init__(self, text_value: str) -> None:
        """Initialize mock response.

        Args:
            text_value: The text value to return.
        """
        self._text = text_value

    def text(self) -> str:
        """Get response text.

        Returns:
            str: The mocked response text.
        """
        return self._text


class MockModel:
    """Mock LLM model for testing."""

    def __init__(self, model_id: str, response_text: str = "mock response") -> None:
        """Initialize mock model.

        Args:
            model_id: The model identifier.
            response_text: Text to return in responses.
        """
        self.model_id = model_id
        self.key: str | None = None
        self._response_text = response_text

    def prompt(self, text: str, stream: bool = False, temperature: float | None = None) -> MockResponse:
        """Mock prompt method.

        Args:
            text: The input prompt text.
            stream: Whether to stream the response.
            temperature: Temperature parameter for response generation.

        Returns:
            MockResponse: A mock response object.
        """
        return MockResponse(self._response_text)


@pytest.fixture
def mock_env_vars(monkeypatch: MonkeyPatch) -> None:
    """Set up mock environment variables for testing.

    Args:
        monkeypatch: Pytest monkeypatch fixture.
    """
    monkeypatch.setenv("ANTHROPIC_API_KEY", "mock_anthropic_key")
    monkeypatch.setenv("OPENAI_API_KEY", "mock_openai_key")
    monkeypatch.setenv("GEMINI_API_KEY", "mock_gemini_key")


@pytest.fixture
def mock_llm(mocker: MockerFixture) -> Generator[MockerFixture, None, None]:
    """Mock the llm package.

    Args:
        mocker: Pytest mocker fixture.

    Yields:
        MockerFixture: The mock fixture.
    """
    mock_llm = mocker.patch("prompt_library.common.llm_module.llm")
    mock_llm.get_model.side_effect = lambda model_id: MockModel(model_id)
    yield mock_llm


def test_conditional_render() -> None:
    """Test conditional template rendering."""
    template = """% if show_greeting
Hello ${name}!
% endif
% if show_farewell
Goodbye ${name}!
% endif"""

    # Test with both conditions true
    context = {"show_greeting": True, "show_farewell": True, "name": "World"}
    result = conditional_render(template, context)
    assert "Hello World!" in result
    assert "Goodbye World!" in result

    # Test with one condition false
    context = {"show_greeting": True, "show_farewell": False, "name": "World"}
    result = conditional_render(template, context)
    assert "Hello World!" in result
    assert "Goodbye World!" not in result


def test_parse_markdown_backticks() -> None:
    """Test parsing markdown code blocks."""
    # Test with Python code block
    markdown = """```python
def hello():
    print('Hello')
```"""
    result = parse_markdown_backticks(markdown)
    assert (
        result
        == """def hello():
    print('Hello')"""
    )

    # Test with no language specified
    markdown = """```
plain text
```"""
    result = parse_markdown_backticks(markdown)
    assert result == "plain text"

    # Test with no code blocks
    text = "plain text without backticks"
    result = parse_markdown_backticks(text)
    assert result == "plain text without backticks"


def test_prompt(mock_llm: MockerFixture) -> None:
    """Test basic model prompting.

    Args:
        mock_llm: Mocked llm package.
    """
    model = MockModel("test-model", "test response")
    result = prompt(model, "test prompt")
    assert result == "test response"


def test_prompt_with_temp(mock_llm: MockerFixture) -> None:
    """Test prompting with temperature control.

    Args:
        mock_llm: Mocked llm package.
    """
    # Test with regular model
    model = MockModel("test-model")
    result = prompt_with_temp(model, "test prompt", 0.5)
    assert result == "mock response"

    # Test with O1 model (fixed temperature)
    o1_model = MockModel("o1-model")
    result = prompt_with_temp(o1_model, "test prompt", 0.5)
    assert result == "mock response"

    # Test with Gemini model (fixed temperature)
    gemini_model = MockModel("gemini-model")
    result = prompt_with_temp(gemini_model, "test prompt", 0.5)
    assert result == "mock response"


def test_get_model_name(mock_llm: MockerFixture) -> None:
    """Test getting model identifier.

    Args:
        mock_llm: Mocked llm package.
    """
    model = MockModel("test-model")
    assert get_model_name(model) == "test-model"


def test_build_sonnet_3_5(mock_env_vars: None, mock_llm: MockerFixture) -> None:
    """Test building Claude 3.5 Sonnet model.

    Args:
        mock_env_vars: Mock environment variables.
        mock_llm: Mocked llm package.
    """
    model = build_sonnet_3_5()
    assert isinstance(model, MockModel)
    assert model.model_id == "claude-3.5-sonnet"
    assert model.key == "mock_anthropic_key"


def test_build_sonnet_3_5_no_api_key(monkeypatch: MonkeyPatch, mock_llm: MockerFixture) -> None:
    """Test building Sonnet model without API key.

    Args:
        monkeypatch: Pytest monkeypatch fixture.
        mock_llm: Mocked llm package.
    """
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    with pytest.raises(TypeError) as exc_info:
        build_sonnet_3_5()
    assert "ANTHROPIC_API_KEY environment variable must be set" in str(exc_info.value)


def test_build_mini_model(mock_env_vars: None, mock_llm: MockerFixture) -> None:
    """Test building mini model.

    Args:
        mock_env_vars: Mock environment variables.
        mock_llm: Mocked llm package.
    """
    model = build_mini_model()
    assert isinstance(model, MockModel)
    assert model.model_id == "gpt-4o-mini"
    assert model.key == "mock_openai_key"


def test_build_big_3_models(mock_env_vars: None, mock_llm: MockerFixture) -> None:
    """Test building big 3 models.

    Args:
        mock_env_vars: Mock environment variables.
        mock_llm: Mocked llm package.
    """
    sonnet, gpt4, gemini = build_big_3_models()

    assert isinstance(sonnet, MockModel)
    assert sonnet.model_id == "claude-3.5-sonnet"
    assert sonnet.key == "mock_anthropic_key"

    assert isinstance(gpt4, MockModel)
    assert gpt4.model_id == "4o"
    assert gpt4.key == "mock_openai_key"

    assert isinstance(gemini, MockModel)
    assert gemini.model_id == "gemini-1.5-pro-latest"
    assert gemini.key == "mock_gemini_key"


def test_build_big_3_plus_mini_models(mock_env_vars: None, mock_llm: MockerFixture) -> None:
    """Test building big 3 plus mini models.

    Args:
        mock_env_vars: Mock environment variables.
        mock_llm: Mocked llm package.
    """
    sonnet, gpt4, gemini, mini = build_big_3_plus_mini_models()

    assert isinstance(sonnet, MockModel)
    assert sonnet.model_id == "claude-3.5-sonnet"
    assert sonnet.key == "mock_anthropic_key"

    assert isinstance(gpt4, MockModel)
    assert gpt4.model_id == "4o"
    assert gpt4.key == "mock_openai_key"

    assert isinstance(gemini, MockModel)
    assert gemini.model_id == "gemini-1.5-pro-latest"
    assert gemini.key == "mock_gemini_key"

    assert isinstance(mini, MockModel)
    assert mini.model_id == "gpt-4o-mini"
    assert mini.key == "mock_openai_key"


def test_build_gemini_duo(mock_env_vars: None, mock_llm: MockerFixture) -> None:
    """Test building Gemini model pair.

    Args:
        mock_env_vars: Mock environment variables.
        mock_llm: Mocked llm package.
    """
    pro, flash = build_gemini_duo()

    assert isinstance(pro, MockModel)
    assert pro.model_id == "gemini-1.5-pro-latest"
    assert pro.key == "mock_gemini_key"

    assert isinstance(flash, MockModel)
    assert flash.model_id == "gemini-1.5-flash-latest"
    assert flash.key == "mock_gemini_key"


def test_build_ollama_models(mock_llm: MockerFixture) -> None:
    """Test building Ollama models.

    Args:
        mock_llm: Mocked llm package.
    """
    llama, llama_1b = build_ollama_models()

    assert isinstance(llama, MockModel)
    assert llama.model_id == "llama3.2"
    assert llama.key is None

    assert isinstance(llama_1b, MockModel)
    assert llama_1b.model_id == "llama3.2:1b"
    assert llama_1b.key is None


def test_build_ollama_slm_models(mock_llm: MockerFixture) -> None:
    """Test building Ollama SLM models.

    Args:
        mock_llm: Mocked llm package.
    """
    llama, phi, qwen = build_ollama_slm_models()

    assert isinstance(llama, MockModel)
    assert llama.model_id == "llama3.2"
    assert llama.key is None

    assert isinstance(phi, MockModel)
    assert phi.model_id == "phi3.5:latest"
    assert phi.key is None

    assert isinstance(qwen, MockModel)
    assert qwen.model_id == "qwen2.5:latest"
    assert qwen.key is None


def test_build_openai_model_stack(mock_env_vars: None, mock_llm: MockerFixture) -> None:
    """Test building OpenAI model stack.

    Args:
        mock_env_vars: Mock environment variables.
        mock_llm: Mocked llm package.
    """
    models = build_openai_model_stack()
    expected_models = ["gpt-4o-mini", "gpt-4o", "o1-preview", "o1-mini"]

    assert len(models) == len(expected_models)
    for model, expected_id in zip(models, expected_models, strict=False):
        assert isinstance(model, MockModel)
        assert model.model_id == expected_id
        assert model.key == "mock_openai_key"


def test_build_openai_latest_and_fastest(mock_env_vars: None, mock_llm: MockerFixture) -> None:
    """Test building latest and fastest OpenAI models.

    Args:
        mock_env_vars: Mock environment variables.
        mock_llm: Mocked llm package.
    """
    latest, mini = build_openai_latest_and_fastest()

    assert isinstance(latest, MockModel)
    assert latest.model_id == "gpt-4o"
    assert latest.key == "mock_openai_key"

    assert isinstance(mini, MockModel)
    assert mini.model_id == "gpt-4o-mini"
    assert mini.key == "mock_openai_key"


def test_build_o1_series(mock_env_vars: None, mock_llm: MockerFixture) -> None:
    """Test building O1 series models.

    Args:
        mock_env_vars: Mock environment variables.
        mock_llm: Mocked llm package.
    """
    mini, preview = build_o1_series()

    assert isinstance(mini, MockModel)
    assert mini.model_id == "o1-mini"
    assert mini.key == "mock_openai_key"

    assert isinstance(preview, MockModel)
    assert preview.model_id == "o1-preview"
    assert preview.key == "mock_openai_key"


def test_build_small_cheap_and_fast(mock_env_vars: None, mock_llm: MockerFixture) -> None:
    """Test building small, cheap, and fast models.

    Args:
        mock_env_vars: Mock environment variables.
        mock_llm: Mocked llm package.
    """
    mini, flash = build_small_cheap_and_fast()

    assert isinstance(mini, MockModel)
    assert mini.model_id == "gpt-4o-mini"
    assert mini.key == "mock_openai_key"

    assert isinstance(flash, MockModel)
    assert flash.model_id == "gemini-1.5-flash-002"
    assert flash.key == "mock_gemini_key"


def test_build_gemini_1_2_002(mock_env_vars: None, mock_llm: MockerFixture) -> None:
    """Test building Gemini 1.2.002 models.

    Args:
        mock_env_vars: Mock environment variables.
        mock_llm: Mocked llm package.
    """
    pro, flash = build_gemini_1_2_002()

    assert isinstance(pro, MockModel)
    assert pro.model_id == "gemini-1.5-pro-002"
    assert pro.key == "mock_gemini_key"

    assert isinstance(flash, MockModel)
    assert flash.model_id == "gemini-1.5-flash-002"
    assert flash.key == "mock_gemini_key"


def test_build_latest_openai(mock_env_vars: None, mock_llm: MockerFixture) -> None:
    """Test building latest OpenAI model.

    Args:
        mock_env_vars: Mock environment variables.
        mock_llm: Mocked llm package.
    """
    model = build_latest_openai()

    assert isinstance(model, MockModel)
    assert model.model_id == "gpt-4o"
    assert model.key == "mock_openai_key"

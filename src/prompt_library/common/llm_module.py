from __future__ import annotations

import os

from typing import Any

import llm

from dotenv import load_dotenv
from mako.template import Template


# Load environment variables from .env file
load_dotenv()


def conditional_render(
    prompt: str, context: dict[str, Any], start_delim: str = "% if", end_delim: str = "% endif"
) -> str:
    """Render a template with conditional blocks using Mako templating.

    This function takes a template string containing conditional blocks and renders it using
    the provided context variables. The conditional blocks are delimited by customizable
    start and end markers.

    Args:
        prompt: The template string containing conditional blocks
        context: Dictionary mapping variable names to values for template rendering
        start_delim: Starting delimiter for conditional blocks. Defaults to "% if"
        end_delim: Ending delimiter for conditional blocks. Defaults to "% endif"

    Returns:
        str: The rendered template string with conditionals evaluated

    Example:
        >>> template = '''% if show_greeting:\\nHello ${name}!\\n% endif'''
        >>> context = {"show_greeting": True, "name": "World"}
        >>> conditional_render(template, context)
        'Hello World!'
    """
    # Ensure proper Mako syntax
    prompt = prompt.replace("% if ", "% if ")
    """Render a template with conditional blocks using Mako templating.

    This function takes a template string containing conditional blocks and renders it using
    the provided context variables. The conditional blocks are delimited by customizable
    start and end markers.

    Args:
        prompt: The template string containing conditional blocks
        context: Dictionary mapping variable names to values for template rendering
        start_delim: Starting delimiter for conditional blocks. Defaults to "% if"
        end_delim: Ending delimiter for conditional blocks. Defaults to "% endif"

    Returns:
        str: The rendered template string with conditionals evaluated

    Example:
        >>> template = "% if show_greeting\nHello ${name}!\n% endif"
        >>> context = {"show_greeting": True, "name": "World"}
        >>> conditional_render(template, context)
        'Hello World!'
    """
    template = Template(prompt)
    return template.render(**context)


def parse_markdown_backticks(markdown_text: str) -> str:
    """Parse and extract code content from markdown backtick blocks.

    This function extracts code content from markdown-style code blocks delimited by
    triple backticks (```). It removes the backticks, language identifier, and any
    excess whitespace.

    Args:
        markdown_text: Input string potentially containing markdown code blocks

    Returns:
        str: The extracted code content with whitespace trimmed. If no code blocks
            are found, returns the input string stripped of whitespace.

    Example:
        >>> text = "```python\ndef hello():\n    print('Hello')\n```"
        >>> parse_markdown_backticks(text)
        "def hello():\n    print('Hello')"
    """
    if "```" not in markdown_text:
        return markdown_text.strip()
    # Remove opening backticks and language identifier
    markdown_text = markdown_text.split("```", 1)[-1].split("\n", 1)[-1]
    # Remove closing backticks
    markdown_text = markdown_text.rsplit("```", 1)[0]
    # Remove any leading or trailing whitespace
    return markdown_text.strip()


def prompt(model: llm.Model, prompt_text: str) -> str:
    """Send a basic prompt to the model and get its response.

    This function sends a prompt to the specified LLM model without streaming
    and returns the generated text response.

    Args:
        model: The LLM model instance to use for generating the response
        prompt_text: The prompt text to send to the model

    Returns:
        str: The model's generated response text

    Example:
        >>> model = build_sonnet_3_5()
        >>> response = prompt(model, "What is 2+2?")
        >>> print(response)
        '4'
    """
    res = model.prompt(prompt_text, stream=False)
    return res.text()


def prompt_with_temp(model: llm.Model, prompt_text: str, temperature: float = 0.7) -> str:
    """Send a prompt to the model with a specified temperature setting.

    This function sends a prompt to the model with temperature control for response
    randomness. Note that for O1 and Gemini models, temperature is fixed at 1.0
    regardless of input.

    Args:
        model: The LLM model instance to use for generating the response
        prompt_text: The prompt text to send to the model
        temperature: Controls randomness in the response. Higher values (e.g., 1.0)
            make output more random, lower values make it more deterministic.
            Defaults to 0.7. Note: Ignored for O1 and Gemini models.

    Returns:
        str: The model's generated response text

    Example:
        >>> model = build_sonnet_3_5()
        >>> response = prompt_with_temp(model, "Write a creative story", 0.9)
        >>> print(response)
        'Once upon a time...'
    """
    model_id = model.model_id
    if "o1" in model_id or "gemini" in model_id:
        temperature = 1
        res = model.prompt(prompt_text, stream=False)
        return res.text()

    res = model.prompt(prompt_text, stream=False, temperature=temperature)
    return res.text()


def get_model_name(model: llm.Model) -> str:
    """Get the identifier name of the model.

    This function returns the unique identifier string for the given model instance.
    This is useful for model-specific logic and debugging.

    Args:
        model: The LLM model instance to get the identifier for

    Returns:
        str: The model's identifier string (e.g., "claude-3.5-sonnet", "gpt-4o")

    Example:
        >>> model = build_sonnet_3_5()
        >>> print(get_model_name(model))
        'claude-3.5-sonnet'
    """
    return model.model_id


def build_sonnet_3_5() -> llm.Model:
    """Build and configure a Claude 3.5 Sonnet model instance.

    This function creates a new Claude 3.5 Sonnet model instance and configures it
    with the API key from environment variables. The API key must be set in the
    environment variable ANTHROPIC_API_KEY.

    Returns:
        llm.Model: Configured Claude 3.5 Sonnet model instance ready for use

    Raises:
        TypeError: If ANTHROPIC_API_KEY environment variable is not set

    Example:
        >>> model = build_sonnet_3_5()
        >>> response = prompt(model, "Hello!")
        >>> print(response)
        'Hi! How can I help you today?'
    """
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    if ANTHROPIC_API_KEY is None:
        raise TypeError("ANTHROPIC_API_KEY environment variable must be set")

    sonnet_3_5_model: llm.Model = llm.get_model("claude-3.5-sonnet")
    sonnet_3_5_model.key = ANTHROPIC_API_KEY

    return sonnet_3_5_model


def build_mini_model():
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    gpt4_o_mini_model: llm.Model = llm.get_model("gpt-4o-mini")
    gpt4_o_mini_model.key = OPENAI_API_KEY
    return gpt4_o_mini_model


def build_big_3_models():
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

    sonnet_3_5_model: llm.Model = llm.get_model("claude-3.5-sonnet")
    sonnet_3_5_model.key = ANTHROPIC_API_KEY

    gpt4_o_model: llm.Model = llm.get_model("4o")
    gpt4_o_model.key = OPENAI_API_KEY

    gemini_1_5_pro_model: llm.Model = llm.get_model("gemini-1.5-pro-latest")
    gemini_1_5_pro_model.key = GEMINI_API_KEY

    return sonnet_3_5_model, gpt4_o_model, gemini_1_5_pro_model


def build_latest_openai():
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    # chatgpt_4o_latest_model: llm.Model = llm.get_model("chatgpt-4o-latest") - experimental
    chatgpt_4o_latest_model: llm.Model = llm.get_model("gpt-4o")
    chatgpt_4o_latest_model.key = OPENAI_API_KEY
    return chatgpt_4o_latest_model


def build_big_3_plus_mini_models():
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

    sonnet_3_5_model: llm.Model = llm.get_model("claude-3.5-sonnet")
    sonnet_3_5_model.key = ANTHROPIC_API_KEY

    gpt4_o_model: llm.Model = llm.get_model("4o")
    gpt4_o_model.key = OPENAI_API_KEY

    gemini_1_5_pro_model: llm.Model = llm.get_model("gemini-1.5-pro-latest")
    gemini_1_5_pro_model.key = GEMINI_API_KEY

    gpt4_o_mini_model: llm.Model = llm.get_model("gpt-4o-mini")
    gpt4_o_mini_model.key = OPENAI_API_KEY

    chatgpt_4o_latest_model = build_latest_openai()

    return (
        sonnet_3_5_model,
        gpt4_o_model,
        gemini_1_5_pro_model,
        gpt4_o_mini_model,
    )


def build_gemini_duo():
    gemini_1_5_pro: llm.Model = llm.get_model("gemini-1.5-pro-latest")
    gemini_1_5_flash: llm.Model = llm.get_model("gemini-1.5-flash-latest")

    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

    gemini_1_5_pro.key = GEMINI_API_KEY
    gemini_1_5_flash.key = GEMINI_API_KEY

    return gemini_1_5_pro, gemini_1_5_flash


def build_ollama_models():
    llama3_2_model: llm.Model = llm.get_model("llama3.2")
    llama_3_2_1b_model: llm.Model = llm.get_model("llama3.2:1b")

    return llama3_2_model, llama_3_2_1b_model


def build_ollama_slm_models():
    llama3_2_model: llm.Model = llm.get_model("llama3.2")
    phi3_5_model: llm.Model = llm.get_model("phi3.5:latest")
    qwen2_5_model: llm.Model = llm.get_model("qwen2.5:latest")

    return llama3_2_model, phi3_5_model, qwen2_5_model


def build_openai_model_stack():
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    gpt4_o_mini_model: llm.Model = llm.get_model("gpt-4o-mini")
    gpt4_o_2024_08_06_model: llm.Model = llm.get_model("gpt-4o")
    o1_preview_model: llm.Model = llm.get_model("o1-preview")
    o1_mini_model: llm.Model = llm.get_model("o1-mini")

    models = [
        gpt4_o_mini_model,
        gpt4_o_2024_08_06_model,
        o1_preview_model,
        o1_mini_model,
    ]

    for model in models:
        model.key = OPENAI_API_KEY

    return models


def build_openai_latest_and_fastest():
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    gpt_4o_latest: llm.Model = llm.get_model("gpt-4o")
    gpt_4o_latest.key = OPENAI_API_KEY

    gpt_4o_mini_model: llm.Model = llm.get_model("gpt-4o-mini")
    gpt_4o_mini_model.key = OPENAI_API_KEY

    return gpt_4o_latest, gpt_4o_mini_model


def build_o1_series():
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    o1_mini_model: llm.Model = llm.get_model("o1-mini")
    o1_mini_model.key = OPENAI_API_KEY

    o1_preview_model: llm.Model = llm.get_model("o1-preview")
    o1_preview_model.key = OPENAI_API_KEY

    return o1_mini_model, o1_preview_model


def build_small_cheap_and_fast():
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    gpt4_o_mini_model: llm.Model = llm.get_model("gpt-4o-mini")
    gpt4_o_mini_model.key = OPENAI_API_KEY

    gemini_1_5_flash_002: llm.Model = llm.get_model("gemini-1.5-flash-002")
    gemini_1_5_flash_002.key = GEMINI_API_KEY

    return gpt4_o_mini_model, gemini_1_5_flash_002


def build_gemini_1_2_002():
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

    gemini_1_5_pro_002: llm.Model = llm.get_model("gemini-1.5-pro-002")
    gemini_1_5_flash_002: llm.Model = llm.get_model("gemini-1.5-flash-002")

    gemini_1_5_pro_002.key = GEMINI_API_KEY
    gemini_1_5_flash_002.key = GEMINI_API_KEY

    return gemini_1_5_pro_002, gemini_1_5_flash_002

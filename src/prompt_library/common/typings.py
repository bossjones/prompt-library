from __future__ import annotations

from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, ConfigDict


class FusionChainResult(BaseModel):
    top_response: Union[str, dict[str, Any]]
    all_prompt_responses: list[list[Any]]
    all_context_filled_prompts: list[list[str]]
    performance_scores: list[float]
    llm_model_names: list[str]


class MultiLLMPromptExecution(BaseModel):
    prompt_responses: list[dict[str, Any]]
    prompt: str
    prompt_template: Optional[str] = None


class ModelRanking(BaseModel):
    llm_model_id: str
    score: int

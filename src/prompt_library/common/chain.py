from __future__ import annotations

import concurrent.futures
import json
import re

from typing import Any, Callable, Dict, List, Tuple, TypeVar, Union, cast

from prompt_library.common.typings import FusionChainResult


# Type variables for better type hints
ModelType = TypeVar("ModelType")
OutputType = TypeVar("OutputType")


class FusionChain:
    """A class for running competitions between multiple language models on a series of prompts.

    This class provides methods to run multiple models on the same prompts and evaluate their performance,
    either sequentially or in parallel.
    """

    @staticmethod
    def run(
        context: dict[str, Any],
        models: list[ModelType],
        callable: Callable[[ModelType, str], str],
        prompts: list[str],
        evaluator: Callable[[list[Any]], tuple[Any, list[float]]],
        get_model_name: Callable[[ModelType], str],
    ) -> FusionChainResult:
        """Run a competition between models on a list of prompts.

        Runs the MinimalChainable.run method for each model for each prompt and evaluates the results.
        The evaluator runs on the last output of each model at the end of the chain of prompts.
        The eval method returns a performance score for each model from 0 to 1.

        Args:
            context: The context dictionary for prompt template variables.
            models: List of language models to compete.
            callable: Function to call for each prompt, taking model and prompt as arguments.
            prompts: List of prompt templates to process.
            evaluator: Function to evaluate model outputs, returning top response and scores.
            get_model_name: Function to get the name/identifier of a model.

        Returns:
            FusionChainResult containing top response, all outputs, prompts, scores, and model names.

        Raises:
            ValueError: If models list is empty or prompts list is empty.
            RuntimeError: If evaluator returns invalid scores.
        """
        if not models:
            raise ValueError("Models list cannot be empty")
        if not prompts:
            raise ValueError("Prompts list cannot be empty")

        all_outputs: list[list[Any]] = []
        all_context_filled_prompts: list[list[str]] = []

        for model in models:
            outputs, context_filled_prompts = MinimalChainable.run(context, model, callable, prompts)
            all_outputs.append(outputs)
            all_context_filled_prompts.append(context_filled_prompts)

        # Evaluate the last output of each model
        last_outputs = [outputs[-1] for outputs in all_outputs]
        top_response, performance_scores = evaluator(last_outputs)

        # Validate performance scores
        if len(performance_scores) != len(models):
            raise RuntimeError("Evaluator returned incorrect number of scores")
        if not all(0 <= score <= 1 for score in performance_scores):
            raise RuntimeError("Performance scores must be between 0 and 1")

        model_names = [get_model_name(model) for model in models]

        return FusionChainResult(
            top_response=top_response,
            all_prompt_responses=all_outputs,
            all_context_filled_prompts=all_context_filled_prompts,
            performance_scores=performance_scores,
            llm_model_names=model_names,
        )

    @staticmethod
    def run_parallel(
        context: dict[str, Any],
        models: list[ModelType],
        callable: Callable[[ModelType, str], str],
        prompts: list[str],
        evaluator: Callable[[list[Any]], tuple[Any, list[float]]],
        get_model_name: Callable[[ModelType], str],
        num_workers: int = 4,
    ) -> FusionChainResult:
        """Run a competition between models on a list of prompts in parallel.

        Similar to run() but utilizes parallel processing for better performance with multiple models.

        Args:
            context: The context dictionary for prompt template variables.
            models: List of language models to compete.
            callable: Function to call for each prompt, taking model and prompt as arguments.
            prompts: List of prompt templates to process.
            evaluator: Function to evaluate model outputs, returning top response and scores.
            get_model_name: Function to get the name/identifier of a model.
            num_workers: Number of parallel workers to use, defaults to 4.

        Returns:
            FusionChainResult containing top response, all outputs, prompts, scores, and model names.

        Raises:
            ValueError: If models list is empty, prompts list is empty, or num_workers < 1.
            RuntimeError: If evaluator returns invalid scores or parallel execution fails.
        """
        if not models:
            raise ValueError("Models list cannot be empty")
        if not prompts:
            raise ValueError("Prompts list cannot be empty")
        if num_workers < 1:
            raise ValueError("Number of workers must be at least 1")

        def process_model(model: ModelType) -> tuple[list[Any], list[str]]:
            return MinimalChainable.run(context, model, callable, prompts)

        all_outputs: list[list[Any]] = []
        all_context_filled_prompts: list[list[str]] = []

        with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
            future_to_model = {executor.submit(process_model, model): model for model in models}

            try:
                for future in concurrent.futures.as_completed(future_to_model):
                    outputs, context_filled_prompts = future.result()
                    all_outputs.append(outputs)
                    all_context_filled_prompts.append(context_filled_prompts)
            except Exception as e:
                raise RuntimeError(f"Parallel execution failed: {e!s}") from e

        # Evaluate the last output of each model
        last_outputs = [outputs[-1] for outputs in all_outputs]
        top_response, performance_scores = evaluator(last_outputs)

        # Validate performance scores
        if len(performance_scores) != len(models):
            raise RuntimeError("Evaluator returned incorrect number of scores")
        if not all(0 <= score <= 1 for score in performance_scores):
            raise RuntimeError("Performance scores must be between 0 and 1")

        model_names = [get_model_name(model) for model in models]

        return FusionChainResult(
            top_response=top_response,
            all_prompt_responses=all_outputs,
            all_context_filled_prompts=all_context_filled_prompts,
            performance_scores=performance_scores,
            llm_model_names=model_names,
        )


class MinimalChainable:
    """Sequential prompt chaining with context and output back-references.

    This class provides functionality to run a sequence of prompts through a language model,
    with support for referencing context variables and previous outputs in the prompts.
    """

    @staticmethod
    def run(
        context: dict[str, Any],
        model: ModelType,
        callable: Callable[[ModelType, str], str],
        prompts: list[str],
    ) -> tuple[list[Any], list[str]]:
        """Run a sequence of prompts through a model with context and output references.

        Args:
            context: Dictionary of variables that can be referenced in prompts.
            model: The language model to use.
            callable: Function to call for each prompt, taking model and prompt as arguments.
            prompts: List of prompt templates to process.

        Returns:
            Tuple containing:
                - List of outputs from each prompt
                - List of context-filled prompts that were sent to the model

        Raises:
            ValueError: If prompts list is empty.
        """
        if not prompts:
            raise ValueError("Prompts list cannot be empty")

        output: list[Any] = []
        context_filled_prompts: list[str] = []

        for i, prompt in enumerate(prompts):
            # Fill context variables
            for key, value in context.items():
                if "{{" + key + "}}" in prompt:
                    prompt = prompt.replace("{{" + key + "}}", str(value))

            # Replace references to previous outputs
            for j in range(i, 0, -1):
                previous_output = output[i - j]

                # Handle JSON (dict) output references
                if isinstance(previous_output, dict):
                    # Handle full dict reference
                    if f"{{{{output[-{j}]}}}}" in prompt:
                        prompt = prompt.replace(f"{{{{output[-{j}]}}}}", json.dumps(previous_output))
                    # Handle key references
                    for key, value in previous_output.items():
                        key_ref = f"{{{{output[-{j}].{key}}}}}"
                        if key_ref in prompt:
                            prompt = prompt.replace(key_ref, str(value))
                else:
                    # Handle non-dict output reference
                    if f"{{{{output[-{j}]}}}}" in prompt:
                        prompt = prompt.replace(f"{{{{output[-{j}]}}}}", str(previous_output))

            context_filled_prompts.append(prompt)

            # Get model response
            result = callable(model, prompt)

            # Try to parse JSON from response
            try:
                # First check for JSON in markdown code blocks
                json_match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", result)
                if json_match:
                    result = json.loads(json_match.group(1))
                else:
                    # Try parsing entire result as JSON
                    result = json.loads(result)
            except json.JSONDecodeError:
                # Not JSON, keep as is
                pass

            output.append(result)

        return output, context_filled_prompts

    @staticmethod
    def to_delim_text_file(name: str, content: list[Union[str, dict, list]]) -> str:
        """Write chain results to a delimited text file.

        Args:
            name: Base name for the output file (without extension).
            content: List of content items to write.

        Returns:
            str: The formatted content string that was written to the file.

        Raises:
            IOError: If file writing fails.
        """
        result_string = ""
        try:
            with open(f"{name}.txt", "w") as outfile:
                for i, item in enumerate(content, 1):
                    if isinstance(item, (dict, list)):
                        item = json.dumps(item)
                    elif not isinstance(item, str):
                        item = str(item)
                    chain_text_delim = f"{'🔗' * i} -------- Prompt Chain Result #{i} -------------\n\n"
                    outfile.write(chain_text_delim)
                    outfile.write(item)
                    outfile.write("\n\n")

                    result_string += chain_text_delim + item + "\n\n"
        except OSError as e:
            raise OSError(f"Failed to write to file {name}.txt: {e!s}") from e

        return result_string

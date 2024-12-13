# pragma: no cover
from __future__ import annotations

import re

from typing import Any, Dict, List, Optional, Tuple, Union

import marimo


__generated_with = "0.9.34"
app = marimo.App(width="full")  # Use full width for side-by-side comparison


@app.cell
def __():
    styles = {
        "container": {
            "max-width": "800px",
            "margin": "0 auto",
            "padding": "20px",
        },
        "card": {
            "background": "#ffffff",
            "border-radius": "8px",
            "box-shadow": "0 2px 4px rgba(0,0,0,0.1)",
            "padding": "16px",
            "margin-bottom": "16px",
        },
        "error": {
            "color": "red",
            "padding": "10px",
            "border-radius": "5px",
            "background": "#ffebee",
        },
        "success": {
            "color": "green",
            "padding": "10px",
            "border-radius": "5px",
            "background": "#e8f5e9",
        },
        "warning": {
            "color": "orange",
            "padding": "10px",
            "border-radius": "5px",
            "background": "#fff3e0",
        },
        "prompt_display": {
            "background": "#eee",
            "padding": "10px",
            "border-radius": "10px",
            "margin-bottom": "20px",
            "min-width": "200px",
            "box-shadow": "2px 2px 2px #ccc",
        },
    }
    return styles


@app.cell
def __():
    import glob
    import importlib
    import os  # For path operations
    import re

    from datetime import datetime
    from pathlib import Path

    import marimo as mo
    import pytz

    from prompt_library.common import llm_module, prompt_library_module

    # Force reload of the module to get the latest version
    importlib.reload(prompt_library_module)

    return (
        Path,
        datetime,
        glob,
        importlib,
        llm_module,
        mo,
        os,
        prompt_library_module,
        pytz,
        re,
    )


@app.cell
def __():
    # Define the directories to search for prompts
    QUESTIONS_DIR = "one-off-tasks/lore-writing/helldivers2/johnhelldiver/questions"
    COMPARE_DIR = "one-off-tasks/lore-writing/helldivers2/johnhelldiver/compare"
    PROMPT_DIRS = ["./src/prompt_library/data/prompt_lib", "./one-off-tasks"]

    return (
        COMPARE_DIR,
        QUESTIONS_DIR,
        PROMPT_DIRS,
    )


@app.cell
def __(mo, prompt_library_module, QUESTIONS_DIR, COMPARE_DIR, PROMPT_DIRS):
    # Convert to Path objects and load prompts from all directories, filtering for XML files
    with mo.status.spinner(title="Loading XML prompts from all directories..."):
        map_prompt_library = prompt_library_module.pull_in_multiple_prompt_libraries(
            directories=PROMPT_DIRS, file_type="xml"
        )

    return (COMPARE_DIR, QUESTIONS_DIR, map_prompt_library)


@app.cell
def __(llm_module, QUESTIONS_DIR):
    # Initialize LLM models
    llm_o1_mini, llm_o1_preview = llm_module.build_o1_series()
    llm_gpt_4o_latest, llm_gpt_4o_mini = llm_module.build_openai_latest_and_fastest()

    models = {
        "gpt-4o-latest": llm_gpt_4o_latest,  # Move to top for default selection
        "o1-mini": llm_o1_mini,
        "o1-preview": llm_o1_preview,
        "gpt-4o-mini": llm_gpt_4o_mini,
    }
    return (models, QUESTIONS_DIR)


@app.cell
def __(QUESTIONS_DIR, mo, prompt_library_module):
    question_names = ["None"] + prompt_library_module.get_question_files(QUESTIONS_DIR)

    question_selector = mo.ui.dropdown(
        options=question_names, value="None", label="Select a predefined question (or None to write your own)"
    )

    return (question_selector,)


@app.cell
def __(question_selector, QUESTIONS_DIR, mo, prompt_library_module):
    question_input = mo.ui.text_area(value="", placeholder="Enter your question here...", label="Question")

    if question_selector.value != "None":
        question_input.value = prompt_library_module.read_question_file(question_selector.value, QUESTIONS_DIR)

    mo.md("### Question Input")
    mo.hstack([question_selector, question_input])
    return question_input, question_selector


@app.cell
def __(map_prompt_library, mo, models, styles):
    # Stop if no prompts were loaded
    mo.stop(
        not map_prompt_library,
        mo.md("""
    ❌ **Error**: No prompts are available to display. Please check the error messages above.
    """).style(styles["error"]),  # type: ignore
    )

    # Create dropdowns for first prompt
    prompt_dropdown_1 = mo.ui.dropdown(
        options=list(map_prompt_library.keys()),
        label="Select First Prompt",
    )
    model_dropdown_1 = mo.ui.dropdown(
        options=list(models.keys()),
        label="Select First LLM Model",
        value="gpt-4o-latest",
    )

    # Create dropdowns for second prompt
    prompt_dropdown_2 = mo.ui.dropdown(
        options=list(map_prompt_library.keys()),
        label="Select Second Prompt",
    )
    model_dropdown_2 = mo.ui.dropdown(
        options=list(models.keys()),
        label="Select Second LLM Model",
        value="gpt-4o-latest",
    )

    # Create a form with both sets of dropdowns
    form = (
        mo.md(
            r"""
            # Prompt Analysis
            ### First Prompt Configuration
            {prompt_dropdown_1}
            {model_dropdown_1}

            ### Second Prompt Configuration
            {prompt_dropdown_2}
            {model_dropdown_2}
            """
        )
        .batch(
            prompt_dropdown_1=prompt_dropdown_1,
            model_dropdown_1=model_dropdown_1,
            prompt_dropdown_2=prompt_dropdown_2,
            model_dropdown_2=model_dropdown_2,
        )
        .form()
    ).style(styles["container"])  # type: ignore
    form
    return form, model_dropdown_1, model_dropdown_2, prompt_dropdown_1, prompt_dropdown_2


@app.cell
def __(map_prompt_library, mo, styles, prompt_dropdown_1, prompt_dropdown_2):
    mo.stop(not prompt_dropdown_1.value or not prompt_dropdown_2.value, "Please select both prompts.")

    # Get first prompt
    selected_prompt_name_1 = prompt_dropdown_1.value  # type: ignore
    selected_prompt_1 = map_prompt_library[selected_prompt_name_1]  # type: ignore

    # Get second prompt
    selected_prompt_name_2 = prompt_dropdown_2.value  # type: ignore
    selected_prompt_2 = map_prompt_library[selected_prompt_name_2]  # type: ignore

    # Display prompts side by side
    mo.hstack([
        mo.vstack([
            mo.md("# First Selected Prompt"),
            mo.accordion({
                "### Click to show": mo.md(f"```xml\n{selected_prompt_1}\n```").style(styles["prompt_display"])  # type: ignore
            }),
        ]),
        mo.vstack([
            mo.md("# Second Selected Prompt"),
            mo.accordion({
                "### Click to show": mo.md(f"```xml\n{selected_prompt_2}\n```").style(styles["prompt_display"])  # type: ignore
            }),
        ]),
    ]).style(styles["container"])  # type: ignore
    return selected_prompt_1, selected_prompt_2, selected_prompt_name_1, selected_prompt_name_2


@app.cell
def __(mo, re, selected_prompt_1, selected_prompt_2, styles):
    mo.stop(not selected_prompt_1 or not selected_prompt_2, "")

    # Extract placeholders from both prompts
    placeholders_1 = re.findall(r"\{\{(.*?)\}\}", selected_prompt_1)
    placeholders_1 = list(set(placeholders_1))  # Remove duplicates

    placeholders_2 = re.findall(r"\{\{(.*?)\}\}", selected_prompt_2)
    placeholders_2 = list(set(placeholders_2))  # Remove duplicates

    # Combine unique placeholders
    all_placeholders = list(set(placeholders_1 + placeholders_2))

    # Create text areas for all unique placeholders
    placeholder_inputs = [
        mo.ui.text_area(label=ph, placeholder=f"Enter {ph}", full_width=True) for ph in all_placeholders
    ]

    # Create an array of placeholder inputs
    placeholder_array = mo.ui.array(
        placeholder_inputs,
        label="Fill in the Placeholders",
    )

    # Create a 'Generate' button
    proceed_button = mo.ui.run_button(label="Generate Both Prompts")

    # Display the placeholders and the 'Generate' button in a vertical stack
    mo.vstack([mo.md("# Prompt Variables"), placeholder_array, proceed_button]).style(styles["container"])  # type: ignore
    return all_placeholders, placeholder_array, proceed_button


@app.cell
def __(mo, placeholder_array, proceed_button, all_placeholders):
    mo.stop(not placeholder_array.value or not len(placeholder_array.value), "")

    # Check if any values are missing
    if any(not value.strip() for value in placeholder_array.value):
        mo.stop(True, mo.md("**Please fill in all placeholders.**"))

    # Ensure the 'Generate' button has been pressed
    mo.stop(
        not proceed_button.value,
        mo.md("**Please press the 'Generate Both Prompts' button to continue.**"),
    )

    # Map the placeholder names to the values
    filled_values = dict(zip(all_placeholders, placeholder_array.value, strict=False))
    return (filled_values,)


@app.cell
def __(filled_values, selected_prompt_1, selected_prompt_2):
    # Replace placeholders in both prompts
    final_prompt_1 = selected_prompt_1
    final_prompt_2 = selected_prompt_2

    for key, value in filled_values.items():
        final_prompt_1 = final_prompt_1.replace(f"{{{{{key}}}}}", value)
        final_prompt_2 = final_prompt_2.replace(f"{{{{{key}}}}}", value)

    return final_prompt_1, final_prompt_2


@app.cell
def __(
    COMPARE_DIR,
    final_prompt_1,
    final_prompt_2,
    form,
    llm_module,
    mo,
    models,
    question_input,
    styles,
    prompt_library_module,
):
    # Get the selected models
    model_1 = models[form.value["model_dropdown_1"]]  # type: ignore
    model_2 = models[form.value["model_dropdown_2"]]  # type: ignore
    model_name_1 = form.value["model_dropdown_1"]  # type: ignore
    model_name_2 = form.value["model_dropdown_2"]  # type: ignore

    # Run both prompts through their respective models
    with mo.status.spinner(title="Running prompts through models..."):
        prompt_response_1 = llm_module.prompt(model_1, final_prompt_1)
        prompt_response_2 = llm_module.prompt(model_2, final_prompt_2)

    # Display responses side by side
    mo.hstack([
        mo.vstack([
            mo.md(f"# First Prompt Output ({model_name_1})\n\n{prompt_response_1}").style(styles["prompt_display"]),  # type: ignore
        ]),
        mo.vstack([
            mo.md(f"# Second Prompt Output ({model_name_2})\n\n{prompt_response_2}").style(styles["prompt_display"]),  # type: ignore
        ]),
    ]).style(styles["container"])  # type: ignore

    # Create save button and preview
    save_data = {
        "question_input": question_input.value,
        "final_prompt_1": final_prompt_1,
        "prompt_response_1": prompt_response_1,
        "final_prompt_2": final_prompt_2,
        "prompt_response_2": prompt_response_2,
        "model_name_1": model_name_1,
        "model_name_2": model_name_2,
        "styles": styles,
        "COMPARE_DIR": COMPARE_DIR,
    }

    preview = mo.md("")
    save_button = mo.ui.button(
        label="Save Comparison",
        tooltip="Save the comparison to a markdown file with timestamp",
        on_click=lambda: prompt_library_module.save_comparison(mo, save_data, preview, save_button),
    )

    mo.vstack([mo.md("### Save Comparison"), save_button, preview]).style(styles["container"])  # type: ignore

    return (save_data, preview, save_button)


@app.cell
def __(mo, styles):
    mo.md("""# Prompt Analysis Tool

This tool helps you compare different prompts using different LLM models. You can:
1. Select a predefined question or write your own
2. Choose two different prompts and LLM models to compare
3. Fill in any variables required by the prompts
4. Generate and compare responses
5. Save the comparison with timestamps for future reference

The saved comparisons will be stored in the `compare` directory with timestamps in EDT.

### Error Handling

- The tool will display clear error messages if something goes wrong
- Check the error messages for:
- API key issues
- Network connection problems
- File permission errors
- Invalid prompt selections

### File Naming

Saved files will use the format: `YYYY-MM-DD-HH-MM-SS-EDT_comparison.md`""").style(styles["container"])  # type: ignore
    return (None,)


if __name__ == "__main__":
    app.run()

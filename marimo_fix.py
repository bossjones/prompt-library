from __future__ import annotations

import marimo


__generated_with = "0.9.34"
app = marimo.App(width="full")


@app.cell
def __():
    """Initialize required modules and reload prompt library module."""
    import glob
    import importlib  # For module reloading
    import os  # For path operations
    import re  # For regex to extract placeholders

    from datetime import datetime
    from pathlib import Path  # For path handling

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


app._unparsable_cell(
    r"""
    \"\"\"Set up directories and load XML prompts.\"\"\"

    # Define the directories to search for prompts
    QUESTIONS_DIR = (
        \"one-off-tasks/lore-writing/helldivers2/johnhelldiver/questions\"
    )
    COMPARE_DIR = \"one-off-tasks/lore-writing/helldivers2/johnhelldiver/compare\"
    PROMPT_DIRS = [\"./src/prompt_library/data/prompt_lib\", \"./one-off-tasks\"]

    # Ensure directories exist
    try:
        Path(QUESTIONS_DIR).mkdir(parents=True, exist_ok=True)
        Path(COMPARE_DIR).mkdir(parents=True, exist_ok=True)
    except PermissionError:
        mo.md(\"\"\"
        ❌ **Error**: Unable to create directories. Please check permissions.
        \"\"\").style({
            \"color\": \"red\",
            \"padding\": \"10px\",
            \"border-radius\": \"5px\",
            \"background\": \"#ffebee\",
        })
        return COMPARE_DIR, QUESTIONS_DIR, PROMPT_DIRS
    """,
    name="__",
)


@app.cell
def __(Path, mo, os, prompt_library_module):
    """Set up directories and load XML prompts."""
    # Define the directories to search for prompts
    QUESTIONS_DIR = "one-off-tasks/lore-writing/helldivers2/johnhelldiver/questions"
    COMPARE_DIR = "one-off-tasks/lore-writing/helldivers2/johnhelldiver/compare"
    PROMPT_DIRS = ["./src/prompt_library/data/prompt_lib", "./one-off-tasks"]

    # Ensure directories exist
    try:
        Path(QUESTIONS_DIR).mkdir(parents=True, exist_ok=True)
        Path(COMPARE_DIR).mkdir(parents=True, exist_ok=True)
    except PermissionError:
        mo.md("""
        ❌ **Error**: Unable to create directories. Please check permissions.
        """).style({"color": "red", "padding": "10px", "border-radius": "5px", "background": "#ffebee"})

    # Validate prompt directories exist
    missing_dirs = [d for d in PROMPT_DIRS if not os.path.exists(d)]
    if missing_dirs:
        mo.md(f"""
        ⚠️ **Warning**: The following directories were not found:
        ```
        {chr(10).join(missing_dirs)}
        ```
        Some prompts may not be available.
        """).style({"color": "orange", "padding": "10px", "border-radius": "5px", "background": "#fff3e0"})

    # Convert to Path objects and load prompts from all directories, filtering for XML files
    try:
        with mo.status.spinner(title="Loading XML prompts from all directories..."):
            map_prompt_library: dict = prompt_library_module.pull_in_multiple_prompt_libraries(
                directories=[Path(d) for d in PROMPT_DIRS], file_type="xml"
            )
    except Exception as e:
        mo.md(f"""
        ❌ **Error**: Failed to load XML prompts:
        ```
        {e!s}
        ```
        """).style({"color": "red", "padding": "10px", "border-radius": "5px", "background": "#ffebee"})

    if not map_prompt_library:
        mo.md("""
        ❌ **Error**: No XML prompts were loaded. Please check that:
        1. The directories exist and are accessible
        2. They contain valid XML prompt files
        """).style({"color": "red", "padding": "10px", "border-radius": "5px", "background": "#ffebee"})
    else:
        mo.md(f"""
        ✅ Successfully loaded **{len(map_prompt_library)}** XML prompts from:
        ```
        {chr(10).join(d for d in PROMPT_DIRS if os.path.exists(d))}
        ```
        """).style({"color": "green", "padding": "10px", "border-radius": "5px", "background": "#e8f5e9"})

    return (
        COMPARE_DIR,
        PROMPT_DIRS,
        QUESTIONS_DIR,
        map_prompt_library,
        missing_dirs,
    )


app._unparsable_cell(
    r"""
    \"\"\"Initialize LLM models.

    Returns:
        dict[str, Any] | None: Dictionary of initialized LLM models or None if initialization fails
    \"\"\"
    try:
        # Initialize LLM models
        llm_o1_mini, llm_o1_preview = llm_module.build_o1_series()
        llm_gpt_4o_latest, llm_gpt_4o_mini = llm_module.build_openai_latest_and_fastest()

        models = {
            \"gpt-4o-latest\": llm_gpt_4o_latest,  # Move to top for default selection
            \"o1-mini\": llm_o1_mini,
            \"o1-preview\": llm_o1_preview,
            \"gpt-4o-mini\": llm_gpt_4o_mini,
        }
        return models
    except Exception as e:
        # Create error message using mo parameter
        mo.md(f\"\"\"
        ❌ **Error**: Failed to initialize LLM models:
        ```
        {str(e)}
        ```
        Please check your API keys and network connection.
        \"\"\").style({\"color\": \"red\", \"padding\": \"10px\", \"border-radius\": \"5px\", \"background\": \"#ffebee\"})
    """,
    name="__",
)


@app.cell
def __(QUESTIONS_DIR, glob, mo, os):
    # Get list of markdown files in questions directory
    question_files = glob.glob(os.path.join(QUESTIONS_DIR, "*.md"))
    question_names = ["None"] + [os.path.basename(f) for f in question_files]

    # Create dropdown for question selection
    question_selector = mo.ui.dropdown(
        options=question_names, value="None", label="Select a predefined question (or None to write your own)"
    )

    # Create text area for question input
    question_input = mo.ui.text_area(value="", placeholder="Enter your question here...", label="Question")

    # Function to read markdown file content
    def read_question_file(filename):
        if filename == "None":
            return ""
        file_path = os.path.join(QUESTIONS_DIR, filename)
        with open(file_path) as f:
            return f.read().strip()

    # Update text area when selection changes
    if question_selector.value != "None":
        question_input.value = read_question_file(question_selector.value)

    mo.md("### Question Input")
    mo.hstack([question_selector, question_input])
    return (
        question_files,
        question_input,
        question_names,
        question_selector,
        read_question_file,
    )


@app.cell
def __(map_prompt_library, mo, models):
    """Create UI components for prompt and model selection."""
    # Stop if no prompts were loaded
    mo.stop(
        not map_prompt_library,
        mo.md("""
    ❌ **Error**: No prompts are available to display. Please check the error messages above.
    """).style({"color": "red", "padding": "10px", "border-radius": "5px", "background": "#ffebee"}),
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
    )
    form
    return (
        form,
        model_dropdown_1,
        model_dropdown_2,
        prompt_dropdown_1,
        prompt_dropdown_2,
    )


@app.cell
def __(form, map_prompt_library, mo, prompt_styles):
    """Display selected prompts side by side."""
    mo.stop(not form.value or not len(form.value), "")

    # Get first prompt
    selected_prompt_name_1 = form.value["prompt_dropdown_1"]
    selected_prompt_1 = map_prompt_library[selected_prompt_name_1]

    # Get second prompt
    selected_prompt_name_2 = form.value["prompt_dropdown_2"]
    selected_prompt_2 = map_prompt_library[selected_prompt_name_2]

    # Display prompts side by side
    mo.hstack([
        mo.vstack([
            mo.md("# First Selected Prompt"),
            mo.accordion({"### Click to show": mo.md(f"```xml\n{selected_prompt_1}\n```").style(prompt_styles)}),
        ]),
        mo.vstack([
            mo.md("# Second Selected Prompt"),
            mo.accordion({"### Click to show": mo.md(f"```xml\n{selected_prompt_2}\n```").style(prompt_styles)}),
        ]),
    ])
    return (
        selected_prompt_1,
        selected_prompt_2,
        selected_prompt_name_1,
        selected_prompt_name_2,
    )


@app.cell
def __(mo, re, selected_prompt_1, selected_prompt_2):
    """Extract and handle placeholders from both prompts."""
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
    mo.vstack([mo.md("# Prompt Variables"), placeholder_array, proceed_button])
    return (
        all_placeholders,
        placeholder_array,
        placeholder_inputs,
        placeholders_1,
        placeholders_2,
        proceed_button,
    )


@app.cell
def __(all_placeholders, mo, placeholder_array, proceed_button):
    """Validate placeholder inputs and create filled values dictionary."""
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
    """Replace placeholders in both prompts with filled values."""
    # Replace placeholders in both prompts
    final_prompt_1 = selected_prompt_1
    final_prompt_2 = selected_prompt_2

    for key, value in filled_values.items():
        final_prompt_1 = final_prompt_1.replace(f"{{{{{key}}}}}", value)
        final_prompt_2 = final_prompt_2.replace(f"{{{{{key}}}}}", value)
    return final_prompt_1, final_prompt_2, key, value


@app.cell
def __(
    COMPARE_DIR,
    Path,
    datetime,
    final_prompt_1,
    final_prompt_2,
    form,
    llm_module,
    mo,
    models,
    pytz,
    question_input,
):
    """Process prompts through LLM models and handle saving functionality."""
    # Get the selected models
    try:
        model_1 = models[form.value["model_dropdown_1"]]
        model_2 = models[form.value["model_dropdown_2"]]
        model_name_1 = form.value["model_dropdown_1"]
        model_name_2 = form.value["model_dropdown_2"]
    except (KeyError, AttributeError) as e:
        mo.md(f"""
        ❌ **Error**: Failed to get selected models:
        ```
        {e!s}
        ```
        Please ensure models are properly selected.
        """).style({"color": "red", "padding": "10px", "border-radius": "5px", "background": "#ffebee"})

    # Run both prompts through their respective models
    try:
        with mo.status.spinner(title="Running prompts through models..."):
            prompt_response_1 = llm_module.prompt(model_1, final_prompt_1)
            prompt_response_2 = llm_module.prompt(model_2, final_prompt_2)
    except Exception as e:
        mo.md(f"""
        ❌ **Error**: Failed to generate responses:
        ```
        {e!s}
        ```
        Please check your API keys and network connection.
        """).style({"color": "red", "padding": "10px", "border-radius": "5px", "background": "#ffebee"})

    # Display responses side by side
    mo.hstack([
        mo.vstack([
            mo.md(f"# First Prompt Output ({model_name_1})\n\n{prompt_response_1}").style({
                "background": "#eee",
                "padding": "10px",
                "border-radius": "10px",
                "width": "50%",
            }),
        ]),
        mo.vstack([
            mo.md(f"# Second Prompt Output ({model_name_2})\n\n{prompt_response_2}").style({
                "background": "#eee",
                "padding": "10px",
                "border-radius": "10px",
                "width": "50%",
            }),
        ]),
    ])

    # Create save button and preview
    save_button = mo.ui.button("Save Comparison", tooltip="Save the comparison to a markdown file with timestamp")
    preview = mo.md("")

    @save_button.click
    def save_comparison():
        try:
            # Get current time in EDT
            edt = pytz.timezone("America/New_York")
            now = datetime.now(edt)
            timestamp = now.strftime("%Y-%m-%d-%H-%M-%S-%Z")

            # Generate markdown content
            content = f"""# Prompt Comparison - {now.strftime("%Y-%m-%d %H:%M:%S %Z")}

    ## Original Question
    ```
    {question_input.value}
    ```

    ## First Prompt (Model: {model_name_1})
    ```xml
    {final_prompt_1}
    ```

    ### Generated Response
    ```
    {prompt_response_1}
    ```

    ## Second Prompt (Model: {model_name_2})
    ```xml
    {final_prompt_2}
    ```

    ### Generated Response
    ```
    {prompt_response_2}
    ```
    """

            # Update preview
            preview.value = f"""### Preview of file to be saved:
    ```markdown
    {content}
    ```"""

            # Save file
            filename = f"{timestamp}_comparison.md"
            filepath = Path(COMPARE_DIR) / filename

            try:
                filepath.write_text(content)
                # Show success message
                preview.value += f"\n\n✅ Saved to: {filepath}"
            except (PermissionError, OSError) as e:
                preview.value += f"\n\n❌ **Error**: Failed to save file: {e!s}"

        except Exception as e:
            preview.value = f"""### ❌ Error
    Failed to generate comparison:
    ```
    {e!s}
    ```"""

    mo.md("### Save Comparison")
    mo.vstack([save_button, preview])
    return (
        model_1,
        model_2,
        model_name_1,
        model_name_2,
        preview,
        prompt_response_1,
        prompt_response_2,
        save_button,
        save_comparison,
    )


@app.cell
def __(mo):
    """Display tool documentation and instructions."""
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
    Saved files will use the format: `YYYY-MM-DD-HH-MM-SS-EDT_comparison.md`""")
    return


if __name__ == "__main__":
    app.run()

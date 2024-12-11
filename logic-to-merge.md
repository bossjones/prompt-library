# Marimo Notebook Syntax Errors Guide

Based on analyzing the working and broken examples, here are the key syntax patterns and errors specific to Marimo notebooks:

## 1. Cell Function Definition

### ✅ Correct Pattern
```python
@app.cell
def __():
    """Docstring describing cell purpose."""
    # Code here
    return (var1, var2)  # Explicit tuple return
```

### ❌ Common Errors
- Missing return statement
- Return statement outside function
- Implicit returns without parentheses
- Missing docstring

## 2. State Management

### ✅ Correct Pattern
```python
@app.cell
def __(dependency1, dependency2):
    """Cell with dependencies."""
    result = process(dependency1, dependency2)
    return (result,)  # Note the comma for single-item tuple
```

### ❌ Common Errors
- Accessing variables not returned by previous cells
- Mutating shared state between cells
- Missing dependency injection in function parameters

## 3. UI Component Reactivity

### ✅ Correct Pattern
From working example:

```75:89:mariomo_multi_language_model_ranker.py
            "gpt-4o-mini",
        ],
    )
    return model_multiselect, prompt_multiselect, prompt_temp_slider


@app.cell
def __():
    prompt_style = {
        "background": "#eee",
        "padding": "10px",
        "border-radius": "10px",
        "margin-bottom": "20px",
    }
    return (prompt_style,)
```


### ❌ Common Errors
- Updating UI components outside their defining cells
- Direct mutation of UI state
- Missing reactive dependencies

## 4. Error Handling

### ✅ Correct Pattern
From working example:

````420:449:marimo_prompt_analysis.py
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
        {str(e)}
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
        {str(e)}
        ```
        Please check your API keys and network connection.
        """).style({"color": "red", "padding": "10px", "border-radius": "5px", "background": "#ffebee"})
````


### ❌ Common Errors
- Uncaught exceptions affecting notebook state
- Missing mo.stop() guards
- Improper error message formatting

## 5. Cell Dependencies

### ✅ Correct Pattern
```python
@app.cell
def __(form, mo):
    mo.stop(not form.value, "")  # Guard clause
    # Process form data
    return (processed_data,)
```

### ❌ Common Errors
- Circular dependencies between cells
- Missing dependency declarations
- Improper dependency ordering

## Few-Shot Examples

### Example 1: State Management
```python
# ❌ Broken
@app.cell
def __():
    data = process_data()
    return data  # Missing tuple wrapping

# ✅ Fixed
@app.cell
def __():
    """Process data and return results."""
    data = process_data()
    return (data,)
```

### Example 2: UI Updates
```python
# ❌ Broken
@app.cell
def __(selector):
    if selector.value:
        input_field.value = new_value  # Direct mutation

# ✅ Fixed
@app.cell
def __(selector, input_field):
    """Update input field based on selector."""
    if selector.value:
        return (input_field.set(new_value),)
```

## Key Differences from Regular Python

1. Cell Isolation: Each cell must be self-contained with explicit dependencies
2. State Flow: All state changes must be handled through return values
3. Reactive Updates: UI components must be updated through the reactive system
4. Error Boundaries: Each cell needs proper error handling and guards
5. Return Format: Always return tuples, even for single values

This guide can be used to improve cursor rules by identifying patterns that distinguish between working and broken Marimo notebook code.

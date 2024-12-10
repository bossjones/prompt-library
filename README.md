# Prompt Library

This repository contains a structured collection of prompts for various AI tasks.

## Structure

- `agents/`: Prompts for continuous use in agentic systems
  - `creative/`: Prompts for creative tasks
    - `image-generation/`: Prompts for generating images
    - `fabrication/`: Prompts for creating fabricated content
    - `story-generation/`: Prompts for generating stories
    - `quote-generation/`: Prompts for generating quotes
  - `engineering/`: Prompts for engineering tasks
    - `code-generation/`: Prompts for generating code
    - `code-review/`: Prompts for reviewing code
    - `bug-finding/`: Prompts for identifying bugs
    - `style-enforcement/`: Prompts for enforcing coding style

- `one-off-tasks/`: Prompts for single-use scenarios
  - `image-generation/`: One-time image generation prompts
  - `lore-writing/`: Prompts for writing lore and backstories
  - `code-generation/`: One-time code generation prompts
  - `code-review/`: One-time code review prompts

- `templates/`: Reusable prompt structures and templates

## Folder Layout Details

### Core Directories

- `agents/`: Contains prompts designed for continuous use in automated systems
  - Each subdirectory focuses on specific types of tasks (creative or engineering)
  - Includes standardized prompt formats for consistent output

- `one-off-tasks/`: Houses prompts intended for single-use scenarios
  - Each subdirectory contains task-specific prompts
  - Example: `lore-writing/helldivers2/johnhelldiver/` shows a complete prompt structure with:
    - `prompt.xml`: The actual prompt definition
    - `README.md`: Usage instructions and context
    - `metadata.json`: Technical details about the prompt
    - `examples/`: Sample outputs and use cases

- `templates/`: Contains reusable structures for creating new prompts
  - `prompt_template.xml`: Base structure for XML prompts
  - `readme_template.md`: Template for prompt documentation
  - `metadata_template.json`: Standard metadata format

### Key Files

- `prompt_schema.xsd`: XML schema definition for validating prompt structure
- `.gitignore`: Specifies which files Git should ignore
- `Justfile`: Contains automation commands for common tasks
- `pyproject.toml`: Python project configuration and tool settings

### Documentation

Each directory contains its own `README.md` that explains:
- Purpose of that prompt category
- Expected inputs/outputs
- Special considerations
- Usage examples

## Usage

1. Navigate to the appropriate category for your task
2. Use existing prompts as templates or create new ones following the established structure
3. Each prompt should include:
   - Clear context and purpose
   - Specific instructions
   - Example inputs/outputs where applicable
   - Metadata about usage and performance

## Contributing

When adding new prompts:
1. Use the appropriate template from the `templates/` directory
2. Include comprehensive documentation
3. Add examples of successful outputs
4. Update metadata with relevant information

## License

[Insert License Information]


## Schema

The schema for the prompts is defined in `prompt_schema.xsd`.


To create an XML linting schema that checks for specific blocks to be defined, you can use XML Schema Definition (XSD). Here's how you can structure your XSD to enforce the presence of certain elements:

## Schema Structure

Your XSD should define a root element and then specify the required child elements using the `xs:element` tag. Here's a basic structure:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">
  <xs:element name="root">
    <xs:complexType>
      <xs:sequence>
        <xs:element name="block1" minOccurs="1" maxOccurs="1">
          <xs:complexType>
            <!-- Define content for block1 -->
          </xs:complexType>
        </xs:element>
        <xs:element name="block2" minOccurs="1" maxOccurs="1">
          <xs:complexType>
            <!-- Define content for block2 -->
          </xs:complexType>
        </xs:element>
        <!-- Add more blocks as needed -->
      </xs:sequence>
    </xs:complexType>
  </xs:element>
</xs:schema>
```

## Key Components

1. **Root Element**: Define the root element of your XML document.

2. **Required Blocks**: Use `minOccurs="1"` to specify that an element must appear at least once.

3. **Element Order**: The `xs:sequence` tag ensures that child elements appear in the specified order.

4. **Content Definition**: Within each `xs:complexType`, define the structure and content allowed for that block.

## Example

Let's say you want to check for the presence of "purpose", "instructions", and "examples" blocks:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">
  <xs:element name="prompt-library">
    <xs:complexType>
      <xs:sequence>
        <xs:element name="purpose" minOccurs="1" maxOccurs="1" type="xs:string"/>
        <xs:element name="instructions" minOccurs="1" maxOccurs="1">
          <xs:complexType>
            <xs:sequence>
              <xs:element name="instruction" minOccurs="1" maxOccurs="unbounded" type="xs:string"/>
            </xs:sequence>
          </xs:complexType>
        </xs:element>
        <xs:element name="examples" minOccurs="1" maxOccurs="1">
          <xs:complexType>
            <xs:sequence>
              <xs:element name="example" minOccurs="1" maxOccurs="unbounded" type="xs:string"/>
            </xs:sequence>
          </xs:complexType>
        </xs:element>
      </xs:sequence>
    </xs:complexType>
  </xs:element>
</xs:schema>
```

This schema ensures that:

1. The root element is `prompt-library`.
2. It contains exactly one `purpose` element.
3. It contains exactly one `instructions` element, which must have one or more `instruction` child elements.
4. It contains exactly one `examples` element, which must have one or more `example` child elements.

To use this schema for linting, you would reference it in your XML file and use an XML validator to check compliance[1][2][3].

Citations:
[1] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/39473573/5da19758-6a8e-42fa-9a2e-5dc9e6ccaf67/paste.txt
[2] https://learn.microsoft.com/th-th/dotnet/standard/data/xml/reading-and-writing-xml-schemas
[3] https://learn.microsoft.com/en-us/dotnet/standard/data/xml/xml-schema-xsd-validation-with-xmlschemaset
[4] https://www.oracle.com/technical-resources/articles/srivastava-structures.html
[5] https://www.w3schools.com/xml/schema_example.asp
[6] https://www.w3.org/TR/xmlschema-1/


## How to use xml schema to lint

To use your XSD schema with xmllint, follow these steps:

1. Save the XSD schema:
   Save your XSD schema with a `.xsd` file extension, for example `prompt_schema.xsd`.

2. Use xmllint for validation:
   Open a terminal and use the following command to validate your XML file against the XSD schema:

   ```bash
   xmllint --schema prompt_schema.xsd your_xml_file.xml --noout
   ```

   Replace `prompt_schema.xsd` with the actual name of your schema file and `your_xml_file.xml` with the name of the XML file you want to validate.

3. Interpret the results:
   - If the XML is valid according to the schema, xmllint will output: `your_xml_file.xml validates`
   - If there are validation errors, xmllint will display error messages indicating where the XML fails to meet the schema requirements

4. Optional: Reference the schema in your XML file:
   You can also reference the XSD schema directly in your XML file by adding the following attributes to the root element:

   ```xml
   <prompt-library xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                   xsi:noNamespaceSchemaLocation="prompt_schema.xsd">
   ```

   This allows some XML editors to provide real-time validation and auto-completion based on the schema.

Remember to ensure that both the XSD file and the XML file are in the same directory when running the xmllint command, or provide the full path to the files[1].

Citations:
[1] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/39473573/5da19758-6a8e-42fa-9a2e-5dc9e6ccaf67/paste.txt


# Inspiration

## IndyDevDan's Youtube Video: OpenAI's o1 Reasoning Models: A Deep Dive

Video Link: https://www.youtube.com/watch?v=GUVrOa4V8iE

Also see: https://www.youtube.com/watch?v=ujnLJru2LIs

### Introduction

OpenAI has released new reasoning models, o1-preview and o1-mini, which incorporate prompt chaining and chain of thought techniques. These models offer advanced capabilities but require a different approach to prompt engineering[1][2].

### Key Points

#### Model Comparison
- The video demonstrates o1-preview vs Claude 3.5 in generating YouTube chapters[1][2].

#### Setup and Tools
- Simon Willison's CLI LLM library is used to set up and work with o1-mini[1][2].

#### Practical Applications
1. **AI Coding Meta Review**: Showcases o1-preview's capabilities in code analysis[1][2].
2. **Hacker News Sentiment Analysis**: Demonstrates o1-preview's ability to analyze sentiment on the platform[1][2].

#### Challenges and Considerations
- The o1 models are described as "NOT easy to use," indicating a learning curve for effective implementation[1][2].

#### Future Implications
- The video concludes with a discussion on the future of reasoning models and their potential impact[1][2].

#### Resources
The video description provides a comprehensive list of resources for further exploration, including Simon Willison's articles and tools, OpenAI documentation, and related discussions[1][2].

Citations:
[1] https://www.youtube.com/watch?v=GUVrOa4V8iE
[2] https://www.youtube.com/watch?v=GUVrOa4V8iE

---------------------

# Marimo Reactive Notebook Prompt Library
> Starter codebase to use Marimo reactive notebooks to build a reusable, customizable, Prompt Library.
>
> Take this codebase and use it as a starter codebase to build your own personal prompt library.
>
> Marimo reactive notebooks & Prompt Library [walkthrough](https://youtu.be/PcLkBkQujMI)
>
> Run multiple prompts against multiple models (SLMs & LLMs) [walkthrough](https://youtu.be/VC6QCEXERpU)

<img src="./images/multi_slm_llm_prompt_and_model.png" alt="multi llm prompting" style="max-width: 750px;">

<img src="./images/marimo_prompt_library.png" alt="marimo promptlibrary" style="max-width: 750px;">

## 1. Understand Marimo Notebook
> This is a simple demo of the Marimo Reactive Notebook
- Install hyper modern [UV Python Package and Project](https://docs.astral.sh/uv/getting-started/installation/)
- Install dependencies `uv sync`
- Install marimo `uv pip install marimo`
- To Edit, Run `uv run marimo edit marimo_is_awesome_demo.py`
- To View, Run `uv run marimo run marimo_is_awesome_demo.py`
- Then use your favorite IDE & AI Coding Assistant to edit the `marimo_is_awesome_demo.py` directly or via the UI.

## 2. Ad-hoc Prompt Notebook
> Quickly run and test prompts across models
- 🟡 Copy `.env.sample` to `.env` and set your keys (minimally set `OPENAI_API_KEY`)
    - Add other keys and update the notebook to add support for additional SOTA LLMs
- 🟡 Install Ollama (https://ollama.ai/) and pull the models you want to use
    - Update the notebook to use Ollama models you have installed
- To Edit, Run `uv run marimo edit adhoc_prompting.py`
- To View, Run `uv run marimo run adhoc_prompting.py`

## 3. ⭐️ Prompt Library Notebook
> Build, Manage, Reuse, Version, and Iterate on your Prompt Library
- 🟡 Copy `.env.sample` to `.env` and set your keys (minimally set `OPENAI_API_KEY`)
    - Add other keys and update the notebook to add support for additional SOTA LLMs
- 🟡 Install Ollama (https://ollama.ai/) and pull the models you want to use
    - Update the notebook to use Ollama models you have installed
- To Edit, Run `uv run marimo edit prompt_library.py`
- To View, Run `uv run marimo run prompt_library.py`

## 4. Multi-LLM Prompt
> Quickly test a single prompt across multiple language models
- 🟡 Ensure your `.env` file is set up with the necessary API keys for the models you want to use
- 🟡 Install Ollama (https://ollama.ai/) and pull the models you want to use
    - Update the notebook to use Ollama models you have installed
- To Edit, Run `uv run marimo edit multi_llm_prompting.py`
- To View, Run `uv run marimo run multi_llm_prompting.py`

## 5. Multi Language Model Ranker
> Compare and rank multiple language models across various prompts
- 🟡 Ensure your `.env` file is set up with the necessary API keys for the models you want to compare
- 🟡 Install Ollama (https://ollama.ai/) and pull the models you want to use
    - Update the notebook to use Ollama models you have installed
- To Edit, Run `uv run marimo edit multi_language_model_ranker.py`
- To View, Run `uv run marimo run multi_language_model_ranker.py`

## General Usage
> See the [Marimo Docs](https://docs.marimo.io/index.html) for general usage details

## Personal Prompt Library Use-Cases
- Ad-hoc prompting
- Prompt reuse
- Prompt versioning
- Interactive prompts
- Prompt testing & Benchmarking
- LLM comparison
- Prompt templating
- Run a single prompt against multiple LLMs & SLMs
- Compare multi prompts against multiple LLMs & SLMs
- Anything you can imagine!

## Advantages of Marimo

### Key Advantages
> Rapid Prototyping: Seamlessly transition between user and builder mode with `cmd+.` to toggle. Consumer vs Producer. UI vs Code.

> Interactivity: Built-in reactive UI elements enable intuitive data exploration and visualization.

> Reactivity: Cells automatically update when dependencies change, ensuring a smooth and efficient workflow.

> Out of the box: Use sliders, textareas, buttons, images, dataframe GUIs, plotting, and other interactive elements to quickly iterate on ideas.

> It's 'just' Python: Pure Python scripts for easy version control and AI coding.


- **Reactive Execution**: Run one cell, and marimo automatically updates all affected cells. This eliminates the need to manually manage notebook state.
- **Interactive Elements**: Provides reactive UI elements like dataframe GUIs and plots, making data exploration fast and intuitive.
- **Python-First Design**: Notebooks are pure Python scripts stored as `.py` files. They can be versioned with git, run as scripts, and imported into other Python code.
- **Reproducible by Default**: Deterministic execution order with no hidden state ensures consistent and reproducible results.
- **Built for Collaboration**: Git-friendly notebooks where small changes yield small diffs, facilitating collaboration.
- **Developer-Friendly Features**: Includes GitHub Copilot, autocomplete, hover tooltips, vim keybindings, code formatting, debugging panels, and extensive hotkeys.
- **Seamless Transition to Production**: Notebooks can be run as scripts or deployed as read-only web apps.
- **Versatile Use Cases**: Ideal for experimenting with data and models, building internal tools, communicating research, education, and creating interactive dashboards.

### Advantages Over Jupyter Notebooks

- **Reactive Notebook**: Automatically updates dependent cells when code or values change, unlike Jupyter where cells must be manually re-executed.
- **Pure Python Notebooks**: Stored as `.py` files instead of JSON, making them easier to version control, lint, and integrate with Python tooling.
- **No Hidden State**: Deleting a cell removes its variables and updates affected cells, reducing errors from stale variables.
- **Better Git Integration**: Plain Python scripts result in smaller diffs and more manageable version control compared to Jupyter's JSON format.
- **Import Symbols**: Allows importing symbols from notebooks into other notebooks or Python files.
- **Enhanced Interactivity**: Built-in reactive UI elements provide a more interactive experience than standard Jupyter widgets.
- **App Deployment**: Notebooks can be served as web apps or exported to static HTML for easier sharing and deployment.
- **Advanced Developer Tools**: Features like code formatting, GitHub Copilot integration, and debugging panels enhance the development experience.
- **Script Execution**: Can be executed as standard Python scripts, facilitating integration into pipelines and scripts without additional tools.

## Resources
- https://docs.astral.sh/uv/
- https://docs.marimo.io/index.html
- https://youtu.be/PcLkBkQujMI
- https://github.com/BuilderIO/gpt-crawler
- https://github.com/simonw/llm
- https://ollama.com/
- https://ai.meta.com/blog/llama-3-2-connect-2024-vision-edge-mobile-devices/
- https://qwenlm.github.io/

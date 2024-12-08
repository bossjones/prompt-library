# Project Layout

[Proplexity convo](https://www.perplexity.ai/search/prompt-libraries-are-important-bLFPTdLIToqyCGM6oMADng)

## Updated Folder Structure

```
prompt-library/
│
├── agents/
│   ├── creative/
│   │   ├── image-generation/
│   │   ├── fabrication/
│   │   ├── story-generation/
│   │   └── quote-generation/
│   │
│   └── engineering/
│       ├── code-generation/
│       ├── code-review/
│       ├── bug-finding/
│       └── style-enforcement/
│
├── one-off-tasks/
│   ├── image-generation/
│   ├── lore-writing/
│   │   └── helldivers2/
│   │       └── johnhelldiver/
│   │           ├── prompt.xml
│   │           ├── README.md
│   │           ├── metadata.json
│   │           └── examples/
│   │               ├── example1.md
│   │               └── example2.md
│   ├── code-generation/
│   └── code-review/
│
├── templates/
│   ├── prompt_template.xml
│   ├── readme_template.md
│   └── metadata_template.json
│
└── README.md
```

## Step-by-Step Explanation

1. **Standardized Prompt Folder Structure**: For each specific prompt (e.g., johnhelldiver), create a folder with the following contents:
   - `prompt.xml`: The actual prompt in XML format
   - `README.md`: Detailed explanation of the prompt
   - `metadata.json`: Technical metadata about the prompt
   - `examples/`: Folder containing example outputs

2. **prompt.xml**: Use XML format for structured prompt storage. This allows for easy parsing and potential automation.

3. **README.md**: Create a detailed markdown file explaining:
   - Purpose of the prompt
   - Expected input/output
   - Any special instructions or considerations
   - Brief description of the character or concept (for lore prompts)

4. **metadata.json**: Include technical details such as:
   - Target model (e.g., "GPT-4", "DALL-E 2")
   - Version of the prompt
   - Creation date
   - Last tested date
   - Author
   - Tags for searchability

5. **examples/**: Store example outputs in markdown files, linking to the specific version of the prompt used.

6. **Templates**: Create template files in the `templates/` folder for:
   - `prompt_template.xml`: Standard structure for prompts
   - `readme_template.md`: Consistent README format
   - `metadata_template.json`: Standard metadata fields

7. **Root README.md**: Update the main README to include:
   - Overview of the library structure
   - Instructions for using templates
   - Guidelines for contributing new prompts
   - Best practices for prompt creation and testing

## Implementation Steps

1. **Create Templates**:
   - Develop standardized templates for `prompt.xml`, `README.md`, and `metadata.json`.
   - Store these in the `templates/` folder.

2. **Implement for Existing Prompts**:
   - Start with the `johnhelldiver` example.
   - Create the folder structure as outlined.
   - Fill in the `prompt.xml`, `README.md`, and `metadata.json` using the templates.
   - Add example outputs to the `examples/` folder.

3. **Establish Naming Conventions**:
   - Use lowercase with hyphens for folder names (e.g., `john-helldiver`).
   - Consistently name files (`prompt.xml`, `README.md`, `metadata.json`).

4. **Version Control**:
   - Use Git tags to mark different versions of prompts.
   - Reference these tags in the `metadata.json` file.

5. **Testing Protocol**:
   - Establish a testing procedure for prompts.
   - Update the `metadata.json` with the last tested date and results.

6. **Documentation**:
   - Create a detailed guide in the root README.md explaining the structure and how to use/contribute to the library.

7. **Automation**:
   - Consider creating scripts to:
     - Generate new prompt folders from templates
     - Validate the structure and presence of required files
     - Update metadata automatically (e.g., version numbers)

## Additional Suggestions

1. **Prompt Chaining**: For complex tasks, consider creating a system for chaining prompts together. This could involve a special XML tag in `prompt.xml` that references other prompts.

2. **Feedback Loop**: Implement a system for users to provide feedback on prompt effectiveness, possibly through GitHub issues or a custom feedback form.

3. **Performance Metrics**: Include a section in `metadata.json` for tracking performance metrics of the prompt (e.g., success rate, average output quality).

4. **Localization**: If relevant, consider adding support for multiple languages, with separate `prompt.xml` files for each language.

5. **API Integration**: If you plan to use these prompts programmatically, consider creating a simple API or library that can load and use prompts directly from your repository structure.

By implementing this expanded strategy, you'll create a robust, scalable, and user-friendly prompt library. The standardized structure and metadata will make it easier to manage, use, and improve your prompts over time, while the templates and potential automation will streamline the process of adding new prompts to the library.

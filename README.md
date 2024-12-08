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

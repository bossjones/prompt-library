# Four Level framework for prompt engineering
> Watch the breakdown here in a [Q4 2024 prompt engineering update video](https://youtu.be/ujnLJru2LIs)
>
> [LLM library](https://github.com/simonw/llm)
>
> [Ollama](https://ollama.com/)

## Level 1: Ad hoc prompt
- Quick, natural language prompts for rapid prototyping
- Perfect for exploring model capabilities and behaviors
- Can be run across multiple models for comparison
- Great for one-off tasks and experimentation

## Level 2: Structured prompt
- Reusable prompts with clear purpose and instructions
- Uses XML/structured format for better model performance
- Contains static variables that can be modified
- Solves well-defined, repeatable problems

## Level 3: Structured prompt with example output
- Builds on Level 2 by adding example outputs
- Examples guide the model to produce specific formats
- Increases consistency and reliability of outputs
- Perfect for when output format matters

## Level 4: Structured prompt with dynamic content
- Production-ready prompts with dynamic variables
- Can be integrated into code and applications
- Infinitely scalable through programmatic updates
- Foundation for building AI-powered tools and agents

# Link:

https://gist.github.com/disler/308edf5cc5df664e72fe9a490836d62e


`level_1_prompt_summarize.xml`:

```xml
Summarize the content with 3 hot takes biased toward the author and 3 hot takes biased against the author

...paste content here...
```

`level_2_prompt_summarize.xml`:

```xml
<purpose>
    Summarize the given content based on the instructions and example-output
</purpose>

<instructions>
   <instruction>Output in markdown format</instruction>
   <instruction>Summarize into 4 sections: High level summary, Main Points, Sentiment, and 3 hot takes biased toward the author and 3 hot takes biased against the author</instruction>
   <instruction>Write the summary in the same format as the example-output</instruction>
</instructions>

<content>
    {...} <<< update this manually
</content>
```

`level_3_prompt_summarize.xml`:


```xml
<purpose>
    Summarize the given content based on the instructions and example-output
</purpose>

<instructions>
   <instruction>Output in markdown format</instruction>
   <instruction>Summarize into 4 sections: High level summary, Main Points, Sentiment, and 3 hot takes biased toward the author and 3 hot takes biased against the author</instruction>
   <instruction>Write the summary in the same format as the example-output</instruction>
</instructions>

<example-output>

    # Title

    ## High Level Summary
    ...

    ## Main Points
    ...

    ## Sentiment
    ...

    ## Hot Takes (biased toward the author)
    ...

    ## Hot Takes (biased against the author)
    ...
</example-output>

<content>
    {...} <<< update this manually
</content>
```

`level_4_prompt_summarize.xml`:

```xml
<purpose>
    Summarize the given content based on the instructions and example-output
</purpose>

<instructions>
   <instruction>Output in markdown format</instruction>
   <instruction>Summarize into 4 sections: High level summary, Main Points, Sentiment, and 3 hot takes biased toward the author and 3 hot takes biased against the author</instruction>
   <instruction>Write the summary in the same format as the example-output</instruction>
</instructions>

<example-output>

    # Title

    ## High Level Summary
    ...

    ## Main Points
    ...

    ## Sentiment
    ...

    ## Hot Takes (biased toward the author)
    ...

    ## Hot Takes (biased against the author)
    ...
</example-output>

<content>
    {{content}} <<< update this dynamically with code
</content>
```


`vscode_structured_prompt_code_snippet.code-snippet`:

```json
{
  "XML Prompt Block 1": {
		"prefix": "px1",
		"body": [
			"<purpose>",
			"    $1",
			"</purpose>",
			"",
			"<instructions>",
			"   <instruction>$2</instruction>",
			"   <instruction>$3</instruction>",
			"   <instruction>$4</instruction>",
			"</instructions>",
			"",
			"<${5:block1}>",
			"$6",
			"</${5:block1}>"
		],
		"description": "Generate XML prompt block with instructions and block1"
	},
  "XML Tag Snippet Inline": {
		"prefix": "xxi",
		"body": [
			"<${1:tag}>$2</${1:tag}>",
		],
		"description": "Create an XML tag with a customizable tag name and content"
	}
}
```

https://gist.github.com/disler/308edf5cc5df664e72fe9a490836d62e



```
<?xml version="1.0" encoding="UTF-8"?>
<prompt xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:noNamespaceSchemaLocation="prompt_schema.xsd">
    <purpose>You are a skilled lore writer for the Helldivers 2 universe. Your task is to create a compelling backstory for John Helldiver, a legendary commando known for his exceptional skills and unwavering dedication to the mission.</purpose>

    <instructions>
        <instruction>Write a brief but engaging backstory for John Helldiver, highlighting his:</instruction>
        <instruction>1. Origin and early life</instruction>
        <instruction>2. Key missions and accomplishments</instruction>
        <instruction>3. Unique personality traits</instruction>
        <instruction>4. Signature weapons or equipment</instruction>
        <instruction>5. Relationships with other Helldivers or characters</instruction>
        <instruction><![CDATA[6. Think before you write the backstory in <thinking></thinking> tags. Think through what you already know about the Helldivers universe.]]></instruction>
        <instruction><![CDATA[7. Provide your answer in <answer></answer> tags.]]></instruction>
    </instructions>

    <examples>
        <example>
          <answer>
          Here's an example of a brief backstory for another character:
          Sarah "Stormbreaker" Chen, born on a remote Super Earth colony, joined the Helldivers at 18 after her home was destroyed by Terminid forces. Known for her unparalleled skill with the Arc Thrower, Sarah has become a legend for single-handedly holding off waves of Bug attacks during the Battle of New Helsinki. Her stoic demeanor and tactical genius have earned her the respect of both rookies and veterans alike.
          </answer>
        </example>
    </examples>

    <output_format>Provide a cohesive narrative of 200-300 words that captures the essence of John Helldiver's legendary status while maintaining the gritty, militaristic tone of the Helldivers universe.</output_format>
</prompt>
```



### helldiver-weapons


```xml
<helldiver-weapons>
  <helldiver-weapon>Arc Thrower</helldiver-weapon>
  <helldiver-weapon>Plasma Rifle</helldiver-weapon>
  <helldiver-weapon>Grenade Launcher</helldiver-weapon>
  <helldiver-weapon>Liberator Assault Rifle</helldiver-weapon>
  <helldiver-weapon>Breaker Shotgun</helldiver-weapon>
  <helldiver-weapon>Railgun</helldiver-weapon>
  <helldiver-weapon>Flamethrower</helldiver-weapon>
  <helldiver-weapon>Sickle Autocannon</helldiver-weapon>
  <helldiver-weapon>Stalwart Machine Gun</helldiver-weapon>
  <helldiver-weapon>P-7 "Punisher" Sidearm</helldiver-weapon>
  <helldiver-stratagem>Orbital Strike</helldiver-stratagem>
  <helldiver-stratagem>Supply Drop</helldiver-stratagem>
  <helldiver-stratagem>Reinforce</helldiver-stratagem>
  <helldiver-stratagem>Hellbomb</helldiver-stratagem>
  <helldiver-stratagem>Orbital Laser</helldiver-stratagem>
  <helldiver-stratagem>Strafing Run</helldiver-stratagem>
  <helldiver-stratagem>Airstrike</helldiver-stratagem>
  <helldiver-stratagem>Defensive Barrier</helldiver-stratagem>
  <helldiver-stratagem>Sentry Gun</helldiver-stratagem>
  <helldiver-stratagem>Jump Pack</helldiver-stratagem>
</helldiver-weapons>
```

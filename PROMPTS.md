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


------------------------------

i'm trying to fix these tests/pylint/* that are using custom pylint plugins defined in pylint/plugins/* they get loaded in by tests/pylint/conftest.py.

Here's an example of this setup via home-assistant/core:

https://github.com/home-assistant/core/blob/dev/tests/pylint/conftest.py
https://github.com/home-assistant/core/blob/dev/pylint/plugins/hass_decorator.py
https://github.com/home-assistant/core/blob/dev/tests/pylint/test_decorator.py

look at these examples and use it as inspiration to fix tests/pylint/test_marimo_cell_params_validator.py

How can I create a pylint plugin to catch any errors specified in the marimo_standards section?
I want to mimick what https://github.com/home-assistant/core/tree/dev/pylint/plugins does. they have a local folder for their rules, the folder structure is as follows:

# this folder contains the tests and the conftest file that tells pytest  how to load the plugins from files.

~/dev/core/tests/pylint dev
❯ tree
.
├── __init__.py
├── conftest.py
├── test_decorator.py
├── test_enforce_class_module.py
├── test_enforce_sorted_platforms.py
├── test_enforce_super_call.py
├── test_enforce_type_hints.py
└── test_imports.py

1 directory, 8 files

here's the conftest file:

"""Configuration for pylint tests."""

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import sys
from types import ModuleType

from pylint.checkers import BaseChecker
from pylint.testutils.unittest_linter import UnittestLinter
import pytest

BASE_PATH = Path(__file__).parents[2]


def _load_plugin_from_file(module_name: str, file: str) -> ModuleType:
    """Load plugin from file path."""
    spec = spec_from_file_location(
        module_name,
        str(BASE_PATH.joinpath(file)),
    )
    assert spec and spec.loader

    module = module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture(name="hass_enforce_type_hints", scope="package")
def hass_enforce_type_hints_fixture() -> ModuleType:
    """Fixture to provide a requests mocker."""
    return _load_plugin_from_file(
        "hass_enforce_type_hints",
        "pylint/plugins/hass_enforce_type_hints.py",
    )


@pytest.fixture(name="linter")
def linter_fixture() -> UnittestLinter:
    """Fixture to provide a requests mocker."""
    return UnittestLinter()


@pytest.fixture(name="type_hint_checker")
def type_hint_checker_fixture(hass_enforce_type_hints, linter) -> BaseChecker:
    """Fixture to provide a requests mocker."""
    type_hint_checker = hass_enforce_type_hints.HassTypeHintChecker(linter)
    type_hint_checker.module = "homeassistant.components.pylint_test"
    return type_hint_checker


@pytest.fixture(name="hass_imports", scope="package")
def hass_imports_fixture() -> ModuleType:
    """Fixture to provide a requests mocker."""
    return _load_plugin_from_file(
        "hass_imports",
        "pylint/plugins/hass_imports.py",
    )


@pytest.fixture(name="imports_checker")
def imports_checker_fixture(hass_imports, linter) -> BaseChecker:
    """Fixture to provide a requests mocker."""
    type_hint_checker = hass_imports.HassImportsFormatChecker(linter)
    type_hint_checker.module = "homeassistant.components.pylint_test"
    return type_hint_checker


@pytest.fixture(name="hass_enforce_super_call", scope="package")
def hass_enforce_super_call_fixture() -> ModuleType:
    """Fixture to provide a requests mocker."""
    return _load_plugin_from_file(
        "hass_enforce_super_call",
        "pylint/plugins/hass_enforce_super_call.py",
    )


@pytest.fixture(name="super_call_checker")
def super_call_checker_fixture(hass_enforce_super_call, linter) -> BaseChecker:
    """Fixture to provide a requests mocker."""
    super_call_checker = hass_enforce_super_call.HassEnforceSuperCallChecker(linter)
    super_call_checker.module = "homeassistant.components.pylint_test"
    return super_call_checker


@pytest.fixture(name="hass_enforce_sorted_platforms", scope="package")
def hass_enforce_sorted_platforms_fixture() -> ModuleType:
    """Fixture to the content for the hass_enforce_sorted_platforms check."""
    return _load_plugin_from_file(
        "hass_enforce_sorted_platforms",
        "pylint/plugins/hass_enforce_sorted_platforms.py",
    )


@pytest.fixture(name="enforce_sorted_platforms_checker")
def enforce_sorted_platforms_checker_fixture(
    hass_enforce_sorted_platforms, linter
) -> BaseChecker:
    """Fixture to provide a hass_enforce_sorted_platforms checker."""
    enforce_sorted_platforms_checker = (
        hass_enforce_sorted_platforms.HassEnforceSortedPlatformsChecker(linter)
    )
    enforce_sorted_platforms_checker.module = "homeassistant.components.pylint_test"
    return enforce_sorted_platforms_checker


@pytest.fixture(name="hass_enforce_class_module", scope="package")
def hass_enforce_class_module_fixture() -> ModuleType:
    """Fixture to the content for the hass_enforce_class_module check."""
    return _load_plugin_from_file(
        "hass_enforce_class_module",
        "pylint/plugins/hass_enforce_class_module.py",
    )


@pytest.fixture(name="enforce_class_module_checker")
def enforce_class_module_fixture(hass_enforce_class_module, linter) -> BaseChecker:
    """Fixture to provide a hass_enforce_class_module checker."""
    enforce_class_module_checker = hass_enforce_class_module.HassEnforceClassModule(
        linter
    )
    enforce_class_module_checker.module = "homeassistant.components.pylint_test"
    return enforce_class_module_checker


@pytest.fixture(name="hass_decorator", scope="package")
def hass_decorator_fixture() -> ModuleType:
    """Fixture to provide a pylint plugin."""
    return _load_plugin_from_file(
        "hass_imports",
        "pylint/plugins/hass_decorator.py",
    )


@pytest.fixture(name="decorator_checker")
def decorator_checker_fixture(hass_decorator, linter) -> BaseChecker:
    """Fixture to provide a pylint checker."""
    type_hint_checker = hass_decorator.HassDecoratorChecker(linter)
    type_hint_checker.module = "homeassistant.components.pylint_test"
    return type_hint_checker


this is the contents of test_decorator.py:

"""Tests for pylint hass_enforce_type_hints plugin."""

from __future__ import annotations

import astroid
from pylint.checkers import BaseChecker
from pylint.interfaces import UNDEFINED
from pylint.testutils import MessageTest
from pylint.testutils.unittest_linter import UnittestLinter
from pylint.utils.ast_walker import ASTWalker
import pytest

from . import assert_adds_messages, assert_no_messages


def test_good_callback(linter: UnittestLinter, decorator_checker: BaseChecker) -> None:
    """Test good `@callback` decorator."""
    code = """
    from homeassistant.core import callback

    @callback
    def setup(
        arg1, arg2
    ):
        pass
    """

    root_node: astroid.Module = astroid.parse(code)
    walker = ASTWalker(linter)
    walker.add_checker(decorator_checker)

    with assert_no_messages(linter):
        walker.walk(root_node)


def test_bad_callback(linter: UnittestLinter, decorator_checker: BaseChecker) -> None:
    """Test bad `@callback` decorator."""
    code = """
    from homeassistant.core import callback

    @callback
    async def setup(
        arg1, arg2
    ):
        pass
    """

    root_node: astroid.Module = astroid.parse(code)
    walker = ASTWalker(linter)
    walker.add_checker(decorator_checker)

    with assert_adds_messages(
        linter,
        MessageTest(
            msg_id="hass-async-callback-decorator",
            line=5,
            node=root_node.body[1],
            args=None,
            confidence=UNDEFINED,
            col_offset=0,
            end_line=5,
            end_col_offset=15,
        ),
    ):
        walker.walk(root_node)


@pytest.mark.parametrize(
    ("keywords", "path"),
    [
        ('scope="function"', "tests.test_bootstrap"),
        ('scope="class"', "tests.test_bootstrap"),
        ('scope="module"', "tests.test_bootstrap"),
        ('scope="package"', "tests.test_bootstrap"),
        ('scope="session", autouse=True', "tests.test_bootstrap"),
        ('scope="function"', "tests.components.conftest"),
        ('scope="class"', "tests.components.conftest"),
        ('scope="module"', "tests.components.conftest"),
        ('scope="package"', "tests.components.conftest"),
        ('scope="session", autouse=True', "tests.components.conftest"),
        (
            'scope="session", autouse=find_spec("zeroconf") is not None',
            "tests.components.conftest",
        ),
        ('scope="function"', "tests.components.pylint_tests.conftest"),
        ('scope="class"', "tests.components.pylint_tests.conftest"),
        ('scope="module"', "tests.components.pylint_tests.conftest"),
        ('scope="package"', "tests.components.pylint_tests.conftest"),
        ('scope="function"', "tests.components.pylint_test"),
        ('scope="class"', "tests.components.pylint_test"),
        ('scope="module"', "tests.components.pylint_test"),
    ],
)
def test_good_fixture(
    linter: UnittestLinter, decorator_checker: BaseChecker, keywords: str, path: str
) -> None:
    """Test good `@pytest.fixture` decorator."""
    code = f"""
    import pytest

    @pytest.fixture
    def setup(
        arg1, arg2
    ):
        pass

    @pytest.fixture({keywords})
    def setup_session(
        arg1, arg2
    ):
        pass
    """

    root_node: astroid.Module = astroid.parse(code, path)
    walker = ASTWalker(linter)
    walker.add_checker(decorator_checker)

    with assert_no_messages(linter):
        walker.walk(root_node)


@pytest.mark.parametrize(
    "path",
    [
        "tests.components.pylint_test",
        "tests.components.pylint_test.conftest",
        "tests.components.pylint_test.module",
    ],
)
def test_bad_fixture_session_scope(
    linter: UnittestLinter, decorator_checker: BaseChecker, path: str
) -> None:
    """Test bad `@pytest.fixture` decorator."""
    code = """
    import pytest

    @pytest.fixture
    def setup(
        arg1, arg2
    ):
        pass

    @pytest.fixture(scope="session")
    def setup_session(
        arg1, arg2
    ):
        pass
    """

    root_node: astroid.Module = astroid.parse(code, path)
    walker = ASTWalker(linter)
    walker.add_checker(decorator_checker)

    with assert_adds_messages(
        linter,
        MessageTest(
            msg_id="hass-pytest-fixture-decorator",
            line=10,
            node=root_node.body[2].decorators.nodes[0],
            args=("scope `session`", "use `package` or lower"),
            confidence=UNDEFINED,
            col_offset=1,
            end_line=10,
            end_col_offset=32,
        ),
    ):
        walker.walk(root_node)


@pytest.mark.parametrize(
    "path",
    [
        "tests.components.pylint_test",
        "tests.components.pylint_test.module",
    ],
)
def test_bad_fixture_package_scope(
    linter: UnittestLinter, decorator_checker: BaseChecker, path: str
) -> None:
    """Test bad `@pytest.fixture` decorator."""
    code = """
    import pytest

    @pytest.fixture
    def setup(
        arg1, arg2
    ):
        pass

    @pytest.fixture(scope="package")
    def setup_session(
        arg1, arg2
    ):
        pass
    """

    root_node: astroid.Module = astroid.parse(code, path)
    walker = ASTWalker(linter)
    walker.add_checker(decorator_checker)

    with assert_adds_messages(
        linter,
        MessageTest(
            msg_id="hass-pytest-fixture-decorator",
            line=10,
            node=root_node.body[2].decorators.nodes[0],
            args=("scope `package`", "use `module` or lower"),
            confidence=UNDEFINED,
            col_offset=1,
            end_line=10,
            end_col_offset=32,
        ),
    ):
        walker.walk(root_node)


@pytest.mark.parametrize(
    "keywords",
    [
        'scope="session"',
        'scope="session", autouse=False',
    ],
)
@pytest.mark.parametrize(
    "path",
    [
        "tests.test_bootstrap",
        "tests.components.conftest",
    ],
)
def test_bad_fixture_autouse(
    linter: UnittestLinter, decorator_checker: BaseChecker, keywords: str, path: str
) -> None:
    """Test bad `@pytest.fixture` decorator."""
    code = f"""
    import pytest

    @pytest.fixture
    def setup(
        arg1, arg2
    ):
        pass

    @pytest.fixture({keywords})
    def setup_session(
        arg1, arg2
    ):
        pass
    """

    root_node: astroid.Module = astroid.parse(code, path)
    walker = ASTWalker(linter)
    walker.add_checker(decorator_checker)

    with assert_adds_messages(
        linter,
        MessageTest(
            msg_id="hass-pytest-fixture-decorator",
            line=10,
            node=root_node.body[2].decorators.nodes[0],
            args=("scope/autouse combination", "set `autouse=True` or reduce scope"),
            confidence=UNDEFINED,
            col_offset=1,
            end_line=10,
            end_col_offset=17 + len(keywords),
        ),
    ):
        walker.walk(root_node)


and in this folder they define their rules.

this is ruff.toml:

# This extend our general Ruff rules specifically for tests
extend = "../pyproject.toml"

[lint]
extend-ignore = [
    "INP001", # File is part of an implicit namespace package. Add an `__init__.py`.
]

[lint.isort]
known-third-party = [
    "pylint",
]

this is hass_decorator.py:

"""Plugin to check decorators."""

from __future__ import annotations

from astroid import nodes
from pylint.checkers import BaseChecker
from pylint.lint import PyLinter


class HassDecoratorChecker(BaseChecker):
    """Checker for decorators."""

    name = "hass_decorator"
    priority = -1
    msgs = {
        "W7471": (
            "A coroutine function should not be decorated with @callback",
            "hass-async-callback-decorator",
            "Used when a coroutine function has an invalid @callback decorator",
        ),
        "W7472": (
            "Fixture %s is invalid here, please %s",
            "hass-pytest-fixture-decorator",
            "Used when a pytest fixture is invalid",
        ),
    }

    def _get_pytest_fixture_node(self, node: nodes.FunctionDef) -> nodes.Call | None:
        for decorator in node.decorators.nodes:
            if (
                isinstance(decorator, nodes.Call)
                and decorator.func.as_string() == "pytest.fixture"
            ):
                return decorator

        return None

    def _get_pytest_fixture_node_keyword(
        self, decorator: nodes.Call, search_arg: str
    ) -> nodes.Keyword | None:
        for keyword in decorator.keywords:
            if keyword.arg == search_arg:
                return keyword

        return None

    def _check_pytest_fixture(
        self, node: nodes.FunctionDef, decoratornames: set[str]
    ) -> None:
        if (
            "_pytest.fixtures.FixtureFunctionMarker" not in decoratornames
            or not (root_name := node.root().name).startswith("tests.")
            or (decorator := self._get_pytest_fixture_node(node)) is None
            or not (
                scope_keyword := self._get_pytest_fixture_node_keyword(
                    decorator, "scope"
                )
            )
            or not isinstance(scope_keyword.value, nodes.Const)
            or not (scope := scope_keyword.value.value)
        ):
            return

        parts = root_name.split(".")
        test_component: str | None = None
        if root_name.startswith("tests.components.") and parts[2] != "conftest":
            test_component = parts[2]

        if scope == "session":
            if test_component:
                self.add_message(
                    "hass-pytest-fixture-decorator",
                    node=decorator,
                    args=("scope `session`", "use `package` or lower"),
                )
                return
            if not (
                autouse_keyword := self._get_pytest_fixture_node_keyword(
                    decorator, "autouse"
                )
            ) or (
                isinstance(autouse_keyword.value, nodes.Const)
                and not autouse_keyword.value.value
            ):
                self.add_message(
                    "hass-pytest-fixture-decorator",
                    node=decorator,
                    args=(
                        "scope/autouse combination",
                        "set `autouse=True` or reduce scope",
                    ),
                )
            return

        test_module = parts[3] if len(parts) > 3 else ""

        if test_component and scope == "package" and test_module != "conftest":
            self.add_message(
                "hass-pytest-fixture-decorator",
                node=decorator,
                args=("scope `package`", "use `module` or lower"),
            )

    def visit_asyncfunctiondef(self, node: nodes.AsyncFunctionDef) -> None:
        """Apply checks on an AsyncFunctionDef node."""
        if decoratornames := node.decoratornames():
            if "homeassistant.core.callback" in decoratornames:
                self.add_message("hass-async-callback-decorator", node=node)
            self._check_pytest_fixture(node, decoratornames)

    def visit_functiondef(self, node: nodes.FunctionDef) -> None:
        """Apply checks on an AsyncFunctionDef node."""
        if decoratornames := node.decoratornames():
            self._check_pytest_fixture(node, decoratornames)


def register(linter: PyLinter) -> None:
    """Register the checker."""
    linter.register_checker(HassDecoratorChecker(linter))


~/dev/core/pylint dev
❯ tree
.
├── plugins
│   ├── hass_decorator.py
│   ├── hass_enforce_class_module.py
│   ├── hass_enforce_sorted_platforms.py
│   ├── hass_enforce_super_call.py
│   ├── hass_enforce_type_hints.py
│   ├── hass_imports.py
│   ├── hass_inheritance.py
│   └── hass_logger.py
└── ruff.toml

2 directories, 9 files

When you are read I will run tests so you can see the errors.

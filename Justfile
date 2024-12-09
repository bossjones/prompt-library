set shell := ["zsh", "-cu"]

# just manual: https://github.com/casey/just/#readme

# Ignore the .env file that is only used by the web service
set dotenv-load := false

CURRENT_DIR := "$(pwd)"

base64_cmd := if "{{os()}}" == "macos" { "base64 -w 0 -i cert.pem -o ca.pem" } else { "base64 -w 0 -i cert.pem > ca.pem" }
grep_cmd := if "{{os()}}" =~ "macos" { "ggrep" } else { "grep" }

# Variables
PYTHON := "uv run python"
UV_RUN := "uv run"

# Recipes
# Install the virtual environment and install the pre-commit hooks
install:
	@echo "🚀 Creating virtual environment using uv"
	uv sync
	uv tool upgrade pyright
	uv run pre-commit install

# Run code quality tools.
check:
	@echo "🚀 Checking lock file consistency with 'pyproject.toml'"
	uv lock --locked
	@echo "🚀 Linting code: Running pre-commit"
	uv run pre-commit run -a
	@echo "🚀 Static type checking: Running mypy"
	uv run mypy
	@echo "🚀 Checking for obsolete dependencies: Running deptry"
	uv run deptry .

# Test the code with pytest
test:
	@echo "🚀 Testing code: Running pytest"
	{{PYTHON}} -m pytest --cov --cov-config=pyproject.toml --cov-report=xml

# Build wheel file
build: clean-build
	@echo "🚀 Creating wheel file"
	uvx --from build pyproject-build --installer uv

# Clean build artifacts
clean-build:
	@echo "🚀 Removing build artifacts"
	{{PYTHON}} -c "import shutil; import os; shutil.rmtree('dist') if os.path.exists('dist') else None"

# Publish a release to PyPI.
publish:
	@echo "🚀 Publishing."
	uvx twine upload --repository-url https://upload.pypi.org/legacy/ dist/*

# Build and publish.
build-and-publish: build publish

# Test if documentation can be built without warnings or errors
docs-test:
	uv run mkdocs build -s

# Build and serve the documentation
docs:
	uv run mkdocs serve

help:
	@just --list

default: help


# Print the current operating system
info:
		print "OS: {{os()}}"

# Display system information
system-info:
	@echo "CPU architecture: {{ arch() }}"
	@echo "Operating system type: {{ os_family() }}"
	@echo "Operating system: {{ os() }}"

# verify python is running under pyenv
which-python:
		python -c "import sys;print(sys.executable)"

# when developing, you can use this to watch for changes and restart the server
autoreload-code:
	uv run watchmedo auto-restart --pattern "*.py" --recursive --signal SIGTERM uv run goobctl go

# Open the HTML coverage report in the default
local-open-coverage:
	./scripts/open-browser.py file://${PWD}/htmlcov/index.html

# Open the HTML coverage report in the default
open-coverage: local-open-coverage

# Run unit tests and open the coverage report
local-unittest:
	bash scripts/unittest-local
	./scripts/open-browser.py file://${PWD}/htmlcov/index.html

# Run all pre-commit hooks on all files
pre-commit-run-all:
	uv run pre-commit run --all-files

# Install pre-commit hooks
pre-commit-install:
	uv run pre-commit install

# Display the dependency tree of the project
pipdep-tree:
	pipdeptree --python .venv/bin/python3

# install uv tools globally
uv-tool-install:
	uv install invoke
	uv install pipdeptree
	uv install click

# Lint GitHub Actions workflow files
lint-github-actions:
	actionlint

# check that taplo is installed to lint/format TOML
check-taplo-installed:
	@command -v taplo >/dev/null 2>&1 || { echo >&2 "taplo is required but it's not installed. run 'brew install taplo'"; exit 1; }

# Format Python files using pre-commit
fmt-python:
	git ls-files '*.py' '*.ipynb' | xargs uv run pre-commit run --files

# Format Markdown files using pre-commit
fmt-markdown-pre-commit:
	git ls-files '*.md' | xargs uv run pre-commit run --files

# format pyproject.toml using taplo
fmt-toml:
	uv run pre-commit run taplo-format --all-files

# SOURCE: https://github.com/PovertyAction/ipa-data-tech-handbook/blob/ed81492f3917ee8c87f5d8a60a92599a324f2ded/Justfile

# Format all markdown and config files
fmt-markdown:
	git ls-files '*.md' | xargs uv run mdformat

# Format a single markdown file, "f"
fmt-md f:
	uv run mdformat {{ f }}

# format all code using pre-commit config
fmt: fmt-python fmt-toml fmt-markdown fmt-markdown fmt-markdown-pre-commit

# lint python files using ruff
lint-python:
	pre-commit run ruff --all-files

# lint TOML files using taplo
lint-toml: check-taplo-installed
	pre-commit run taplo-lint --all-files

# lint yaml files using yamlfix
lint-yaml:
	pre-commit run yamlfix --all-files

# lint pyproject.toml and detect log_cli = true
lint-check-log-cli:
	pre-commit run detect-pytest-live-log --all-files

# Check format of all markdown files
lint-check-markdown:
	uv run mdformat --check .

# Lint all files in the current directory (and any subdirectories).
lint: lint-python lint-toml lint-check-log-cli lint-check-markdown

# generate type stubs for the project
createstubs:
	./scripts/createstubs.sh

# sweep init
sweep-init:
	uv run sweep init

# TODO: We should try out trunk
# By default, we use the following config that runs Trunk, an opinionated super-linter that installs all the common formatters and linters for your codebase. You can set up and configure Trunk for yourself by following https://docs.trunk.io/get-started.
# sandbox:
#   install:
#     - trunk init
#   check:
#     - trunk fmt {file_path}
#     - trunk check {file_path}

# Download AI models from Dropbox
download-models:
	curl -L 'https://www.dropbox.com/s/im6ytahqgbpyjvw/ScreenNetV1.pth?dl=1' > data/ScreenNetV1.pth

# Perform a dry run of dependency upgrades
upgrade-dry-run:
	uv lock --update-all --all-features

# Upgrade all dependencies and sync the environment
sync-upgrade-all:
	uv sync --update-all --all-features

# Start a background HTTP server for test fixtures
http-server-background:
	#!/bin/bash
	# _PID=$(pgrep -f " -m http.server --bind localhost 19000 -d ./tests/fixtures")
	pkill -f " -m http.server --bind localhost 19000 -d ./tests/fixtures"
	python3 -m http.server --bind localhost 19000 -d ./tests/fixtures &
	echo $! > PATH.PID

# Start an HTTP server for test fixtures
http-server:
	#!/bin/bash
	# _PID=$(pgrep -f " -m http.server --bind localhost 19000 -d ./tests/fixtures")
	pkill -f " -m http.server --bind localhost 19000 -d ./tests/fixtures"
	python3 -m http.server --bind localhost 19000 -d ./tests/fixtures
	echo $! > PATH.PID

# Bump the version by major
major-version-bump:
	uv version
	uv version --bump major

# Bump the version by minor
minor-version-bump:
	uv version
	uv version --bump minor

# Bump the version by patch
patch-version-bump:
	uv version
	uv version --bump patch

# Bump the version by major
version-bump-major: major-version-bump

# Bump the version by minor
version-bump-minor: minor-version-bump

# Bump the version by patch
version-bump-patch: patch-version-bump

# Serve the documentation locally for preview
docs_preview:
	uv run mkdocs serve

# Build the documentation
docs_build:
	uv run mkdocs build

# Deploy the documentation to GitHub Pages
docs_deploy:
	uv run mkdocs gh-deploy --clean

# Generate a draft changelog
changelog:
	uv run towncrier build --version main --draft

# Checkout main branch and pull latest changes
gco:
	gco main
	git pull --rebase

# Show diff for LangChain migration
langchain-migrate-diff:
	langchain-cli migrate --include-ipynb --diff democracy_exe

# Perform LangChain migration
langchain-migrate:
	langchain-cli migrate --include-ipynb democracy_exe

# Get the ruff config
get-ruff-config:
	uv run ruff check --show-settings --config pyproject.toml -v -o ruff_config.toml >> ruff.log 2>&1

# Run lint and test
ci:
	uv run lint
	uv run test

# Open a manhole shell
manhole-shell:
	./scripts/manhole-shell

# Find the cassettes directories
find-cassettes-dirs:
	fd -td cassettes

# Delete the cassettes directories
delete-cassettes:
	fd -td cassettes -X rm -ri

# Install brew dependencies
brew-deps:
	brew install libmagic poppler tesseract pandoc qpdf tesseract-lang
	brew install --cask libreoffice

# install aicommits and configure it
init-aicommits:
	npm install -g aicommits
	aicommits config set OPENAI_KEY=$OCO_OPENAI_API_KEY type=conventional model=gpt-4o max-length=100
	aicommits hook install

# Run aider
aider:
	uv run aider -c .aider.conf.yml --aiderignore .aiderignore

aider-o1-preview:
	uv run aider -c .aider.conf.yml --aiderignore .aiderignore --o1-preview --architect --edit-format whole --model o1-mini --no-stream

aider-sonnet:
	uv run aider -c .aider.conf.yml --aiderignore .aiderignore --sonnet --architect --map-tokens 2048 --cache-prompts --edit-format diff

# Run aider with Claude
aider-claude:
	uv run aider -c .aider.conf.yml --aiderignore .aiderignore --model 'anthropic/claude-3-5-sonnet-20241022'


# SOURCE: https://github.com/RobertCraigie/prisma-client-py/blob/da53c4280756f1a9bddc3407aa3b5f296aa8cc10/Makefile#L77
# Remove all generated files and caches
clean:
	#!/bin/bash
	rm -rf .cache
	rm -rf `find . -name __pycache__`
	rm -rf .tests_cache
	rm -rf .mypy_cache
	rm -rf htmlcov
	rm -rf *.egg-info
	rm -f .coverage
	rm -f .coverage.*
	rm -rf build
	rm -rf dist
	rm -f coverage.xml

# Create a token for authentication
uv_create_token:
	{{PYTHON}} -c "from democracy_exe.cli import create_token; create_token()"

# Show current database state
uv_db_current:
	{{PYTHON}} -c "from democracy_exe.cli import db_current; db_current()"

# Upgrade database to latest version
uv_db_upgrade:
	{{PYTHON}} -c "from democracy_exe.cli import db_upgrade; db_upgrade()"

# Downgrade database to previous version
uv_db_downgrade:
	{{PYTHON}} -c "from democracy_exe.cli import db_downgrade; db_downgrade()"

# Export a collection of data
uv_export_collection:
	{{PYTHON}} -c "from democracy_exe.cli import export_collection; export_collection()"

# Import a collection of data
uv_import_collection:
	{{PYTHON}} -c "from democracy_exe.cli import import_collection; import_collection()"

# Import a single file
uv_import_file:
	{{PYTHON}} -c "from democracy_exe.cli import import_file; import_file()"

# Lint markdown files
uv_lint_markdown:
	{{UV_RUN}} pymarkdownlnt --disable-rules=MD013,MD034 scan README.md

# Serve documentation locally
uv_serve_docs:
	{{UV_RUN}} mkdocs serve

# Convert pylint configuration to ruff
uv_pylint_to_ruff:
	{{UV_RUN}} pylint-to-ruff

# Start a simple HTTP server
uv_http:
	{{UV_RUN}} -m http.server 8008

# Display current user
uv_whoami:
	whoami

# Install missing mypy type stubs
uv_mypy_missing:
	{{UV_RUN}} mypy --install-types

# Run pre-commit hooks on all files
uv_fmt:
	{{UV_RUN}} pre-commit run --all-files

# Run pylint checks
uv_pylint:
	{{PYTHON}} -m invoke ci.pylint --everything

# Run pylint with error-only configuration
uv_pylint_error_only:
	{{UV_RUN}} pylint --output-format=colorized --disable=all --max-line-length=120 --enable=F,E --rcfile pyproject.toml democracy_exe tests

# Run pylint on all files
uv_lint_all:
	{{PYTHON}} -m pylint -j4 --output-format=colorized --rcfile pyproject.toml tests democracy_exe

# Run ruff linter
uv_lint:
	{{PYTHON}} -m ruff check --fix . --config=pyproject.toml

# Run all typecheck tasks
uv_typecheck:
	just uv_typecheck_pyright
	just uv_typecheck_mypy

# Run Pyright type checker
uv_typecheck_pyright:
	{{UV_RUN}} pyright -p pyproject.toml .

# Verify types using Pyright, ignoring external packages
uv_typecheck_verify_types:
	{{UV_RUN}} pyright --verifytypes democracy_exe --ignoreexternal --verbose

# Run MyPy type checker and open coverage report
uv_typecheck_mypy:
	just uv_ci_mypy
	just uv_open_mypy_coverage

# Generate changelog draft
uv_docs_changelog:
	{{UV_RUN}} towncrier build --version main --draft

# Run MyPy with various report formats
uv_ci_mypy:
	{{UV_RUN}} mypy --config-file=pyproject.toml --html-report typingcov --cobertura-xml-report typingcov_cobertura --xml-report typingcov_xml --txt-report typingcov_txt .

# Open MyPy coverage report
uv_open_mypy_coverage:
	open typingcov/index.html

# Open Zipkin UI
uv_open_zipkin:
	open http://127.0.0.1:9411

# Open OpenTelemetry endpoint
uv_open_otel:
	open http://127.0.0.1:4317

# Open test coverage report
uv_open_coverage:
	just local-open-coverage

# Open pgAdmin
uv_open_pgadmin:
	open http://127.0.0.1:4000

# Open Prometheus UI
uv_open_prometheus:
	open http://127.0.0.1:9999

# Open Grafana UI
uv_open_grafana:
	open http://127.0.0.1:3333

# Open Chroma UI
uv_open_chroma:
	open http://127.0.0.1:9010

# Open ChromaDB Admin UI
uv_open_chromadb_admin:
	open http://127.0.0.1:4001

# Open all UIs and reports
uv_open_all:
	just uv_open_mypy_coverage
	just uv_open_chroma
	just uv_open_zipkin
	just uv_open_otel
	just uv_open_pgadmin
	just uv_open_prometheus
	just uv_open_grafana
	just uv_open_chromadb_admin
	just uv_open_coverage


# Run simple unit tests with coverage
uv_unittests_simple:
	{{UV_RUN}} pytest --diff-width=60 --diff-symbols --cov-append --cov-report=term-missing --junitxml=junit/test-results.xml --cov-report=xml:cov.xml --cov-report=html:htmlcov --cov-report=annotate:cov_annotate --cov=.

# Run unit tests in debug mode with extended output
uv_unittests_debug:
	{{UV_RUN}} pytest -s -vv --diff-width=60 --diff-symbols --pdb --pdbcls bpdb:BPdb --showlocals --tb=short --cov-append --cov-report=term-missing --junitxml=junit/test-results.xml --cov-report=xml:cov.xml --cov-report=html:htmlcov --cov-report=annotate:cov_annotate --cov=.

# Run service-related unit tests in debug mode
uv_unittests_debug_services:
	{{UV_RUN}} pytest -m services -s -vv --diff-width=60 --diff-symbols --pdb --pdbcls bpdb:BPdb --showlocals --tb=short --cov-append --cov-report=term-missing --junitxml=junit/test-results.xml --cov-report=xml:cov.xml --cov-report=html:htmlcov --cov-report=annotate:cov_annotate --cov=.

# Run asynciotyper-related unit tests in debug mode
uv_unittests_debug_asynciotyper:
	{{UV_RUN}} pytest -s -vv --diff-width=60 --diff-symbols --showlocals --tb=short --cov-append --cov-report=term-missing --junitxml=junit/test-results.xml --cov-report=xml:cov.xml --cov-report=html:htmlcov --cov-report=annotate:cov_annotate --cov=. -m asynciotyper

# Run pgvector-related unit tests in debug mode
uv_unittests_debug_pgvector:
	{{UV_RUN}} pytest -m pgvectoronly -s -vv --diff-width=60 --diff-symbols --pdb --pdbcls bpdb:BPdb --showlocals --tb=short --cov-append --cov-report=term-missing --junitxml=junit/test-results.xml --cov-report=xml:cov.xml --cov-report=html:htmlcov --cov-report=annotate:cov_annotate --cov=.

# Profile unit tests in debug mode using pyinstrument
uv_profile_unittests_debug:
	{{UV_RUN}} pyinstrument -m pytest -s -vv --diff-width=60 --diff-symbols --pdb --pdbcls bpdb:BPdb --showlocals --tb=short --cov-append --cov-report=term-missing --junitxml=junit/test-results.xml --cov-report=xml:cov.xml --cov-report=html:htmlcov --cov-report=annotate:cov_annotate --cov=.

# Profile unit tests in debug mode using py-spy
uv_spy_unittests_debug:
	{{UV_RUN}} py-spy top -- python -m pytest -s -vv --diff-width=60 --diff-symbols --pdb --pdbcls bpdb:BPdb --showlocals --tb=short --cov-append --cov-report=term-missing --junitxml=junit/test-results.xml --cov-report=xml:cov.xml --cov-report=html:htmlcov --cov-report=annotate:cov_annotate --cov=.

# Run standard unit tests with coverage
uv_unittests:
	{{UV_RUN}} pytest --verbose --showlocals --tb=short --cov-append --cov-report=term-missing --junitxml=junit/test-results.xml --cov-report=xml:cov.xml --cov-report=html:htmlcov --cov-report=annotate:cov_annotate --cov=.

# Run unit tests with VCR in record mode
uv_unittests_vcr_record:
	{{UV_RUN}} pytest --record-mode=all --verbose --showlocals --tb=short --cov-append --cov-report=term-missing --junitxml=junit/test-results.xml --cov-report=xml:cov.xml --cov-report=html:htmlcov --cov-report=annotate:cov_annotate --cov=.

# Run unit tests with VCR in rewrite mode
uv_unittests_vcr_record_rewrite:
	{{UV_RUN}} pytest --record-mode=rewrite --verbose --showlocals --tb=short --cov-append --cov-report=term-missing --junitxml=junit/test-results.xml --cov-report=xml:cov.xml --cov-report=html:htmlcov --cov-report=annotate:cov_annotate --cov=.

# Run unit tests with VCR in once mode
uv_unittests_vcr_record_once:
	{{UV_RUN}} pytest --record-mode=once --verbose --showlocals --tb=short --cov-append --cov-report=term-missing --junitxml=junit/test-results.xml --cov-report=xml:cov.xml --cov-report=html:htmlcov --cov-report=annotate:cov_annotate --cov=.

# Run all VCR recording tests
uv_unittests_vcr_record_all: uv_unittests_vcr_record

# Run final VCR recording tests (NOTE: this is the only one that works)
uv_unittests_vcr_record_final: uv_unittests_vcr_record

# Run simple tests without warnings
uv_test_simple:
	{{UV_RUN}} pytest -p no:warnings

# Alias for simple tests without warnings
uv_simple_test:
	{{UV_RUN}} pytest -p no:warnings

# Run unit tests in debug mode with extended output
uv_new_unittests_debug:
	{{UV_RUN}} pytest -s --verbose --pdb --pdbcls bpdb:BPdb --showlocals --tb=short

# Run linting and unit tests
uv_test:
	just uv_lint
	just uv_unittests

# Combine coverage data
uv_coverage_combine:
	{{UV_RUN}} python -m coverage combine

# Generate HTML coverage report
uv_coverage_html:
	{{UV_RUN}} python -m coverage html --skip-covered --skip-empty

# Run pytest with coverage
uv_coverage_pytest:
	{{UV_RUN}} coverage run --rcfile=pyproject.toml -m pytest tests

# Run pytest with coverage in debug mode
uv_coverage_pytest_debug:
	{{UV_RUN}} coverage run --rcfile=pyproject.toml -m pytest --verbose -vvv --pdb --pdbcls bpdb:BPdb --showlocals --tb=short --capture=no tests

# Run pytest with coverage for evals in debug mode
uv_coverage_pytest_evals_debug:
	{{UV_RUN}} coverage run --rcfile=pyproject.toml -m pytest --verbose -vv --pdb --pdbcls bpdb:BPdb --showlocals --tb=short --capture=no -m evals --slow tests

# Run pytest with coverage and memray in debug mode
uv_memray_coverage_pytest_debug:
	{{UV_RUN}} coverage run --rcfile=pyproject.toml -m pytest --verbose -vvv --memray --pdb --pdbcls bpdb:BPdb --showlocals --tb=short --capture=no tests

# Run pytest with coverage and memray for evals in debug mode
uv_memray_coverage_pytest_evals_debug:
	{{UV_RUN}} coverage run --rcfile=pyproject.toml -m pytest --verbose --memray -vv --pdb --pdbcls bpdb:BPdb --showlocals --tb=short --capture=no -m evals --slow tests

# Generate and view coverage report
uv_coverage_report:
	just uv_coverage_pytest
	just uv_coverage_combine
	just uv_coverage_show
	just uv_coverage_html
	just uv_coverage_open

# Generate and view coverage report in debug mode
uv_coverage_report_debug:
	just uv_coverage_pytest_debug
	just uv_coverage_combine
	just uv_coverage_show
	just uv_coverage_html
	just uv_coverage_open

# Generate and view coverage report for evals in debug mode
uv_coverage_report_debug_evals:
	just uv_coverage_pytest_debug
	just uv_coverage_pytest_evals_debug
	just uv_coverage_combine
	just uv_coverage_show
	just uv_coverage_html
	just uv_coverage_open

# Run end-to-end tests with coverage in debug mode
uv_e2e_coverage_pytest_debug:
	{{UV_RUN}} coverage run --rcfile=pyproject.toml -m pytest --verbose --pdb --pdbcls bpdb:BPdb --showlocals --tb=short --capture=no tests -m e2e

# Generate and view end-to-end coverage report in debug mode
uv_e2e_coverage_report_debug:
	just uv_e2e_coverage_pytest_debug
	just uv_coverage_combine
	just uv_coverage_show
	just uv_coverage_html
	just uv_coverage_open

# Show coverage report
uv_coverage_show:
	{{UV_RUN}} python -m coverage report --fail-under=5

# Open coverage report
uv_coverage_open:
	just local-open-coverage

# Run linting and tests (CI)
uv_ci:
	just uv_lint
	just uv_test

# Run debug unit tests and open coverage report (CI debug)
uv_ci_debug:
	just uv_unittests_debug
	just uv_coverage_open

# Run simple unit tests and open coverage report (CI simple)
uv_ci_simple:
	just uv_unittests_simple
	just uv_coverage_open

# Run CI with evals
uv_ci_with_evals:
	just uv_coverage_pytest_debug
	just uv_coverage_pytest_evals_debug
	just uv_coverage_combine
	just uv_coverage_show
	just uv_coverage_html
	just uv_coverage_open

# Run CI with evals and memray
uv_ci_with_evals_memray:
	just uv_memray_coverage_pytest_debug
	just uv_memray_coverage_pytest_evals_debug
	just uv_coverage_combine
	just uv_coverage_show
	just uv_coverage_html
	just uv_coverage_open

# Deploy documentation to GitHub Pages
uv_gh_deploy:
	{{UV_RUN}} mkdocs gh-deploy --force --message '[skip ci] Docs updates'

# Create site directory
uv_mkdir_site:
	mkdir site

# Deploy documentation
uv_deploy_docs:
	just uv_mkdir_site
	just uv_gh_deploy

# Add bespoke adobe concepts to cursor context
add-cursor-context:
	mkdir -p democracy_exe/vendored || true
	gh repo clone universityofprofessorex/cerebro-bot democracy_exe/vendored/cerebro-bot || true && cd democracy_exe/vendored/cerebro-bot && git checkout feature-discord-utils && cd ../../..
	gh repo clone bossjones/sandbox_agent democracy_exe/vendored/sandbox_agent || true
	gh repo clone langchain-ai/retrieval-agent-template democracy_exe/vendored/retrieval-agent-template || true
	gh repo clone langchain-ai/rag-research-agent-template democracy_exe/vendored/rag-research-agent-template || true
	gh repo clone langchain-ai/memory-template democracy_exe/vendored/memory-template || true
	gh repo clone langchain-ai/react-agent democracy_exe/vendored/react-agent || true
	gh repo clone langchain-ai/chat-langchain democracy_exe/vendored/chat-langchain || true
	gh repo clone bossjones/goob_ai democracy_exe/vendored/goob_ai || true
	gh repo clone langchain-ai/langchain democracy_exe/vendored/langchain || true
	gh repo clone langchain-ai/langgraph democracy_exe/vendored/langgraph || true
	gh repo clone CraftSpider/dpytest democracy_exe/vendored/dpytest || true

	rm -rf democracy_exe/vendored/cerebro-bot/.git
	rm -rf democracy_exe/vendored/sandbox_agent/.git
	rm -rf democracy_exe/vendored/retrieval-agent-template/.git
	rm -rf democracy_exe/vendored/rag-research-agent-template/.git
	rm -rf democracy_exe/vendored/memory-template/.git
	rm -rf democracy_exe/vendored/react-agent/.git
	rm -rf democracy_exe/vendored/chat-langchain/.git
	rm -rf democracy_exe/vendored/goob_ai/.git
	rm -rf democracy_exe/vendored/langchain/.git
	rm -rf democracy_exe/vendored/langgraph/.git
	rm -rf democracy_exe/vendored/langchain-academy/.git
	rm -rf democracy_exe/vendored/dpytest/.git

# List outdated packages
outdated:
	{{UV_RUN}} pip list --outdated

install-llm-cli-plugins:
	uv add llm
	uv add llm-cmd llm-clip llm-sentence-transformers llm-replicate llm-perplexity llm-claude-3 llm-python llm-gemini llm-jq
# {{UV_RUN}} llm install llm-cmd
# {{UV_RUN}} llm install llm-clip
# {{UV_RUN}} llm install llm-sentence-transformers
# {{UV_RUN}} llm install llm-replicate
# {{UV_RUN}} llm install llm-perplexity
# {{UV_RUN}} llm install llm-claude-3
# {{UV_RUN}} llm install llm-python
# {{UV_RUN}} llm install llm-json
# {{UV_RUN}} llm install llm-markdown
# {{UV_RUN}} llm install llm-sql

smoke-test:
	cd democracy_exe/agentic/studio/react && {{UV_RUN}} python -m memory_agent

# Commitizen commands
# commit using commitizen
commit:
	{{UV_RUN}} cz commit

commit-help:
	{{UV_RUN}} cz commit -h

# bump version using commitizen
bump:
	{{UV_RUN}} cz bump

# tag using commitizen
tag:
	{{UV_RUN}} cz tag

# release using commitizen
release:
	{{UV_RUN}} cz release

# bump patch version using commitizen
bump-patch:
	{{UV_RUN}} cz bump --patch

# bump minor version using commitizen
bump-minor:
	{{UV_RUN}} cz bump --minor

# bump major version using commitizen
bump-major:
	{{UV_RUN}} cz bump --major

# bump prerelease version using commitizen
bump-prerelease:
	{{UV_RUN}} cz bump --prerelease

# bump postrelease version using commitizen
bump-postrelease:
	{{UV_RUN}} cz bump --postrelease

# Generate AI commit messages
ai-commit:
	aicommits --generate 3 --type conventional

# Run the bot
run:
	{{UV_RUN}} democracyctl run-bot

# https://github.com/langchain-ai/langchain/blob/fbf0704e48273d40a9068ee2078ffe4374185338/docs/docs/integrations/document_loaders/readthedocs_documentation.ipynb#L36

# Download the read the docs
download-read-the-docs:
	wget -r -A.html -P rtdocs https://python.langchain.com/en/latest/

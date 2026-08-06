# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

hier-config-cli is a Click-based CLI tool for network configuration analysis built on the `hier-config` library. It compares running and intended device configs to generate remediation, rollback, and future-state configurations. Supports 13 network platforms (Cisco IOS/NXOS/XR, Arista EOS, Aruba AOS-CX, Juniper JunOS, VyOS, FortiOS, HP Comware5/ProCurve, Huawei VRP, Nokia SR Linux, Generic).

## Build & Development Commands

All commands use **poetry** (not pip):

```bash
# Install dependencies
poetry install

# Full lint + test suite (equivalent to CI)
poetry run python scripts/build.py lint-and-test

# Lint only (ruff format + check, mypy, pyright, pylint, yamllint, flynt — run in parallel)
poetry run python scripts/build.py lint

# Auto-fix formatting and fixable lint issues
poetry run python scripts/build.py lint --fix

# Tests only (95% coverage required)
poetry run python scripts/build.py pytest --coverage

# Run a single test
poetry run pytest tests/test_cli.py::test_version_command -v

# Auto-format code
poetry run ruff format src tests scripts
```

## Architecture

The entire CLI lives in a single module: `src/hier_config_cli/__main__.py`. The entry point is the `cli()` Click group, registered as `hier-config-cli` in pyproject.toml.

**Key flow:** All three config commands (`remediation`, `rollback`, `future`) share the same pattern:
1. `common_options` decorator applies shared Click options (platform, running-config, generated-config, format, output)
2. `process_configs()` validates the platform, reads both config files via `hier_config.utils.read_text_from_file`, parses them with `HConfig.from_text()`, then runs the requested operation via `WorkflowRemediation` (for remediation/rollback) or `HConfig.future()` (for future)
3. `format_output()` converts the result HConfig to text/JSON/YAML
4. `get_output_text()` handles platform-specific formatting — JunOS uses `line.text`, all others use `line.indented_text()`

**PLATFORM_MAP** dict maps CLI string names to `hier_config.Platform` enum values. To add a new platform, add it here, handle any special output formatting in `get_output_text()`, and add tests.

## Code Standards

These mirror the hier_config library's standards and are enforced by `scripts/build.py lint`:

- Python 3.10+ (uses `X | Y` union syntax); CI tests 3.10–3.14
- `ruff format` for formatting (NOT black), line length 88
- ruff linting with `select = ["ALL"]` and preview rules; the ignore list in `pyproject.toml` is the authoritative configuration — never loosen it to make a change pass
- mypy strict + pyright strict; full type annotations everywhere, including tests. No `Any`, no unjustified `# type: ignore` or `# noqa`
- pylint with extension plugins for checks not covered by ruff; yamllint for YAML; flynt for f-string enforcement
- Google-style docstrings; use `r"""` when a docstring contains backslashes
- Conventional commits: `feat:`, `fix:`, `docs:`, `test:`, `refactor:`
- Every PR adds a CHANGELOG.md entry under `## [Unreleased]` (Keep a Changelog categories)

## Testing

- TDD: write a failing test first, confirm it fails for the right reason, implement minimally, then run the full suite. 95% coverage floor (enforced by `build.py pytest --coverage`).
- Flat function-based tests (no classes), fully annotated; shared fixtures live in `tests/conftest.py`.
- Tests use Click's `CliRunner` for CLI invocation testing. Fixtures provide mock Cisco IOS and Juniper JunOS configs via temporary files. `tests/test_cli.py` covers commands, output formats, platforms, and logging levels; `tests/test_helpers.py` covers error paths through the public helpers.

## CI/CD

- `test-app.yaml`: Runs `scripts/build.py lint` and `scripts/build.py pytest --coverage` on Python 3.10–3.14 for every push/PR to main and next
- `deploy.yaml`: Publishes to PyPI via Poetry on GitHub release creation
- Version is maintained in both `pyproject.toml` and `__main__.py:__version__`

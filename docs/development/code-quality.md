# Code Quality

This guide covers code quality standards and tools used in hier-config-cli.

## Overview

hier-config-cli maintains high code quality through:

- **Black**: Code formatting
- **Ruff**: Fast Python linting
- **mypy**: Static type checking
- **pytest**: Testing framework
- **pre-commit**: Automated checks

## Code Formatting with Black

[Black](https://black.readthedocs.io/) is used for consistent code formatting.

### Configuration

**pyproject.toml:**
```toml
[tool.black]
line-length = 100
target-version = ["py310", "py311", "py312", "py313"]
```

### Usage

```bash
# Format all code
black src/ tests/

# Check formatting without changes
black --check src/ tests/

# Show diff of changes
black --diff src/ tests/

# Format specific file
black src/hier_config_cli/__main__.py
```

### Integration

**VS Code settings.json:**
```json
{
    "python.formatting.provider": "black",
    "python.formatting.blackArgs": ["--line-length", "100"],
    "editor.formatOnSave": true
}
```

**PyCharm:**
1. Install Black plugin
2. Settings → Tools → Black → Enable
3. Set line length to 100

## Linting with Ruff

[Ruff](https://docs.astral.sh/ruff/) is an extremely fast Python linter.

### Configuration

**pyproject.toml:**
```toml
[tool.ruff]
line-length = 100
target-version = "py310"

[tool.ruff.lint]
select = [
    "E",   # pycodestyle errors
    "W",   # pycodestyle warnings
    "F",   # pyflakes
    "I",   # isort
    "B",   # flake8-bugbear
    "C4",  # flake8-comprehensions
    "UP",  # pyupgrade
]
ignore = []
```

### Usage

```bash
# Lint all code
ruff check src/ tests/

# Fix auto-fixable issues
ruff check --fix src/ tests/

# Show all violations
ruff check --output-format=full src/

# Watch for changes
ruff check --watch src/
```

### Common Rules

| Rule | Description | Example |
|------|-------------|---------|
| E501 | Line too long | Lines should be ≤100 chars |
| F401 | Unused import | Remove unused imports |
| F841 | Unused variable | Remove or use variable |
| B006 | Mutable default argument | Use `None` instead |
| UP006 | Use `list` instead of `List` | Modern type syntax |

### Fixing Issues

```python
# Before (E501 - line too long)
def long_function_name(param1, param2, param3, param4, param5, param6, param7):
    pass

# After
def long_function_name(
    param1, param2, param3,
    param4, param5, param6,
    param7,
):
    pass

# Before (F401 - unused import)
import json
import os  # Not used

# After
import json

# Before (B006 - mutable default)
def process(items=[]):
    pass

# After
def process(items=None):
    if items is None:
        items = []
```

## Type Checking with mypy

[mypy](https://mypy.readthedocs.io/) provides static type checking.

### Configuration

**pyproject.toml:**
```toml
[tool.mypy]
python_version = "3.10"
warn_return_any = false
warn_unused_configs = true
disallow_untyped_defs = true
disallow_incomplete_defs = true
check_untyped_defs = true
no_implicit_optional = true
warn_redundant_casts = true
warn_unused_ignores = false
strict_equality = true

[[tool.mypy.overrides]]
module = [
    "hier_config.*",
    "click.*",
]
ignore_missing_imports = true
```

### Usage

```bash
# Type check all code
mypy src/

# Check specific file
mypy src/hier_config_cli/__main__.py

# Show error codes
mypy --show-error-codes src/

# Generate coverage report
mypy --html-report mypy-report src/
```

### Writing Type-Safe Code

```python
from pathlib import Path
from typing import Optional, Union, List
from collections.abc import Callable

# Function with type hints
def read_config(
    path: Path,
    encoding: str = "utf-8",
) -> str:
    """Read configuration file.

    Args:
        path: Path to config file
        encoding: File encoding

    Returns:
        File contents as string

    Raises:
        FileNotFoundError: If file doesn't exist
    """
    return path.read_text(encoding=encoding)

# Using Optional for nullable values
def find_device(name: str) -> Optional[dict]:
    """Find device by name.

    Args:
        name: Device name

    Returns:
        Device dict if found, None otherwise
    """
    # Implementation
    return None

# Type aliases for clarity
DeviceConfig = dict[str, str]
ConfigList = list[DeviceConfig]

def process_devices(devices: ConfigList) -> None:
    """Process multiple device configurations."""
    pass

# Callable types
ProcessFunc = Callable[[str], str]

def apply_transform(data: str, func: ProcessFunc) -> str:
    """Apply transformation function to data."""
    return func(data)
```

### Common Type Errors

```python
# Error: Incompatible return type
def get_count() -> int:
    return "5"  # Error: expected int, got str

# Fix
def get_count() -> int:
    return 5

# Error: Missing type annotation
def process(data):  # Error: missing type hints
    return data

# Fix
def process(data: str) -> str:
    return data

# Error: Incompatible types in assignment
value: int = "hello"  # Error

# Fix
value: str = "hello"
```

## Pre-commit Hooks

[pre-commit](https://pre-commit.com/) runs checks before each commit.

### Installation

```bash
pip install pre-commit
pre-commit install
```

### Configuration

**.pre-commit-config.yaml:**
```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
      - id: check-merge-conflict

  - repo: https://github.com/psf/black
    rev: 24.10.0
    hooks:
      - id: black

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.8.4
    hooks:
      - id: ruff
        args: [--fix]

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.13.0
    hooks:
      - id: mypy
        additional_dependencies: [types-pyyaml]
        args: [--strict]
```

### Usage

```bash
# Run on all files
pre-commit run --all-files

# Run specific hook
pre-commit run black --all-files

# Skip hooks for a commit
git commit --no-verify

# Update hooks to latest versions
pre-commit autoupdate
```

## Code Review Checklist

Before submitting code for review:

### Functionality
- [ ] Code works as intended
- [ ] Edge cases are handled
- [ ] Error handling is appropriate
- [ ] No hardcoded values

### Code Quality
- [ ] Black formatting applied
- [ ] No Ruff violations
- [ ] mypy type checking passes
- [ ] Meaningful variable/function names
- [ ] Code is DRY (Don't Repeat Yourself)

### Testing
- [ ] Tests are written
- [ ] Tests pass
- [ ] Coverage is adequate
- [ ] Edge cases are tested

### Documentation
- [ ] Docstrings are present
- [ ] Comments explain "why", not "what"
- [ ] README updated if needed
- [ ] API docs updated if needed

### Security
- [ ] No secrets in code
- [ ] Input validation present
- [ ] No SQL injection risks
- [ ] No command injection risks

## Continuous Integration

### GitHub Actions Workflow

**.github/workflows/quality.yml:**
```yaml
name: Code Quality

on: [push, pull_request]

jobs:
  quality:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install poetry
          poetry install

      - name: Check formatting with Black
        run: poetry run black --check src/ tests/

      - name: Lint with Ruff
        run: poetry run ruff check src/ tests/

      - name: Type check with mypy
        run: poetry run mypy src/

      - name: Run tests
        run: poetry run pytest --cov=hier_config_cli

      - name: Check coverage threshold
        run: |
          poetry run pytest --cov=hier_config_cli --cov-fail-under=90
```

## Quality Metrics

### Code Coverage

Target: **>90% coverage**

```bash
# Generate coverage report
pytest --cov=hier_config_cli --cov-report=term-missing

# Fail if below threshold
pytest --cov=hier_config_cli --cov-fail-under=90
```

### Type Coverage

Target: **100% type coverage**

```bash
# Check type coverage
mypy --strict src/
```

### Complexity

Keep cyclomatic complexity low:

```bash
# Install radon
pip install radon

# Check complexity
radon cc src/ -a

# Grade: A is best, F is worst
# Aim for A or B grades
```

## Best Practices

### Code Organization

```python
# Good: Organized imports
import json
import sys
from pathlib import Path
from typing import Optional

import click
import yaml
from hier_config import HConfig

# Module-level constants
DEFAULT_TIMEOUT = 30
MAX_RETRIES = 3

# Functions and classes
def main() -> None:
    pass
```

### Error Messages

```python
# Good: Clear, actionable error messages
raise click.ClickException(
    f"Configuration file not found: {path}\n"
    f"Please check the path and try again."
)

# Bad: Vague error message
raise Exception("Error")
```

### Function Length

Keep functions focused and concise:

```python
# Good: Single responsibility
def read_file(path: Path) -> str:
    """Read file contents."""
    return path.read_text()

def parse_config(content: str) -> dict:
    """Parse configuration content."""
    return json.loads(content)

# Bad: Too much in one function
def read_and_parse_and_validate(path: Path) -> dict:
    content = path.read_text()
    data = json.loads(content)
    if not validate(data):
        raise ValueError("Invalid")
    return data
```

### Documentation

```python
# Good: Clear docstring with examples
def calculate_diff(
    running: str,
    intended: str,
) -> list[str]:
    """Calculate configuration differences.

    Args:
        running: Running configuration
        intended: Intended configuration

    Returns:
        List of commands needed for remediation

    Example:
        >>> calculate_diff("hostname old", "hostname new")
        ['no hostname old', 'hostname new']
    """
    pass
```

## Tools Summary

| Tool | Purpose | Command |
|------|---------|---------|
| Black | Code formatting | `black src/ tests/` |
| Ruff | Linting | `ruff check src/ tests/` |
| mypy | Type checking | `mypy src/` |
| pytest | Testing | `pytest` |
| pre-commit | Automated checks | `pre-commit run --all-files` |

## Next Steps

- Review [Testing Guide](testing.md)
- Read [Contributing Guidelines](contributing.md)
- Explore [Commands Reference](../commands.md)

# Contributing

Thank you for your interest in contributing to hier-config-cli! This document provides guidelines and instructions for contributing.

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for everyone.

## How to Contribute

### Reporting Bugs

If you find a bug, please open an issue on GitHub with:

- **Clear title** describing the issue
- **Detailed description** of the bug
- **Steps to reproduce** the issue
- **Expected behavior** vs actual behavior
- **Environment details** (OS, Python version, hier-config-cli version)
- **Sample configs** if applicable (sanitized)

**Example:**
```markdown
## Bug Report

### Description
hier-config-cli fails when processing FortiOS configurations with certain syntax.

### Steps to Reproduce
1. Run: `hier-config-cli remediation --platform fortios --running-config running.conf --generated-config intended.conf`
2. Error occurs during parsing

### Expected Behavior
Should generate remediation configuration

### Actual Behavior
Raises parsing error: [error message]

### Environment
- OS: Ubuntu 22.04
- Python: 3.11.5
- hier-config-cli: 0.2.0
- hier-config: 3.4.0
```

### Suggesting Features

Feature requests are welcome! Please open an issue with:

- **Clear use case** explaining why the feature would be useful
- **Detailed description** of the proposed functionality
- **Example usage** showing how it would work
- **Alternative solutions** you've considered

### Submitting Pull Requests

1. **Fork the repository**
2. **Create a feature branch** from `main`
3. **Make your changes**
4. **Add tests** for new functionality
5. **Update documentation** as needed
6. **Run all quality checks** (tests, linting, type checking)
7. **Submit a pull request**

## Development Setup

### Prerequisites

- Python 3.10 or higher
- Poetry for dependency management
- Git

### Initial Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/hier-config-cli.git
cd hier-config-cli

# Install dependencies
poetry install

# Activate virtual environment
poetry shell

# Verify installation
hier-config-cli version
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=hier_config_cli --cov-report=html

# Run specific test file
pytest tests/test_cli.py

# Run with verbose output
pytest -v

# Run and watch for changes
pytest-watch
```

### Code Quality Checks

Before submitting a PR, ensure all quality checks pass:

```bash
# Format code with black
black src/ tests/

# Check linting with ruff
ruff check src/ tests/

# Fix auto-fixable issues
ruff check --fix src/ tests/

# Type check with mypy
mypy src/

# Run all checks at once
black src/ tests/ && ruff check src/ tests/ && mypy src/ && pytest
```

### Pre-commit Hooks

We recommend using pre-commit hooks:

```bash
# Install pre-commit
pip install pre-commit

# Install hooks
pre-commit install

# Run manually
pre-commit run --all-files
```

**.pre-commit-config.yaml:**
```yaml
repos:
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
```

## Coding Standards

### Code Style

- Follow **PEP 8** style guidelines
- Use **Black** for code formatting (line length: 100)
- Use **type hints** for all functions
- Write **docstrings** for all public functions/classes

### Type Hints

```python
from pathlib import Path
from typing import Optional

def process_config(
    config_path: Path,
    platform: str,
    output_format: str = "text",
) -> str:
    """Process configuration file.

    Args:
        config_path: Path to configuration file
        platform: Platform name
        output_format: Output format (text, json, yaml)

    Returns:
        Processed configuration as string

    Raises:
        FileNotFoundError: If config file doesn't exist
        ValueError: If platform is unknown
    """
    # Implementation
    pass
```

### Docstring Style

Use Google-style docstrings:

```python
def example_function(param1: str, param2: int) -> bool:
    """Brief description of function.

    Longer description if needed. Can span multiple
    lines and paragraphs.

    Args:
        param1: Description of param1
        param2: Description of param2

    Returns:
        Description of return value

    Raises:
        ValueError: When param2 is negative
        TypeError: When param1 is not a string

    Example:
        >>> example_function("test", 42)
        True
    """
    pass
```

### Error Handling

```python
import click

# Use click.ClickException for user-facing errors
try:
    config = read_file(path)
except FileNotFoundError:
    raise click.ClickException(
        f"Configuration file not found: {path}"
    ) from None

# Chain exceptions for debugging
except Exception as e:
    raise click.ClickException(
        f"Error processing configuration: {e}"
    ) from e
```

## Writing Tests

### Test Structure

```python
import pytest
from pathlib import Path
from hier_config_cli import process_configs

def test_remediation_generation():
    """Test remediation configuration generation."""
    # Arrange
    platform = "ios"
    running_config = "test_data/running.conf"
    intended_config = "test_data/intended.conf"

    # Act
    result, platform_enum = process_configs(
        platform,
        running_config,
        intended_config,
        "remediation",
    )

    # Assert
    assert result is not None
    assert len(list(result.all_children())) > 0

def test_invalid_platform():
    """Test error handling for invalid platform."""
    with pytest.raises(click.ClickException) as exc_info:
        process_configs(
            "invalid_platform",
            "running.conf",
            "intended.conf",
            "remediation",
        )

    assert "Unknown platform" in str(exc_info.value)
```

### Test Coverage

- Aim for **>90% code coverage**
- Test **happy paths** and **error conditions**
- Include **edge cases**
- Use **fixtures** for common test data

```python
import pytest
from pathlib import Path

@pytest.fixture
def test_configs(tmp_path):
    """Create test configuration files."""
    running = tmp_path / "running.conf"
    running.write_text("hostname test-router\n")

    intended = tmp_path / "intended.conf"
    intended.write_text("hostname new-router\n")

    return {
        "running": str(running),
        "intended": str(intended),
    }

def test_with_fixture(test_configs):
    """Test using fixture."""
    result = process_configs(
        "ios",
        test_configs["running"],
        test_configs["intended"],
        "remediation",
    )
    assert result is not None
```

## Documentation

### Updating Documentation

- Update docs in the `docs/` directory
- Use Markdown format
- Include code examples
- Add links to related pages

### Building Documentation Locally

```bash
# Install mkdocs
pip install mkdocs mkdocs-material mkdocstrings[python]

# Serve locally
mkdocs serve

# Build static site
mkdocs build

# Open in browser
# Navigate to http://127.0.0.1:8000
```

### Documentation Style

- Use **clear, concise language**
- Provide **working examples**
- Include **expected output**
- Add **troubleshooting tips**
- Link to **related documentation**

## Pull Request Process

### Before Submitting

- [ ] All tests pass
- [ ] Code is formatted with Black
- [ ] No linting errors from Ruff
- [ ] Type checking passes with mypy
- [ ] Documentation is updated
- [ ] CHANGELOG.md is updated (if applicable)
- [ ] Commit messages are clear and descriptive

### PR Description Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
Describe the tests you ran and their results

## Checklist
- [ ] Tests pass locally
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] No new warnings
```

### Review Process

1. Maintainer reviews code
2. Automated checks run (tests, linting, type checking)
3. Feedback is provided if changes needed
4. Once approved, PR is merged

## Release Process

(For maintainers)

1. Update version in `pyproject.toml` and `src/hier_config_cli/__main__.py`
2. Update `CHANGELOG.md`
3. Create a git tag: `git tag v0.x.x`
4. Push tag: `git push origin v0.x.x`
5. GitHub Actions will build and publish to PyPI

## Getting Help

- **GitHub Issues**: [Report bugs or request features](https://github.com/netdevops/hier-config-cli/issues)
- **GitHub Discussions**: [Ask questions](https://github.com/netdevops/hier-config-cli/discussions)
- **Email**: james.williams@packetgeek.net

## Recognition

Contributors will be recognized in:
- CHANGELOG.md
- GitHub contributors page
- Release notes

Thank you for contributing to hier-config-cli!

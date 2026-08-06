# Contributing to Hier Config CLI

Thank you for your interest in contributing to Hier Config CLI! This document provides guidelines and instructions for contributing to the project.

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for all contributors.

## How to Contribute

### Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates. When creating a bug report, include:

- **Clear title and description**
- **Steps to reproduce** the issue
- **Expected behavior** vs actual behavior
- **Environment details** (OS, Python version, tool version)
- **Sample configurations** if applicable (sanitized of sensitive data)
- **Error messages** or stack traces

Example:
```markdown
**Bug**: Remediation fails on Juniper configs with curly braces

**To Reproduce**:
1. Run: `hier-config-cli remediation --platform junos --running-config r.conf --generated-config g.conf`
2. See error: ...

**Expected**: Should generate remediation commands
**Actual**: Raises ValueError

**Environment**: Python 3.11, hier-config-cli 0.2.0, Ubuntu 22.04
```

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion:

- **Use a clear and descriptive title**
- **Provide detailed description** of the proposed functionality
- **Explain why this enhancement would be useful**
- **Provide examples** of how it would be used
- **List alternatives** you've considered

### Pull Requests

1. **Fork the repository** and create your branch from `main`
2. **Follow the development workflow** (see below)
3. **Write tests** for new functionality
4. **Ensure all tests pass** and code quality checks succeed
5. **Update documentation** as needed
6. **Submit the pull request** with a clear description

#### Pull Request Process

1. Update the README.md or relevant documentation with details of changes
2. Add entries to CHANGELOG.md under "Unreleased" section
3. Ensure the full quality gate passes (`poetry run python scripts/build.py lint-and-test`)
4. Update type hints for any new functions or modified signatures
5. Request review from maintainers

## Development Workflow

### Setting Up Development Environment

```bash
# Clone your fork
git clone https://github.com/YOUR-USERNAME/hier-config-cli.git
cd hier-config-cli

# Add upstream remote
git remote add upstream https://github.com/netdevops/hier-config-cli.git

# Install dependencies
poetry install

# Activate virtual environment
poetry shell
```

### Creating a Branch

```bash
# Update your fork
git fetch upstream
git checkout main
git merge upstream/main

# Create feature branch
git checkout -b feature/your-feature-name
# or
git checkout -b fix/bug-description
```

### Making Changes

1. **Write code** following the project style guidelines
2. **Add tests** for new functionality
3. **Run tests** to ensure everything works
4. **Check code quality** with linters and type checker

```bash
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

### Committing Changes

Write clear, concise commit messages following conventional commits:

```bash
# Feature
git commit -m "feat: add support for FortiOS platform"

# Bug fix
git commit -m "fix: correct Junos output formatting"

# Documentation
git commit -m "docs: update installation instructions"

# Tests
git commit -m "test: add error handling tests"

# Refactor
git commit -m "refactor: consolidate duplicate command code"
```

### Submitting Pull Request

```bash
# Push to your fork
git push origin feature/your-feature-name

# Create pull request on GitHub
# Include:
# - Clear description of changes
# - Reference to related issues
# - Screenshots if applicable
# - Checklist of completed items
```

## Coding Standards

### Python Style Guide

- Follow [PEP 8](https://peps.python.org/pep-0008/) style guide
- Use [Ruff](https://github.com/astral-sh/ruff) for both formatting (`ruff format`, line length: 88) and linting (`select = ["ALL"]` with preview rules)
- Use [mypy](https://mypy.readthedocs.io/) (strict) and [pyright](https://microsoft.github.io/pyright/) (strict) for type checking
- Use [pylint](https://pylint.readthedocs.io/) with extension plugins for checks not covered by ruff
- Never loosen the lint or coverage configuration to make a change pass; do not add `# type: ignore` or `# noqa` suppressions without a justifying reason

### Code Organization

- Keep functions focused and single-purpose
- Use descriptive variable and function names
- Add docstrings to all public functions and classes
- Include type hints for all function signatures
- Avoid code duplication (DRY principle)

### Documentation Standards

#### Docstrings

Use Google-style docstrings:

```python
def process_configs(
    platform_str: str,
    running_config_path: str,
    generated_config_path: str,
    operation: str,
) -> tuple[HConfig, Platform]:
    """Process configuration files and return the result.

    Args:
        platform_str: Platform name string
        running_config_path: Path to running configuration
        generated_config_path: Path to generated configuration
        operation: Operation type (remediation, rollback, future)

    Returns:
        Tuple of (result HConfig, Platform enum)

    Raises:
        click.ClickException: If processing fails
    """
```

#### Type Hints

Always include type hints:

```python
from typing import Optional
from pathlib import Path

def save_output(content: str, filepath: Optional[Path] = None) -> None:
    """Save output to file."""
    if filepath:
        filepath.write_text(content)
```

### Testing Standards

- Write tests first (TDD): add a failing test, confirm it fails for the right reason, then implement minimally
- Flat function-based tests (no test classes), with full type annotations
- Shared fixtures live in `tests/conftest.py`
- Maintain the 95% coverage floor (CI enforces it); test both happy paths and error cases
- Test the CLI through Click's `CliRunner`
- Use descriptive test names and include docstrings in test functions

```python
def test_remediation_with_invalid_platform(
    mock_running_config: str,
    mock_generated_config: str
) -> None:
    """Test that remediation fails gracefully with invalid platform."""
    runner = CliRunner()
    result = runner.invoke(
        cli,
        [
            "remediation",
            "--platform", "invalid_platform",
            "--running-config", mock_running_config,
            "--generated-config", mock_generated_config,
        ],
    )
    assert result.exit_code != 0
    assert "Unknown platform" in result.output
```

## Project Structure

```
hier-config-cli/
├── src/
│   └── hier_config_cli/
│       ├── __main__.py      # Main CLI code
│       └── py.typed         # Type hints marker
├── tests/
│   ├── conftest.py          # Shared fixtures
│   ├── test_cli.py          # CLI command tests
│   └── test_helpers.py      # Helper/error-path tests
├── scripts/
│   └── build.py             # Parallel lint/test runner
├── examples/                # Example configurations
│   ├── cisco_ios_running.conf
│   ├── cisco_ios_intended.conf
│   └── README.md
├── .github/
│   └── workflows/           # CI/CD workflows
├── .yamllint.yml            # yamllint configuration
├── pyproject.toml           # Project configuration
├── README.md                # Main documentation
├── CONTRIBUTING.md          # This file
├── CHANGELOG.md             # Version history
├── SECURITY.md              # Security policy
└── LICENSE                  # License file
```

## Adding New Platforms

To add support for a new network platform:

1. Add the platform to `PLATFORM_MAP` in `src/hier_config_cli/__main__.py`
2. Ensure proper output formatting in `get_output_text()` function
3. Add test cases for the new platform
4. Update documentation (README.md, examples)
5. Add example configuration files if available

Example:
```python
PLATFORM_MAP = {
    # ... existing platforms ...
    "new_platform": Platform.NEW_PLATFORM,
}
```

## Adding New Features

When adding new features:

1. **Discuss first** by opening an issue to get feedback
2. **Design carefully** considering backwards compatibility
3. **Write tests** covering new functionality
4. **Document thoroughly** in code and README
5. **Update CHANGELOG** with your changes

## Releasing

Maintainers handle releases. The process is automated by two GitHub Actions
workflows and requires repository admin permission:

1. Run the **Prepare Release** workflow (`prepare-release.yml`) from the
   Actions tab: pick the branch to release from in the "Run workflow"
   dropdown and choose the bump type (`major`, `minor`, `patch`, or
   `prerelease`). The workflow bumps the version in `pyproject.toml` and
   `src/hier_config_cli/__main__.py`, rotates the `## [Unreleased]`
   CHANGELOG section into a dated release section (skipped for
   prereleases), opens a release PR against the chosen branch, and creates
   a draft GitHub release `vX.Y.Z` targeting that branch.
2. Review and merge the release PR.
3. Publish the draft release on GitHub.
4. Publishing the release triggers the **Release** workflow
   (`release.yml`), which builds and publishes the package to PyPI
   automatically (`poetry publish --build` using the `PYPI_TOKEN` secret).

## Getting Help

- **Questions**: Open a [GitHub Discussion](https://github.com/netdevops/hier-config-cli/discussions)
- **Bugs**: Open a [GitHub Issue](https://github.com/netdevops/hier-config-cli/issues)
- **Chat**: Join our community channels (if available)

## Recognition

Contributors will be recognized in:
- GitHub contributors list
- CHANGELOG.md for significant contributions
- Project README (for major features)

## License

By contributing, you agree that your contributions will be licensed under the Apache License 2.0.

---

Thank you for contributing to Hier Config CLI! Your efforts help make network automation better for everyone.

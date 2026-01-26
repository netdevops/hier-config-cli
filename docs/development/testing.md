# Testing

This guide covers testing practices and procedures for hier-config-cli.

## Test Framework

hier-config-cli uses [pytest](https://pytest.org/) as its testing framework, along with pytest-cov for coverage reporting.

## Running Tests

### Basic Test Execution

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_cli.py

# Run specific test function
pytest tests/test_cli.py::test_remediation_command

# Run tests matching a pattern
pytest -k "remediation"
```

### Coverage Reporting

```bash
# Run with coverage
pytest --cov=hier_config_cli

# Generate HTML coverage report
pytest --cov=hier_config_cli --cov-report=html

# Open coverage report
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux

# Generate XML coverage report (for CI)
pytest --cov=hier_config_cli --cov-report=xml
```

### Watch Mode

For development, use pytest-watch to automatically run tests on file changes:

```bash
# Install pytest-watch
pip install pytest-watch

# Run in watch mode
ptw
```

## Test Structure

### Directory Layout

```
tests/
├── __init__.py
├── conftest.py          # Shared fixtures
├── test_cli.py          # CLI command tests
├── test_config.py       # Configuration processing tests
├── test_formats.py      # Output format tests
└── fixtures/            # Test data
    ├── configs/
    │   ├── ios/
    │   │   ├── running.conf
    │   │   └── intended.conf
    │   └── nxos/
    │       ├── running.conf
    │       └── intended.conf
    └── expected/
        └── remediation/
            └── ios_remediation.txt
```

### Test File Organization

```python
"""Tests for CLI commands."""

import pytest
from click.testing import CliRunner
from hier_config_cli import cli

class TestRemediationCommand:
    """Tests for remediation command."""

    def test_basic_remediation(self, test_configs):
        """Test basic remediation generation."""
        pass

    def test_remediation_with_output_file(self, test_configs, tmp_path):
        """Test remediation with output file."""
        pass

    def test_remediation_json_format(self, test_configs):
        """Test remediation with JSON output."""
        pass

class TestRollbackCommand:
    """Tests for rollback command."""

    def test_basic_rollback(self, test_configs):
        """Test basic rollback generation."""
        pass
```

## Writing Tests

### Test Fixtures

**conftest.py:**
```python
"""Shared test fixtures."""

import pytest
from pathlib import Path

@pytest.fixture
def test_data_dir():
    """Return path to test data directory."""
    return Path(__file__).parent / "fixtures"

@pytest.fixture
def ios_configs(test_data_dir, tmp_path):
    """Create temporary IOS config files."""
    # Copy test configs to temp directory
    running_config = """hostname router-01
interface GigabitEthernet0/0
 description WAN Interface
 ip address 10.0.1.1 255.255.255.0
!
"""
    intended_config = """hostname router-01-updated
interface GigabitEthernet0/0
 description WAN Interface - Updated
 ip address 10.0.1.1 255.255.255.0
!
interface Vlan20
 description Guest VLAN
 ip address 10.0.20.1 255.255.255.0
!
"""

    running_file = tmp_path / "running.conf"
    running_file.write_text(running_config)

    intended_file = tmp_path / "intended.conf"
    intended_file.write_text(intended_config)

    return {
        "platform": "ios",
        "running": str(running_file),
        "intended": str(intended_file),
    }

@pytest.fixture
def cli_runner():
    """Return Click CLI test runner."""
    return CliRunner()
```

### CLI Testing

```python
from click.testing import CliRunner
from hier_config_cli import cli

def test_remediation_command(cli_runner, ios_configs):
    """Test remediation command."""
    result = cli_runner.invoke(
        cli,
        [
            "remediation",
            "--platform", ios_configs["platform"],
            "--running-config", ios_configs["running"],
            "--generated-config", ios_configs["intended"],
        ],
    )

    assert result.exit_code == 0
    assert "Remediation Configuration" in result.output
    assert "hostname router-01-updated" in result.output

def test_remediation_with_output_file(cli_runner, ios_configs, tmp_path):
    """Test remediation with output file."""
    output_file = tmp_path / "remediation.txt"

    result = cli_runner.invoke(
        cli,
        [
            "remediation",
            "--platform", ios_configs["platform"],
            "--running-config", ios_configs["running"],
            "--generated-config", ios_configs["intended"],
            "--output", str(output_file),
        ],
    )

    assert result.exit_code == 0
    assert output_file.exists()
    content = output_file.read_text()
    assert "hostname router-01-updated" in content

def test_invalid_platform(cli_runner, ios_configs):
    """Test error handling for invalid platform."""
    result = cli_runner.invoke(
        cli,
        [
            "remediation",
            "--platform", "invalid",
            "--running-config", ios_configs["running"],
            "--generated-config", ios_configs["intended"],
        ],
    )

    assert result.exit_code != 0
    assert "Unknown platform" in result.output
```

### Testing Output Formats

```python
import json
import yaml

def test_json_output(cli_runner, ios_configs):
    """Test JSON output format."""
    result = cli_runner.invoke(
        cli,
        [
            "remediation",
            "--platform", ios_configs["platform"],
            "--running-config", ios_configs["running"],
            "--generated-config", ios_configs["intended"],
            "--format", "json",
        ],
    )

    assert result.exit_code == 0

    # Parse JSON output
    # Skip the header line
    json_output = "\n".join(result.output.split("\n")[1:])
    data = json.loads(json_output)

    assert "config" in data
    assert isinstance(data["config"], list)
    assert len(data["config"]) > 0

def test_yaml_output(cli_runner, ios_configs):
    """Test YAML output format."""
    result = cli_runner.invoke(
        cli,
        [
            "remediation",
            "--platform", ios_configs["platform"],
            "--running-config", ios_configs["running"],
            "--generated-config", ios_configs["intended"],
            "--format", "yaml",
        ],
    )

    assert result.exit_code == 0

    # Parse YAML output
    yaml_output = "\n".join(result.output.split("\n")[1:])
    data = yaml.safe_load(yaml_output)

    assert "config" in data
    assert isinstance(data["config"], list)
```

### Parameterized Tests

```python
@pytest.mark.parametrize("platform,expected", [
    ("ios", "cisco_style"),
    ("nxos", "cisco_style"),
    ("iosxr", "cisco_style"),
    ("eos", "cisco_style"),
])
def test_multiple_platforms(cli_runner, tmp_path, platform, expected):
    """Test remediation for multiple platforms."""
    # Create test configs
    running = tmp_path / "running.conf"
    running.write_text("hostname old-device\n")

    intended = tmp_path / "intended.conf"
    intended.write_text("hostname new-device\n")

    result = cli_runner.invoke(
        cli,
        [
            "remediation",
            "--platform", platform,
            "--running-config", str(running),
            "--generated-config", str(intended),
        ],
    )

    assert result.exit_code == 0
    assert "new-device" in result.output
```

### Testing Error Conditions

```python
def test_missing_running_config(cli_runner, tmp_path):
    """Test error when running config is missing."""
    intended = tmp_path / "intended.conf"
    intended.write_text("hostname test\n")

    result = cli_runner.invoke(
        cli,
        [
            "remediation",
            "--platform", "ios",
            "--running-config", str(tmp_path / "nonexistent.conf"),
            "--generated-config", str(intended),
        ],
    )

    assert result.exit_code != 0
    assert "not found" in result.output.lower()

def test_permission_error(cli_runner, ios_configs, tmp_path):
    """Test error handling for permission issues."""
    import os

    # Create unreadable file
    unreadable = tmp_path / "unreadable.conf"
    unreadable.write_text("hostname test\n")
    os.chmod(unreadable, 0o000)

    result = cli_runner.invoke(
        cli,
        [
            "remediation",
            "--platform", "ios",
            "--running-config", str(unreadable),
            "--generated-config", ios_configs["intended"],
        ],
    )

    # Cleanup
    os.chmod(unreadable, 0o644)

    assert result.exit_code != 0
    assert "permission" in result.output.lower()
```

## Test Coverage Goals

### Coverage Targets

- **Overall**: >90%
- **Critical paths**: 100%
- **Error handling**: >95%
- **CLI commands**: >95%

### Checking Coverage

```bash
# Generate coverage report
pytest --cov=hier_config_cli --cov-report=term-missing

# View detailed coverage
pytest --cov=hier_config_cli --cov-report=html
open htmlcov/index.html
```

### Coverage Configuration

**pyproject.toml:**
```toml
[tool.coverage.run]
source = ["src"]
omit = ["*/tests/*", "*/__pycache__/*"]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError",
    "raise NotImplementedError",
    "if __name__ == .__main__.:",
    "if TYPE_CHECKING:",
]
```

## Integration Tests

### Full Workflow Tests

```python
def test_complete_workflow(cli_runner, ios_configs, tmp_path):
    """Test complete remediation workflow."""
    remediation_file = tmp_path / "remediation.txt"
    rollback_file = tmp_path / "rollback.txt"
    future_file = tmp_path / "future.txt"

    # Generate remediation
    result = cli_runner.invoke(
        cli,
        [
            "remediation",
            "--platform", ios_configs["platform"],
            "--running-config", ios_configs["running"],
            "--generated-config", ios_configs["intended"],
            "--output", str(remediation_file),
        ],
    )
    assert result.exit_code == 0
    assert remediation_file.exists()

    # Generate rollback
    result = cli_runner.invoke(
        cli,
        [
            "rollback",
            "--platform", ios_configs["platform"],
            "--running-config", ios_configs["running"],
            "--generated-config", ios_configs["intended"],
            "--output", str(rollback_file),
        ],
    )
    assert result.exit_code == 0
    assert rollback_file.exists()

    # Generate future state
    result = cli_runner.invoke(
        cli,
        [
            "future",
            "--platform", ios_configs["platform"],
            "--running-config", ios_configs["running"],
            "--generated-config", ios_configs["intended"],
            "--output", str(future_file),
        ],
    )
    assert result.exit_code == 0
    assert future_file.exists()
```

## Performance Tests

```python
import time

def test_performance_large_config(cli_runner, tmp_path):
    """Test performance with large configuration."""
    # Generate large config
    lines = ["interface GigabitEthernet0/{}\n description Test\n".format(i)
             for i in range(1000)]

    running = tmp_path / "running.conf"
    running.write_text("".join(lines))

    intended = tmp_path / "intended.conf"
    intended.write_text("".join(lines) + "ntp server 192.0.2.1\n")

    start_time = time.time()

    result = cli_runner.invoke(
        cli,
        [
            "remediation",
            "--platform", "ios",
            "--running-config", str(running),
            "--generated-config", str(intended),
        ],
    )

    duration = time.time() - start_time

    assert result.exit_code == 0
    assert duration < 5.0  # Should complete in under 5 seconds
```

## CI/CD Integration

### GitHub Actions

**.github/workflows/test.yml:**
```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
        python-version: ['3.10', '3.11', '3.12']

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}

      - name: Install dependencies
        run: |
          pip install poetry
          poetry install

      - name: Run tests
        run: |
          poetry run pytest --cov=hier_config_cli --cov-report=xml

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage.xml
```

## Best Practices

1. **Write tests first** (TDD approach when possible)
2. **Test both success and failure paths**
3. **Use meaningful test names** that describe what is being tested
4. **Keep tests isolated** - each test should be independent
5. **Use fixtures** for common setup
6. **Mock external dependencies** when appropriate
7. **Aim for high coverage** but focus on meaningful tests
8. **Run tests before committing**
9. **Keep tests fast** - slow tests won't be run often
10. **Update tests** when changing functionality

## Next Steps

- Learn about [Code Quality](code-quality.md) standards
- Review [Contributing Guidelines](contributing.md)
- Explore the [Commands Reference](../commands.md)

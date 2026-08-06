"""Comprehensive tests for hier-config-cli."""

import json
from pathlib import Path

import pytest
import yaml
from click.testing import CliRunner

from hier_config_cli import cli


# Define test fixtures for mock configurations
@pytest.fixture
def mock_running_config(tmp_path: Path) -> str:
    """Create a mock running configuration file.

    Args:
        tmp_path: Pytest temporary directory fixture

    Returns:
        Path to the mock running config file
    """
    config_path = tmp_path / "running_config.conf"
    config_path.write_text(
        "hostname test-router\ninterface Vlan1\n ip address 10.0.0.1 255.255.255.0\n"
    )
    return str(config_path)


@pytest.fixture
def mock_generated_config(tmp_path: Path) -> str:
    """Create a mock generated configuration file.

    Args:
        tmp_path: Pytest temporary directory fixture

    Returns:
        Path to the mock generated config file
    """
    config_path = tmp_path / "generated_config.conf"
    config_path.write_text(
        "hostname test-router-updated\n"
        "interface Vlan1\n"
        " ip address 10.0.0.1 255.255.255.0\n"
        "interface Vlan2\n"
        " ip address 10.0.1.1 255.255.255.0\n"
    )
    return str(config_path)


@pytest.fixture
def mock_junos_running_config(tmp_path: Path) -> str:
    """Create a mock Junos running configuration file.

    Args:
        tmp_path: Pytest temporary directory fixture

    Returns:
        Path to the mock Junos running config file
    """
    config_path = tmp_path / "junos_running.conf"
    config_path.write_text("system {\n    host-name test-router;\n}\n")
    return str(config_path)


@pytest.fixture
def mock_junos_generated_config(tmp_path: Path) -> str:
    """Create a mock Junos generated configuration file.

    Args:
        tmp_path: Pytest temporary directory fixture

    Returns:
        Path to the mock Junos generated config file
    """
    config_path = tmp_path / "junos_generated.conf"
    config_path.write_text("system {\n    host-name test-router-updated;\n}\n")
    return str(config_path)


# Test `version` command
def test_version_command() -> None:
    """Test the version command."""
    runner = CliRunner()
    result = runner.invoke(cli, ["version"])
    assert result.exit_code == 0
    assert "hier-config-cli version" in result.output
    assert "0.2.0" in result.output


# Test `list_platforms` command
def test_list_platforms() -> None:
    """Test listing available platforms."""
    runner = CliRunner()
    result = runner.invoke(cli, ["list-platforms"])
    assert result.exit_code == 0
    assert "Available Platforms" in result.output
    assert "ios" in result.output
    assert "junos" in result.output
    assert "fortios" in result.output
    assert "nxos" in result.output


# Test `remediation` command - happy path
def test_remediation_command(mock_running_config: str, mock_generated_config: str) -> None:
    """Test remediation command with valid inputs."""
    runner = CliRunner()
    result = runner.invoke(
        cli,
        [
            "remediation",
            "--platform",
            "ios",
            "--running-config",
            mock_running_config,
            "--generated-config",
            mock_generated_config,
        ],
    )
    assert result.exit_code == 0
    assert "Remediation Configuration" in result.output
    assert "no hostname test-router" in result.output
    assert "hostname test-router-updated" in result.output


# Test `remediation` command - JSON output
def test_remediation_json_output(mock_running_config: str, mock_generated_config: str) -> None:
    """Test remediation command with JSON output format."""
    runner = CliRunner()
    result = runner.invoke(
        cli,
        [
            "remediation",
            "--platform",
            "ios",
            "--running-config",
            mock_running_config,
            "--generated-config",
            mock_generated_config,
            "--format",
            "json",
        ],
    )
    assert result.exit_code == 0
    # Parse JSON to verify it's valid
    output_lines = result.output.split("\n")
    json_start = next(i for i, line in enumerate(output_lines) if line.strip().startswith("{"))
    json_output = "\n".join(output_lines[json_start:])
    data = json.loads(json_output)
    assert "config" in data
    assert isinstance(data["config"], list)


# Test `remediation` command - YAML output
def test_remediation_yaml_output(mock_running_config: str, mock_generated_config: str) -> None:
    """Test remediation command with YAML output format."""
    runner = CliRunner()
    result = runner.invoke(
        cli,
        [
            "remediation",
            "--platform",
            "ios",
            "--running-config",
            mock_running_config,
            "--generated-config",
            mock_generated_config,
            "--format",
            "yaml",
        ],
    )
    assert result.exit_code == 0
    # Parse YAML to verify it's valid
    output_lines = result.output.split("\n")
    yaml_start = next(i for i, line in enumerate(output_lines) if "config:" in line)
    yaml_output = "\n".join(output_lines[yaml_start:])
    data = yaml.safe_load(yaml_output)
    assert "config" in data
    assert isinstance(data["config"], list)


# Test `remediation` command - output to file
def test_remediation_output_file(
    mock_running_config: str, mock_generated_config: str, tmp_path: Path
) -> None:
    """Test remediation command with output to file."""
    output_file = tmp_path / "output.txt"
    runner = CliRunner()
    result = runner.invoke(
        cli,
        [
            "remediation",
            "--platform",
            "ios",
            "--running-config",
            mock_running_config,
            "--generated-config",
            mock_generated_config,
            "--output",
            str(output_file),
        ],
    )
    assert result.exit_code == 0
    assert output_file.exists()
    content = output_file.read_text()
    assert "no hostname test-router" in content
    assert "hostname test-router-updated" in content


# Test `rollback` command
def test_rollback_command(mock_running_config: str, mock_generated_config: str) -> None:
    """Test rollback command with valid inputs."""
    runner = CliRunner()
    result = runner.invoke(
        cli,
        [
            "rollback",
            "--platform",
            "ios",
            "--running-config",
            mock_running_config,
            "--generated-config",
            mock_generated_config,
        ],
    )
    assert result.exit_code == 0
    assert "Rollback Configuration" in result.output
    assert "hostname test-router" in result.output
    assert "no hostname test-router-updated" in result.output


# Test `future` command
def test_future_command(mock_running_config: str, mock_generated_config: str) -> None:
    """Test future command with valid inputs."""
    runner = CliRunner()
    result = runner.invoke(
        cli,
        [
            "future",
            "--platform",
            "ios",
            "--running-config",
            mock_running_config,
            "--generated-config",
            mock_generated_config,
        ],
    )
    assert result.exit_code == 0
    assert "Future Configuration" in result.output
    assert "hostname test-router-updated" in result.output


# Error handling tests
def test_invalid_platform(mock_running_config: str, mock_generated_config: str) -> None:
    """Test error handling for invalid platform."""
    runner = CliRunner()
    result = runner.invoke(
        cli,
        [
            "remediation",
            "--platform",
            "invalid_platform",
            "--running-config",
            mock_running_config,
            "--generated-config",
            mock_generated_config,
        ],
    )
    assert result.exit_code != 0


def test_missing_running_config(mock_generated_config: str) -> None:
    """Test error handling for missing running config file."""
    runner = CliRunner()
    result = runner.invoke(
        cli,
        [
            "remediation",
            "--platform",
            "ios",
            "--running-config",
            "/nonexistent/file.conf",
            "--generated-config",
            mock_generated_config,
        ],
    )
    assert result.exit_code != 0
    assert "does not exist" in result.output


def test_missing_generated_config(mock_running_config: str) -> None:
    """Test error handling for missing generated config file."""
    runner = CliRunner()
    result = runner.invoke(
        cli,
        [
            "remediation",
            "--platform",
            "ios",
            "--running-config",
            mock_running_config,
            "--generated-config",
            "/nonexistent/file.conf",
        ],
    )
    assert result.exit_code != 0
    assert "does not exist" in result.output


def test_unreadable_file(tmp_path: Path, mock_generated_config: str) -> None:
    """Test error handling for unreadable config file."""
    unreadable_file = tmp_path / "unreadable.conf"
    unreadable_file.write_text("hostname test")
    unreadable_file.chmod(0o000)

    runner = CliRunner()
    result = runner.invoke(
        cli,
        [
            "remediation",
            "--platform",
            "ios",
            "--running-config",
            str(unreadable_file),
            "--generated-config",
            mock_generated_config,
        ],
    )

    # Clean up permissions
    unreadable_file.chmod(0o644)

    assert result.exit_code != 0


# Test verbose logging
def test_verbose_logging(mock_running_config: str, mock_generated_config: str) -> None:
    """Test verbose logging output."""
    runner = CliRunner()
    result = runner.invoke(
        cli,
        [
            "-v",
            "remediation",
            "--platform",
            "ios",
            "--running-config",
            mock_running_config,
            "--generated-config",
            mock_generated_config,
        ],
    )
    assert result.exit_code == 0


def test_very_verbose_logging(mock_running_config: str, mock_generated_config: str) -> None:
    """Test very verbose (debug) logging output."""
    runner = CliRunner()
    result = runner.invoke(
        cli,
        [
            "-vv",
            "remediation",
            "--platform",
            "ios",
            "--running-config",
            mock_running_config,
            "--generated-config",
            mock_generated_config,
        ],
    )
    assert result.exit_code == 0


# Test all platforms
@pytest.mark.parametrize(
    "platform",
    [
        "ios",
        "nxos",
        "iosxr",
        "eos",
        "junos",
        "vyos",
        "fortios",
        "generic",
        "hp_comware5",
        "hp_procurve",
        "aruba_aoscx",
        "huawei_vrp",
        "nokia_srl",
    ],
)
def test_all_platforms(platform: str, mock_running_config: str, mock_generated_config: str) -> None:
    """Test remediation command works with all supported platforms."""
    runner = CliRunner()
    result = runner.invoke(
        cli,
        [
            "remediation",
            "--platform",
            platform,
            "--running-config",
            mock_running_config,
            "--generated-config",
            mock_generated_config,
        ],
    )
    assert result.exit_code == 0


# Test Junos platform with appropriate configs
def test_junos_platform_specific(
    mock_junos_running_config: str, mock_junos_generated_config: str
) -> None:
    """Test Junos platform with Junos-specific configurations."""
    runner = CliRunner()
    result = runner.invoke(
        cli,
        [
            "remediation",
            "--platform",
            "junos",
            "--running-config",
            mock_junos_running_config,
            "--generated-config",
            mock_junos_generated_config,
        ],
    )
    assert result.exit_code == 0


# Test help text
def test_help_command() -> None:
    """Test help command output."""
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "Hier Config CLI Tool" in result.output
    assert "remediation" in result.output
    assert "rollback" in result.output
    assert "future" in result.output


def test_remediation_help() -> None:
    """Test remediation command help output."""
    runner = CliRunner()
    result = runner.invoke(cli, ["remediation", "--help"])
    assert result.exit_code == 0
    assert "Generate the remediation configuration" in result.output
    assert "--platform" in result.output
    assert "--running-config" in result.output
    assert "--generated-config" in result.output

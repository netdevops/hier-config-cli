import pytest
from click.testing import CliRunner
from hier_config_cli import cli


# Define test fixtures for mock configurations
@pytest.fixture
def mock_running_config(tmp_path):
    config_path = tmp_path / "running_config.conf"
    config_path.write_text("hostname test-router\ninterface Vlan1\n")
    return str(config_path)


@pytest.fixture
def mock_generated_config(tmp_path):
    config_path = tmp_path / "generated_config.conf"
    config_path.write_text(
        "hostname test-router-updated\ninterface Vlan1\n ip address 10.0.0.1 255.255.255.0\n"
    )
    return str(config_path)


# Test `list_platforms` command
def test_list_platforms():
    runner = CliRunner()
    result = runner.invoke(cli, ["list-platforms"])
    assert result.exit_code == 0
    assert "Available Platforms" in result.output
    assert "ios" in result.output
    assert "junos" in result.output


# Test `remediation` command
def test_remediation_command(mock_running_config, mock_generated_config):
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


# Test `rollback` command
def test_rollback_command(mock_running_config, mock_generated_config):
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
def test_future_command(mock_running_config, mock_generated_config):
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

"""Unit tests for hier-config-cli error paths."""

from pathlib import Path

import click
import pytest
from click.testing import CliRunner
from hier_config import HConfig, Platform

from hier_config_cli import cli
from hier_config_cli.__main__ import format_output, process_configs


def test_format_output_unsupported_format() -> None:
    """Test that format_output raises ValueError for an unknown format."""
    hconfig = HConfig.from_text(Platform.CISCO_IOS, "hostname test")
    with pytest.raises(ValueError, match="Unsupported output format: xml"):
        format_output(hconfig, Platform.CISCO_IOS, "xml")


def test_process_configs_unknown_platform(
    mock_running_config: str, mock_generated_config: str
) -> None:
    """Test that process_configs rejects an unknown platform name."""
    with pytest.raises(click.ClickException, match="Unknown platform: bogus"):
        process_configs(
            "bogus",
            mock_running_config,
            mock_generated_config,
            "remediation",
        )


def test_process_configs_missing_file(mock_generated_config: str) -> None:
    """Test that process_configs reports a missing config file cleanly."""
    with pytest.raises(click.ClickException, match="file not found"):
        process_configs(
            "ios",
            "/nonexistent/config.conf",
            mock_generated_config,
            "remediation",
        )


def test_process_configs_permission_denied(
    tmp_path: Path, mock_generated_config: str
) -> None:
    """Test that process_configs reports a permission error cleanly."""
    protected = tmp_path / "protected.conf"
    protected.write_text("hostname test", encoding="utf-8")
    protected.chmod(0o000)
    with pytest.raises(click.ClickException, match="Permission denied"):
        process_configs(
            "ios",
            str(protected),
            mock_generated_config,
            "remediation",
        )
    # Clean up permissions so pytest can remove the temporary directory
    protected.chmod(0o644)


def test_process_configs_read_os_error(
    tmp_path: Path, mock_generated_config: str
) -> None:
    """Test that process_configs reports other read failures cleanly."""
    # Reading a directory raises IsADirectoryError, an OSError that is
    # neither FileNotFoundError nor PermissionError.
    with pytest.raises(click.ClickException, match="Error reading running config"):
        process_configs(
            "ios",
            str(tmp_path),
            mock_generated_config,
            "remediation",
        )


def test_process_configs_parse_error(
    monkeypatch: pytest.MonkeyPatch,
    mock_running_config: str,
    mock_generated_config: str,
) -> None:
    """Test that parser failures are converted to a clean CLI error."""

    def _raise(_platform: Platform, _text: str) -> HConfig:
        message = "boom"
        raise RuntimeError(message)

    monkeypatch.setattr(HConfig, "from_text", _raise)
    with pytest.raises(click.ClickException, match="Error parsing configuration: boom"):
        process_configs(
            "ios",
            mock_running_config,
            mock_generated_config,
            "remediation",
        )


def test_process_configs_generate_error(
    monkeypatch: pytest.MonkeyPatch,
    mock_running_config: str,
    mock_generated_config: str,
) -> None:
    """Test that operation failures are converted to a clean CLI error."""

    def _raise(_operation: str, _running: HConfig, _generated: HConfig) -> HConfig:
        message = "boom"
        raise RuntimeError(message)

    monkeypatch.setattr("hier_config_cli.__main__._run_operation", _raise)
    with pytest.raises(
        click.ClickException,
        match="Error generating remediation: boom",
    ):
        process_configs(
            "ios",
            mock_running_config,
            mock_generated_config,
            "remediation",
        )


def test_format_error_reported_via_cli(
    monkeypatch: pytest.MonkeyPatch,
    mock_running_config: str,
    mock_generated_config: str,
) -> None:
    """Test that formatting failures surface as a clean CLI error."""

    def _raise(_hconfig: HConfig, _platform: Platform, _output_format: str) -> str:
        message = "bad format"
        raise ValueError(message)

    monkeypatch.setattr("hier_config_cli.__main__.format_output", _raise)
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
    assert result.exit_code != 0
    assert "bad format" in result.output


def test_output_file_write_error(
    mock_running_config: str, mock_generated_config: str, tmp_path: Path
) -> None:
    """Test the CLI reports a clean error when the output file cannot be written."""
    bad_output = tmp_path / "missing_dir" / "out.txt"
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
            str(bad_output),
        ],
    )
    assert result.exit_code != 0
    assert "Error writing output file" in result.output

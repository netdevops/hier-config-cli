"""Shared fixtures for hier-config-cli tests."""

from pathlib import Path

import pytest


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
        "hostname test-router\ninterface Vlan1\n ip address 10.0.0.1 255.255.255.0\n",
        encoding="utf-8",
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
        " ip address 10.0.1.1 255.255.255.0\n",
        encoding="utf-8",
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
    config_path.write_text(
        "system {\n    host-name test-router;\n}\n", encoding="utf-8"
    )
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
    config_path.write_text(
        "system {\n    host-name test-router-updated;\n}\n", encoding="utf-8"
    )
    return str(config_path)

# Hier Config CLI

[![PyPI version](https://badge.fury.io/py/hier-config-cli.svg)](https://badge.fury.io/py/hier-config-cli)
[![Python Versions](https://img.shields.io/pypi/pyversions/hier-config-cli.svg)](https://pypi.org/project/hier-config-cli/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Tests](https://github.com/netdevops/hier-config-cli/workflows/test-app/badge.svg)](https://github.com/netdevops/hier-config-cli/actions)

A powerful command-line interface tool for network configuration analysis, remediation, and rollback built on top of the [Hier Config](https://github.com/netdevops/hier_config) library.

## Overview

**hier-config-cli** helps network engineers analyze configuration differences, generate remediation commands, prepare rollback procedures, and predict configuration states across multiple network platforms. It's an essential tool for network automation workflows, change management, and configuration compliance.

## Key Features

- **Remediation Generation**: Automatically generate commands to transform running config into intended config
- **Rollback Planning**: Create rollback procedures before making changes
- **Future State Prediction**: Preview the complete configuration after applying changes
- **Multi-Platform Support**: Works with Cisco, Juniper, Arista, HP, Fortinet, VyOS, and more
- **Multiple Output Formats**: Export as text, JSON, or YAML
- **Type-Safe**: Fully typed Python code with mypy support
- **Well-Tested**: Comprehensive test suite with high code coverage
- **Detailed Logging**: Verbose and debug modes for troubleshooting

## Use Cases

### Change Management

Before applying configuration changes to network devices, use hier-config-cli to:

1. Generate the exact commands needed for remediation
2. Create rollback procedures in case of issues
3. Preview the final configuration state
4. Document changes for approval workflows

### Configuration Compliance

Ensure network devices match their intended configurations:

1. Compare running configs against golden configs
2. Identify configuration drift
3. Generate remediation to bring devices into compliance

### Network Automation

Integrate with your automation tools:

- **CI/CD Pipelines**: Validate configuration changes in pull requests
- **Nornir**: Scale configuration analysis across hundreds of devices
- **Ansible**: Generate dynamic remediation playbooks

## Quick Example

```bash
# Generate remediation commands
hier-config-cli remediation \
  --platform ios \
  --running-config running.conf \
  --generated-config intended.conf

# Output:
# === Remediation Configuration ===
# no hostname router-01
# hostname router-01-updated
# interface GigabitEthernet0/0
#  description WAN Interface - Updated
```

## Get Started

Ready to dive in? Check out the [Installation](installation.md) guide and [Quick Start](quick-start.md) tutorial.

## Links

- **GitHub**: [netdevops/hier-config-cli](https://github.com/netdevops/hier-config-cli)
- **PyPI**: [hier-config-cli](https://pypi.org/project/hier-config-cli/)
- **Issues**: [Report a bug](https://github.com/netdevops/hier-config-cli/issues)
- **Hier Config Library**: [netdevops/hier_config](https://github.com/netdevops/hier_config)

## Acknowledgments

Built on top of the excellent [Hier Config](https://github.com/netdevops/hier_config) library by James Williams and contributors.

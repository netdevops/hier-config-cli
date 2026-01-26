# API Reference

This page provides detailed API documentation for hier-config-cli's Python modules.

## Command-Line Interface

### Main CLI Group

::: hier_config_cli.cli
    options:
      show_root_heading: true
      show_source: true

## Core Functions

### Configuration Processing

::: hier_config_cli.process_configs
    options:
      show_root_heading: true
      show_source: true

### Output Formatting

::: hier_config_cli.format_output
    options:
      show_root_heading: true
      show_source: true

::: hier_config_cli.get_output_text
    options:
      show_root_heading: true
      show_source: true

### Logging

::: hier_config_cli.setup_logging
    options:
      show_root_heading: true
      show_source: true

## Commands

### Remediation Command

::: hier_config_cli.remediation
    options:
      show_root_heading: true
      show_source: true

### Rollback Command

::: hier_config_cli.rollback
    options:
      show_root_heading: true
      show_source: true

### Future Command

::: hier_config_cli.future
    options:
      show_root_heading: true
      show_source: true

### List Platforms Command

::: hier_config_cli.list_platforms
    options:
      show_root_heading: true
      show_source: true

### Version Command

::: hier_config_cli.version
    options:
      show_root_heading: true
      show_source: true

## Constants

### Platform Mapping

The `PLATFORM_MAP` dictionary maps platform names to `hier_config.Platform` enum values:

```python
PLATFORM_MAP = {
    "ios": Platform.CISCO_IOS,
    "nxos": Platform.CISCO_NXOS,
    "iosxr": Platform.CISCO_XR,
    "eos": Platform.ARISTA_EOS,
    "junos": Platform.JUNIPER_JUNOS,
    "vyos": Platform.VYOS,
    "fortios": Platform.FORTINET_FORTIOS,
    "generic": Platform.GENERIC,
    "hp_comware5": Platform.HP_COMWARE5,
    "hp_procurve": Platform.HP_PROCURVE,
}
```

## Type Definitions

### Common Types

```python
from pathlib import Path
from typing import Optional, Union

# Configuration path types
ConfigPath = Union[str, Path]

# Output format types
OutputFormat = Literal["text", "json", "yaml"]

# Operation types
Operation = Literal["remediation", "rollback", "future"]
```

## Usage Examples

### Programmatic Usage

While hier-config-cli is primarily a CLI tool, you can use its functions programmatically:

```python
from hier_config_cli import process_configs, format_output
from pathlib import Path

# Process configurations
result, platform = process_configs(
    platform_str="ios",
    running_config_path="configs/running.conf",
    generated_config_path="configs/intended.conf",
    operation="remediation",
)

# Format output
output = format_output(
    hconfig=result,
    platform=platform,
    output_format="text",
)

print(output)
```

### Custom Integration

```python
import subprocess
import json
from pathlib import Path

def generate_remediation(
    platform: str,
    running_config: Path,
    intended_config: Path,
) -> dict:
    """Generate remediation using hier-config-cli.

    Args:
        platform: Platform name
        running_config: Path to running config
        intended_config: Path to intended config

    Returns:
        Remediation data as dictionary

    Raises:
        subprocess.CalledProcessError: If command fails
    """
    result = subprocess.run(
        [
            "hier-config-cli",
            "remediation",
            "--platform", platform,
            "--running-config", str(running_config),
            "--generated-config", str(intended_config),
            "--format", "json",
        ],
        capture_output=True,
        text=True,
        check=True,
    )

    return json.loads(result.stdout)

# Usage
remediation = generate_remediation(
    platform="ios",
    running_config=Path("configs/running.conf"),
    intended_config=Path("configs/intended.conf"),
)

for command in remediation["config"]:
    print(command)
```

## Error Handling

### Exception Types

hier-config-cli uses `click.ClickException` for all user-facing errors:

```python
from click import ClickException

try:
    result = process_configs(
        platform_str="invalid",
        running_config_path="running.conf",
        generated_config_path="intended.conf",
        operation="remediation",
    )
except ClickException as e:
    print(f"Error: {e.message}")
```

### Common Exceptions

| Exception | Cause | Message Example |
|-----------|-------|-----------------|
| `ClickException` | Unknown platform | "Unknown platform: invalid_platform" |
| `ClickException` | File not found | "Running config file not found: path/to/file" |
| `ClickException` | Permission denied | "Permission denied reading running config: path/to/file" |
| `ClickException` | Parsing error | "Error parsing configuration: [details]" |

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Error occurred |

## Environment Variables

hier-config-cli doesn't use environment variables directly, but respects standard Python environment variables:

| Variable | Purpose |
|----------|---------|
| `PYTHONPATH` | Python module search path |
| `PYTHONDONTWRITEBYTECODE` | Disable .pyc files |

## Logging

### Log Levels

Control logging verbosity with the `-v` flag:

```bash
# WARNING level (default)
hier-config-cli remediation ...

# INFO level
hier-config-cli -v remediation ...

# DEBUG level
hier-config-cli -vv remediation ...
```

### Log Format

```
LEVEL: message
```

Examples:
```
INFO: Using platform: ios
INFO: Reading running config from: running.conf
INFO: Reading generated config from: intended.conf
INFO: Parsing configurations
INFO: Generating remediation configuration
```

## Related Documentation

- [Commands Reference](commands.md) - Detailed command documentation
- [Integration Guide](integration/index.md) - Integration examples
- [Development Guide](development/contributing.md) - Contributing guidelines

## External Dependencies

hier-config-cli depends on:

- [hier-config](https://github.com/netdevops/hier_config) - Core configuration analysis
- [click](https://click.palletsprojects.com/) - CLI framework
- [PyYAML](https://pyyaml.org/) - YAML support

Refer to their documentation for advanced usage and features.

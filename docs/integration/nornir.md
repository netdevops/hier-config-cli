# Nornir Integration

[Nornir](https://nornir.readthedocs.io/) is a Python-based automation framework designed for network engineers. This guide shows how to integrate hier-config-cli with Nornir for scalable network configuration management.

## Overview

Nornir excels at running tasks across multiple devices in parallel, making it ideal for large-scale network automation. Combined with hier-config-cli, you can:

- Generate remediation for hundreds of devices concurrently
- Validate configuration changes before deployment
- Create comprehensive rollback procedures
- Automate compliance checking

## Basic Integration

### Installation

```bash
pip install nornir nornir-napalm nornir-utils hier-config-cli
```

### Simple Example

```python
from nornir import InitNornir
from nornir.core.task import Task, Result
import subprocess

def generate_remediation(task: Task) -> Result:
    """Generate remediation configuration for a device."""

    # Run hier-config-cli
    cmd = [
        "hier-config-cli",
        "remediation",
        "--platform", task.host.platform,
        "--running-config", f"configs/running/{task.host.name}.conf",
        "--generated-config", f"configs/intended/{task.host.name}.conf",
        "--output", f"configs/remediation/{task.host.name}.txt",
    ]

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
    )

    if result.returncode == 0:
        return Result(
            host=task.host,
            result=f"Remediation generated successfully",
            changed=True,
        )
    else:
        return Result(
            host=task.host,
            failed=True,
            result=f"Error: {result.stderr}",
        )

# Initialize Nornir
nr = InitNornir(config_file="config.yaml")

# Run task on all hosts
results = nr.run(task=generate_remediation)

# Print results
for host, result in results.items():
    print(f"{host}: {result.result}")
```

## Complete Workflow Example

### Directory Structure

```
nornir-automation/
├── config.yaml
├── inventory/
│   ├── hosts.yaml
│   ├── groups.yaml
│   └── defaults.yaml
├── configs/
│   ├── running/
│   ├── intended/
│   ├── remediation/
│   └── rollback/
└── tasks/
    └── hier_config_tasks.py
```

### Nornir Configuration (config.yaml)

```yaml
---
inventory:
  plugin: SimpleInventory
  options:
    host_file: "inventory/hosts.yaml"
    group_file: "inventory/groups.yaml"
    defaults_file: "inventory/defaults.yaml"

runner:
  plugin: threaded
  options:
    num_workers: 20
```

### Inventory (inventory/hosts.yaml)

```yaml
---
router1:
  hostname: 192.168.1.1
  platform: ios
  groups:
    - cisco_routers

router2:
  hostname: 192.168.1.2
  platform: ios
  groups:
    - cisco_routers

switch1:
  hostname: 192.168.1.10
  platform: nxos
  groups:
    - cisco_switches

firewall1:
  hostname: 192.168.1.254
  platform: fortios
  groups:
    - firewalls
```

### Advanced Task Module (tasks/hier_config_tasks.py)

```python
"""Hier Config CLI tasks for Nornir."""

from pathlib import Path
import subprocess
from typing import Optional
from nornir.core.task import Task, Result


def run_hier_config_cli(
    task: Task,
    operation: str,
    running_config_path: Optional[str] = None,
    intended_config_path: Optional[str] = None,
    output_path: Optional[str] = None,
    output_format: str = "text",
) -> Result:
    """
    Run hier-config-cli command.

    Args:
        task: Nornir task object
        operation: Operation to perform (remediation, rollback, future)
        running_config_path: Path to running config (defaults to configs/running/{hostname}.conf)
        intended_config_path: Path to intended config (defaults to configs/intended/{hostname}.conf)
        output_path: Path for output file (optional)
        output_format: Output format (text, json, yaml)

    Returns:
        Nornir Result object
    """
    # Set default paths
    if not running_config_path:
        running_config_path = f"configs/running/{task.host.name}.conf"
    if not intended_config_path:
        intended_config_path = f"configs/intended/{task.host.name}.conf"

    # Build command
    cmd = [
        "hier-config-cli",
        operation,
        "--platform", task.host.platform,
        "--running-config", running_config_path,
        "--generated-config", intended_config_path,
        "--format", output_format,
    ]

    if output_path:
        cmd.extend(["--output", output_path])

    # Execute command
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
    )

    if result.returncode == 0:
        return Result(
            host=task.host,
            result=result.stdout if not output_path else f"Output written to {output_path}",
            changed=True,
        )
    else:
        return Result(
            host=task.host,
            failed=True,
            result=result.stderr,
        )


def generate_remediation(task: Task) -> Result:
    """Generate remediation configuration."""
    return run_hier_config_cli(
        task,
        operation="remediation",
        output_path=f"configs/remediation/{task.host.name}.txt",
    )


def generate_rollback(task: Task) -> Result:
    """Generate rollback configuration."""
    return run_hier_config_cli(
        task,
        operation="rollback",
        output_path=f"configs/rollback/{task.host.name}.txt",
    )


def generate_future(task: Task) -> Result:
    """Generate future configuration state."""
    return run_hier_config_cli(
        task,
        operation="future",
        output_path=f"configs/future/{task.host.name}.txt",
    )


def complete_workflow(task: Task) -> Result:
    """
    Run complete hier-config workflow.

    Generates:
    1. Remediation configuration
    2. Rollback configuration
    3. Future state prediction
    """
    results = []

    # Generate remediation
    remediation = task.run(task=generate_remediation)
    results.append(f"Remediation: {remediation.result}")

    # Generate rollback
    rollback = task.run(task=generate_rollback)
    results.append(f"Rollback: {rollback.result}")

    # Generate future state
    future = task.run(task=generate_future)
    results.append(f"Future: {future.result}")

    return Result(
        host=task.host,
        result="\n".join(results),
        changed=True,
    )
```

### Main Script (main.py)

```python
#!/usr/bin/env python3
"""Main Nornir automation script."""

from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from tasks.hier_config_tasks import (
    generate_remediation,
    generate_rollback,
    generate_future,
    complete_workflow,
)


def main():
    """Run main automation workflow."""
    # Initialize Nornir
    nr = InitNornir(config_file="config.yaml")

    # Filter to specific platform if needed
    # ios_devices = nr.filter(platform="ios")

    print("=" * 80)
    print("Running Complete Hier Config Workflow")
    print("=" * 80)

    # Run complete workflow on all devices
    results = nr.run(task=complete_workflow)

    # Print results
    print_result(results)

    # Check for failures
    failed_hosts = [host for host, result in results.items() if result.failed]

    if failed_hosts:
        print(f"\n❌ Failed hosts: {', '.join(failed_hosts)}")
        return 1
    else:
        print(f"\n✅ All {len(results)} devices processed successfully")
        return 0


if __name__ == "__main__":
    exit(main())
```

## Integration with NAPALM

Combine hier-config-cli with NAPALM to fetch running configs:

```python
from nornir import InitNornir
from nornir_napalm.plugins.tasks import napalm_get
from nornir.core.task import Task, Result
import subprocess
from pathlib import Path


def fetch_and_analyze(task: Task) -> Result:
    """Fetch running config and generate remediation."""

    # Fetch running config with NAPALM
    result = task.run(task=napalm_get, getters=["config"])
    running_config = result.result["config"]["running"]

    # Save running config
    running_path = f"configs/running/{task.host.name}.conf"
    Path(running_path).write_text(running_config)

    # Generate remediation
    cmd = [
        "hier-config-cli",
        "remediation",
        "--platform", task.host.platform,
        "--running-config", running_path,
        "--generated-config", f"configs/intended/{task.host.name}.conf",
        "--output", f"configs/remediation/{task.host.name}.txt",
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode == 0:
        return Result(
            host=task.host,
            result="Config fetched and remediation generated",
            changed=True,
        )
    else:
        return Result(
            host=task.host,
            failed=True,
            result=result.stderr,
        )


# Initialize and run
nr = InitNornir(config_file="config.yaml")
results = nr.run(task=fetch_and_analyze)
```

## Error Handling

```python
from nornir.core.exceptions import NornirExecutionError


def safe_remediation(task: Task) -> Result:
    """Generate remediation with error handling."""
    try:
        cmd = [
            "hier-config-cli",
            "remediation",
            "--platform", task.host.platform,
            "--running-config", f"configs/running/{task.host.name}.conf",
            "--generated-config", f"configs/intended/{task.host.name}.conf",
            "--output", f"configs/remediation/{task.host.name}.txt",
        ]

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True,
        )

        return Result(
            host=task.host,
            result="Success",
            changed=True,
        )

    except subprocess.CalledProcessError as e:
        return Result(
            host=task.host,
            failed=True,
            result=f"Command failed: {e.stderr}",
        )
    except FileNotFoundError as e:
        return Result(
            host=task.host,
            failed=True,
            result=f"File not found: {e}",
        )
    except Exception as e:
        return Result(
            host=task.host,
            failed=True,
            result=f"Unexpected error: {e}",
        )
```

## Best Practices

1. **Use Nornir's filtering** to target specific device groups
2. **Leverage parallel execution** for large device counts
3. **Implement proper error handling** for production use
4. **Store configs in version control**
5. **Use NAPALM** to fetch live configs when needed
6. **Create separate tasks** for different operations
7. **Log all operations** for audit trails

## Next Steps

- Explore [Ansible Integration](ansible.md)
- Learn about [CI/CD Integration](cicd.md)
- Review [Commands Reference](../commands.md)

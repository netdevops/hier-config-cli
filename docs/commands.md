# Commands Reference

This page provides a detailed reference for all available hier-config-cli commands.

## Global Options

These options are available for all commands:

| Option | Short | Description |
|--------|-------|-------------|
| `--verbose` | `-v` | Increase verbosity. Use `-v` for INFO level, `-vv` for DEBUG level |
| `--help` | `-h` | Show help message and exit |

## Commands

### `remediation`

Generates the commands needed to transform the running configuration into the intended configuration.

**Synopsis:**
```bash
hier-config-cli remediation [OPTIONS]
```

**Options:**

| Option | Required | Description |
|--------|----------|-------------|
| `--platform` | Yes | Target platform (ios, nxos, iosxr, eos, junos, vyos, fortios, etc.) |
| `--running-config` | Yes | Path to the running configuration file |
| `--generated-config` | Yes | Path to the intended/generated configuration file |
| `--format` | No | Output format: `text`, `json`, or `yaml` (default: text) |
| `--output`, `-o` | No | Write output to file instead of stdout |

**Examples:**

```bash
# Basic usage
hier-config-cli remediation \
  --platform ios \
  --running-config running.conf \
  --generated-config intended.conf

# Save to file
hier-config-cli remediation \
  --platform ios \
  --running-config running.conf \
  --generated-config intended.conf \
  --output remediation.txt

# JSON format
hier-config-cli remediation \
  --platform nxos \
  --running-config running.conf \
  --generated-config intended.conf \
  --format json

# With verbose logging
hier-config-cli -v remediation \
  --platform iosxr \
  --running-config running.conf \
  --generated-config intended.conf
```

---

### `rollback`

Generates the commands needed to revert from the intended configuration back to the running configuration. This is useful for preparing rollback procedures before making changes.

**Synopsis:**
```bash
hier-config-cli rollback [OPTIONS]
```

**Options:**

Same as `remediation` command.

**Examples:**

```bash
# Basic usage
hier-config-cli rollback \
  --platform ios \
  --running-config running.conf \
  --generated-config intended.conf

# Save to file
hier-config-cli rollback \
  --platform eos \
  --running-config running.conf \
  --generated-config intended.conf \
  --output rollback.txt

# YAML format
hier-config-cli rollback \
  --platform junos \
  --running-config running.conf \
  --generated-config intended.conf \
  --format yaml
```

---

### `future`

Predicts what the complete configuration will look like after applying the intended configuration to the running configuration.

**Synopsis:**
```bash
hier-config-cli future [OPTIONS]
```

**Options:**

Same as `remediation` command.

**Examples:**

```bash
# Basic usage
hier-config-cli future \
  --platform ios \
  --running-config running.conf \
  --generated-config intended.conf

# Save to file
hier-config-cli future \
  --platform vyos \
  --running-config running.conf \
  --generated-config intended.conf \
  --output future_state.txt

# JSON format
hier-config-cli future \
  --platform fortios \
  --running-config running.conf \
  --generated-config intended.conf \
  --format json
```

---

### `list-platforms`

Lists all available and supported network platforms.

**Synopsis:**
```bash
hier-config-cli list-platforms
```

**Options:**

None

**Example:**

```bash
hier-config-cli list-platforms
```

**Output:**
```
=== Available Platforms ===
  eos
  fortios
  generic
  hp_comware5
  hp_procurve
  ios
  iosxr
  junos
  nxos
  vyos
```

---

### `version`

Shows the installed version of hier-config-cli.

**Synopsis:**
```bash
hier-config-cli version
```

**Options:**

None

**Example:**

```bash
hier-config-cli version
```

**Output:**
```
hier-config-cli version 0.2.0
```

## Common Usage Patterns

### Complete Change Workflow

```bash
# 1. Generate remediation
hier-config-cli remediation \
  --platform ios \
  --running-config running.conf \
  --generated-config intended.conf \
  --output remediation.txt

# 2. Generate rollback (for safety)
hier-config-cli rollback \
  --platform ios \
  --running-config running.conf \
  --generated-config intended.conf \
  --output rollback.txt

# 3. Preview future state
hier-config-cli future \
  --platform ios \
  --running-config running.conf \
  --generated-config intended.conf \
  --output future.txt

# 4. Review all files before applying changes
cat remediation.txt
cat rollback.txt
cat future.txt
```

### Batch Processing Multiple Devices

```bash
# Process multiple devices
for device in router1 router2 switch1; do
  hier-config-cli remediation \
    --platform ios \
    --running-config configs/${device}_running.conf \
    --generated-config configs/${device}_intended.conf \
    --output remediation/${device}_remediation.txt
done
```

### Using with Different Platforms

```bash
# Cisco IOS
hier-config-cli remediation --platform ios \
  --running-config ios_running.conf \
  --generated-config ios_intended.conf

# Cisco NX-OS
hier-config-cli remediation --platform nxos \
  --running-config nxos_running.conf \
  --generated-config nxos_intended.conf

# Arista EOS
hier-config-cli remediation --platform eos \
  --running-config eos_running.conf \
  --generated-config eos_intended.conf

# Juniper JunOS
hier-config-cli remediation --platform junos \
  --running-config junos_running.conf \
  --generated-config junos_intended.conf
```

## Exit Codes

| Code | Description |
|------|-------------|
| 0 | Success |
| 1 | Error (file not found, invalid platform, parsing error, etc.) |

## Error Handling

The CLI provides clear error messages for common issues:

**File Not Found:**
```
Error: Running config file not found: /path/to/missing.conf
```

**Invalid Platform:**
```
Error: Unknown platform: invalid_platform. Use 'list-platforms' to see available platforms.
```

**Permission Denied:**
```
Error: Permission denied reading running config: /path/to/file.conf
```

## Tips

1. **Use Tab Completion**: If your shell supports it, enable tab completion for easier command entry
2. **Combine with Shell Tools**: Pipe output to `less`, `grep`, or other tools for analysis
3. **Check File Paths**: Always use absolute paths or ensure you're in the correct directory
4. **Review Before Applying**: Always review generated commands before applying them to production devices

# Output Formats

hier-config-cli supports multiple output formats to integrate with different workflows and tools.

## Available Formats

| Format | Description | Use Case |
|--------|-------------|----------|
| `text` | Plain text output (default) | Human reading, direct device application |
| `json` | JSON format | API integration, programmatic processing |
| `yaml` | YAML format | Configuration management, human-readable structured data |

## Text Format (Default)

The default text format outputs configuration commands in a format ready to be applied to network devices.

**Usage:**
```bash
hier-config-cli remediation \
  --platform ios \
  --running-config running.conf \
  --generated-config intended.conf \
  --format text
```

**Example Output:**
```
=== Remediation Configuration ===
no hostname router-01
hostname router-01-updated
interface GigabitEthernet0/0
 no description WAN Interface
 description WAN Interface - Updated
interface Vlan20
 description Guest VLAN
 ip address 10.0.20.1 255.255.255.0
router ospf 1
 network 10.0.20.0 0.0.0.255 area 0
ntp server 192.0.2.1
```

**When to Use:**
- Directly copying commands to device CLI
- Manual review of changes
- Documentation and change records
- Generating configuration snippets

---

## JSON Format

JSON format provides structured output for programmatic processing.

**Usage:**
```bash
hier-config-cli remediation \
  --platform ios \
  --running-config running.conf \
  --generated-config intended.conf \
  --format json
```

**Example Output:**
```json
{
  "config": [
    "no hostname router-01",
    "hostname router-01-updated",
    "interface GigabitEthernet0/0",
    " no description WAN Interface",
    " description WAN Interface - Updated",
    "interface Vlan20",
    " description Guest VLAN",
    " ip address 10.0.20.1 255.255.255.0",
    "router ospf 1",
    " network 10.0.20.0 0.0.0.255 area 0",
    "ntp server 192.0.2.1"
  ]
}
```

**When to Use:**
- REST API integration
- Processing with JavaScript/Node.js
- Storing in document databases
- Web application integration
- CI/CD pipeline processing

**Example - Processing with Python:**
```python
import json
import subprocess

result = subprocess.run(
    [
        "hier-config-cli",
        "remediation",
        "--platform", "ios",
        "--running-config", "running.conf",
        "--generated-config", "intended.conf",
        "--format", "json",
    ],
    capture_output=True,
    text=True,
)

data = json.loads(result.stdout)
commands = data["config"]

for cmd in commands:
    print(f"Command: {cmd}")
```

**Example - Processing with jq:**
```bash
hier-config-cli remediation \
  --platform ios \
  --running-config running.conf \
  --generated-config intended.conf \
  --format json | jq '.config[]'
```

---

## YAML Format

YAML format provides human-readable structured output.

**Usage:**
```bash
hier-config-cli remediation \
  --platform ios \
  --running-config running.conf \
  --generated-config intended.conf \
  --format yaml
```

**Example Output:**
```yaml
config:
- no hostname router-01
- hostname router-01-updated
- interface GigabitEthernet0/0
- ' no description WAN Interface'
- ' description WAN Interface - Updated'
- interface Vlan20
- ' description Guest VLAN'
- ' ip address 10.0.20.1 255.255.255.0'
- router ospf 1
- ' network 10.0.20.0 0.0.0.255 area 0'
- ntp server 192.0.2.1
```

**When to Use:**
- Ansible playbooks
- Configuration management systems
- Human-readable structured data
- Git-friendly diffs
- Documentation

**Example - Using with Ansible:**
```yaml
- name: Generate and apply remediation
  hosts: routers
  tasks:
    - name: Generate remediation configuration
      command: >
        hier-config-cli remediation
        --platform ios
        --running-config /tmp/{{ inventory_hostname }}_running.conf
        --generated-config /tmp/{{ inventory_hostname }}_intended.conf
        --format yaml
      register: remediation_output

    - name: Parse YAML output
      set_fact:
        remediation_commands: "{{ remediation_output.stdout | from_yaml }}"

    - name: Display commands
      debug:
        var: remediation_commands.config
```

---

## Saving Output to Files

All formats can be saved to files using the `--output` or `-o` option:

```bash
# Save text output
hier-config-cli remediation \
  --platform ios \
  --running-config running.conf \
  --generated-config intended.conf \
  --format text \
  --output remediation.txt

# Save JSON output
hier-config-cli remediation \
  --platform ios \
  --running-config running.conf \
  --generated-config intended.conf \
  --format json \
  --output remediation.json

# Save YAML output
hier-config-cli remediation \
  --platform ios \
  --running-config running.conf \
  --generated-config intended.conf \
  --format yaml \
  --output remediation.yml
```

## Format Comparison

### Text Format
**Pros:**
- ✅ Ready to apply directly to devices
- ✅ Easy to read
- ✅ Compact output

**Cons:**
- ❌ No structure for programmatic parsing
- ❌ Harder to process with scripts

### JSON Format
**Pros:**
- ✅ Easy to parse programmatically
- ✅ Wide language support
- ✅ Standard format for APIs

**Cons:**
- ❌ More verbose
- ❌ Requires parsing before use
- ❌ Less human-readable

### YAML Format
**Pros:**
- ✅ Human-readable
- ✅ Easy to parse
- ✅ Good for configuration management
- ✅ Git-friendly

**Cons:**
- ❌ Requires parsing before use
- ❌ Whitespace-sensitive

## Choosing the Right Format

**Use Text when:**
- Manually reviewing changes
- Copying commands to device CLI
- Creating documentation
- Quick visual inspection

**Use JSON when:**
- Building REST APIs
- Processing with web applications
- Integrating with JavaScript/Node.js
- Storing in document databases

**Use YAML when:**
- Working with Ansible
- Need human-readable structured data
- Using configuration management tools
- Want Git-friendly diffs

## Advanced Usage

### Combining Formats

Process multiple formats in a single workflow:

```bash
# Generate text for manual review
hier-config-cli remediation \
  --platform ios \
  --running-config running.conf \
  --generated-config intended.conf \
  --format text \
  --output remediation.txt

# Generate JSON for automation
hier-config-cli remediation \
  --platform ios \
  --running-config running.conf \
  --generated-config intended.conf \
  --format json \
  --output remediation.json

# Generate YAML for Ansible
hier-config-cli remediation \
  --platform ios \
  --running-config running.conf \
  --generated-config intended.conf \
  --format yaml \
  --output remediation.yml
```

### Format Conversion

Convert between formats using standard tools:

```bash
# JSON to YAML
cat remediation.json | yq eval -P - > remediation.yml

# YAML to JSON
cat remediation.yml | yq eval -o=json - > remediation.json
```

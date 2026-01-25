# Examples

This directory contains example configuration files for various network platforms to demonstrate the capabilities of hier-config-cli.

## Cisco IOS Example

The `cisco_ios_running.conf` and `cisco_ios_intended.conf` files demonstrate a typical use case:

- **Running config**: Current device configuration
- **Intended config**: Desired device configuration with updates

### Generate Remediation Configuration

```bash
hier-config-cli remediation \
  --platform ios \
  --running-config examples/cisco_ios_running.conf \
  --generated-config examples/cisco_ios_intended.conf
```

This will output the commands needed to transform the running configuration into the intended configuration:

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

### Generate Rollback Configuration

```bash
hier-config-cli rollback \
  --platform ios \
  --running-config examples/cisco_ios_running.conf \
  --generated-config examples/cisco_ios_intended.conf
```

This will output the commands needed to rollback from the intended configuration to the running configuration.

### Generate Future Configuration

```bash
hier-config-cli future \
  --platform ios \
  --running-config examples/cisco_ios_running.conf \
  --generated-config examples/cisco_ios_intended.conf
```

This will show what the complete configuration will look like after applying the remediation.

### Output Formats

You can export configurations in different formats:

**JSON:**
```bash
hier-config-cli remediation \
  --platform ios \
  --running-config examples/cisco_ios_running.conf \
  --generated-config examples/cisco_ios_intended.conf \
  --format json
```

**YAML:**
```bash
hier-config-cli remediation \
  --platform ios \
  --running-config examples/cisco_ios_running.conf \
  --generated-config examples/cisco_ios_intended.conf \
  --format yaml
```

**Save to File:**
```bash
hier-config-cli remediation \
  --platform ios \
  --running-config examples/cisco_ios_running.conf \
  --generated-config examples/cisco_ios_intended.conf \
  --output remediation.txt
```

## Other Platforms

The tool supports multiple platforms. See `hier-config-cli list-platforms` for all available options:

- ios (Cisco IOS)
- nxos (Cisco NX-OS)
- iosxr (Cisco IOS XR)
- eos (Arista EOS)
- junos (Juniper JunOS)
- vyos (VyOS)
- fortios (Fortinet FortiOS)
- hp_comware5 (HP Comware5)
- hp_procurve (HP ProCurve)
- generic (Generic platform)

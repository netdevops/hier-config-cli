# Quick Start

This guide will walk you through your first steps with hier-config-cli.

## Prerequisites

Make sure you have hier-config-cli installed. See the [Installation](installation.md) guide if you haven't already.

## Basic Workflow

The typical workflow with hier-config-cli involves three main operations:

1. **Remediation**: Generate commands to transform running config into intended config
2. **Rollback**: Generate commands to revert changes (for safety)
3. **Future**: Preview the final configuration state

## Example Configuration Files

For this tutorial, we'll use simple Cisco IOS configurations.

### Running Configuration (running.conf)

```
hostname router-01
!
interface GigabitEthernet0/0
 description WAN Interface
 ip address 10.0.1.1 255.255.255.0
!
interface Vlan10
 description Management VLAN
 ip address 10.0.10.1 255.255.255.0
!
router ospf 1
 network 10.0.1.0 0.0.0.255 area 0
 network 10.0.10.0 0.0.0.255 area 0
!
```

### Intended Configuration (intended.conf)

```
hostname router-01-updated
!
interface GigabitEthernet0/0
 description WAN Interface - Updated
 ip address 10.0.1.1 255.255.255.0
!
interface Vlan10
 description Management VLAN
 ip address 10.0.10.1 255.255.255.0
!
interface Vlan20
 description Guest VLAN
 ip address 10.0.20.1 255.255.255.0
!
router ospf 1
 network 10.0.1.0 0.0.0.255 area 0
 network 10.0.10.0 0.0.0.255 area 0
 network 10.0.20.0 0.0.0.255 area 0
!
ntp server 192.0.2.1
!
```

## Step 1: List Available Platforms

First, check which platforms are supported:

```bash
hier-config-cli list-platforms
```

Output:
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

## Step 2: Generate Remediation

Generate the commands needed to transform the running configuration into the intended configuration:

```bash
hier-config-cli remediation \
  --platform ios \
  --running-config running.conf \
  --generated-config intended.conf
```

Output:
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

## Step 3: Generate Rollback

Before applying changes, generate rollback commands for safety:

```bash
hier-config-cli rollback \
  --platform ios \
  --running-config running.conf \
  --generated-config intended.conf
```

Output:
```
=== Rollback Configuration ===
no hostname router-01-updated
hostname router-01
interface GigabitEthernet0/0
 no description WAN Interface - Updated
 description WAN Interface
no interface Vlan20
router ospf 1
 no network 10.0.20.0 0.0.0.255 area 0
no ntp server 192.0.2.1
```

## Step 4: Preview Future State

See what the complete configuration will look like after applying changes:

```bash
hier-config-cli future \
  --platform ios \
  --running-config running.conf \
  --generated-config intended.conf
```

Output:
```
=== Future Configuration ===
hostname router-01-updated
!
interface GigabitEthernet0/0
 description WAN Interface - Updated
 ip address 10.0.1.1 255.255.255.0
!
interface Vlan10
 description Management VLAN
 ip address 10.0.10.1 255.255.255.0
!
interface Vlan20
 description Guest VLAN
 ip address 10.0.20.1 255.255.255.0
!
router ospf 1
 network 10.0.1.0 0.0.0.255 area 0
 network 10.0.10.0 0.0.0.255 area 0
 network 10.0.20.0 0.0.0.255 area 0
!
ntp server 192.0.2.1
!
```

## Step 5: Save Output to File

Save remediation commands to a file for later use:

```bash
hier-config-cli remediation \
  --platform ios \
  --running-config running.conf \
  --generated-config intended.conf \
  --output remediation_commands.txt
```

Output:
```
Remediation configuration written to: remediation_commands.txt
```

## Step 6: Use Different Output Formats

### JSON Output

```bash
hier-config-cli remediation \
  --platform ios \
  --running-config running.conf \
  --generated-config intended.conf \
  --format json
```

### YAML Output

```bash
hier-config-cli remediation \
  --platform ios \
  --running-config running.conf \
  --generated-config intended.conf \
  --format yaml
```

## Step 7: Enable Verbose Logging

For troubleshooting or understanding what's happening:

```bash
# INFO level logging
hier-config-cli -v remediation \
  --platform ios \
  --running-config running.conf \
  --generated-config intended.conf

# DEBUG level logging
hier-config-cli -vv remediation \
  --platform ios \
  --running-config running.conf \
  --generated-config intended.conf
```

## Best Practices

1. **Always Generate Rollback First**: Before applying changes, always generate and save rollback commands
2. **Review Changes**: Manually review remediation commands before applying them
3. **Test in Lab**: Test configuration changes in a lab environment first
4. **Use Version Control**: Store your intended configurations in Git
5. **Document Changes**: Use the output files as documentation for change management

## Next Steps

- Learn about all available [Commands](commands.md)
- Explore [Supported Platforms](platforms.md)
- Check out [Integration Examples](integration/index.md)
- Read about [Output Formats](output-formats.md)

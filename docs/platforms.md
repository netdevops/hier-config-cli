# Supported Platforms

hier-config-cli supports multiple network device platforms through the underlying [Hier Config](https://github.com/netdevops/hier_config) library.

## Platform List

| Platform | Code | Vendor | Description |
|----------|------|--------|-------------|
| Cisco IOS | `ios` | Cisco | Cisco IOS routers and switches |
| Cisco NX-OS | `nxos` | Cisco | Cisco Nexus switches |
| Cisco IOS XR | `iosxr` | Cisco | Cisco IOS XR routers |
| Arista EOS | `eos` | Arista | Arista switches |
| Juniper JunOS | `junos` | Juniper | Juniper routers and switches |
| VyOS | `vyos` | VyOS | VyOS routers |
| Fortinet FortiOS | `fortios` | Fortinet | Fortinet firewalls (v3.4.0+) |
| HP Comware5 | `hp_comware5` | HP | HP Comware5 switches |
| HP ProCurve | `hp_procurve` | HP | HP ProCurve switches |
| Aruba AOS-CX | `aruba_aoscx` | Aruba | Aruba AOS-CX switches (hier-config v4+) |
| Huawei VRP | `huawei_vrp` | Huawei | Huawei VRP routers and switches (hier-config v4+) |
| Nokia SR Linux | `nokia_srl` | Nokia | Nokia SR Linux switches (hier-config v4+) |
| Generic | `generic` | N/A | Generic/unknown platform |

## Platform-Specific Details

### Cisco IOS (`ios`)

**Supported Devices:**
- Catalyst switches (2960, 3560, 3750, 4500, 6500, 9000 series)
- ISR routers (1900, 2900, 3900, 4000 series)
- ASR routers (1000 series running IOS)

**Configuration Format:**
- Hierarchical indentation
- Uses indentation to indicate parent-child relationships
- Commands like `interface`, `router`, `line` create context blocks

**Example:**
```bash
hier-config-cli remediation \
  --platform ios \
  --running-config cisco_ios_running.conf \
  --generated-config cisco_ios_intended.conf
```

---

### Cisco NX-OS (`nxos`)

**Supported Devices:**
- Nexus switches (3000, 5000, 6000, 7000, 9000 series)

**Configuration Format:**
- Similar to IOS but with NX-OS specific syntax
- Support for VDC (Virtual Device Context)
- Different command structures for some features

**Example:**
```bash
hier-config-cli remediation \
  --platform nxos \
  --running-config cisco_nxos_running.conf \
  --generated-config cisco_nxos_intended.conf
```

---

### Cisco IOS XR (`iosxr`)

**Supported Devices:**
- ASR 9000 series
- NCS (Network Convergence System) routers
- CRS (Carrier Routing System)

**Configuration Format:**
- Hierarchical with explicit ending (usually with `!`)
- Different syntax from IOS for some features

**Example:**
```bash
hier-config-cli remediation \
  --platform iosxr \
  --running-config cisco_iosxr_running.conf \
  --generated-config cisco_iosxr_intended.conf
```

---

### Arista EOS (`eos`)

**Supported Devices:**
- Arista switches (7000, 7500 series)
- Arista routers

**Configuration Format:**
- Similar to Cisco IOS
- Some Arista-specific commands and features

**Example:**
```bash
hier-config-cli remediation \
  --platform eos \
  --running-config arista_eos_running.conf \
  --generated-config arista_eos_intended.conf
```

---

### Juniper JunOS (`junos`)

**Supported Devices:**
- MX Series routers
- EX Series switches
- SRX Series firewalls
- QFX Series switches

**Configuration Format:**
- Hierarchical with curly braces `{}`
- Different syntax from Cisco-style platforms
- Set/delete command structure

**Example:**
```bash
hier-config-cli remediation \
  --platform junos \
  --running-config juniper_junos_running.conf \
  --generated-config juniper_junos_intended.conf
```

**Note:** JunOS configurations use a different text representation than Cisco-style platforms.

---

### VyOS (`vyos`)

**Supported Devices:**
- VyOS routers (open-source network OS)

**Configuration Format:**
- Hierarchical configuration
- Set/delete command structure

**Example:**
```bash
hier-config-cli remediation \
  --platform vyos \
  --running-config vyos_running.conf \
  --generated-config vyos_intended.conf
```

---

### Fortinet FortiOS (`fortios`)

**Supported Devices:**
- FortiGate firewalls

**Configuration Format:**
- Hierarchical configuration with specific FortiOS syntax
- Edit/set/next command structure

**Example:**
```bash
hier-config-cli remediation \
  --platform fortios \
  --running-config fortios_running.conf \
  --generated-config fortios_intended.conf
```

**Requirements:** Requires hier-config version 3.4.0 or higher.

---

### HP Comware5 (`hp_comware5`)

**Supported Devices:**
- HP switches running Comware5 OS

**Example:**
```bash
hier-config-cli remediation \
  --platform hp_comware5 \
  --running-config hp_comware5_running.conf \
  --generated-config hp_comware5_intended.conf
```

---

### HP ProCurve (`hp_procurve`)

**Supported Devices:**
- HP ProCurve switches

**Example:**
```bash
hier-config-cli remediation \
  --platform hp_procurve \
  --running-config hp_procurve_running.conf \
  --generated-config hp_procurve_intended.conf
```

---

### Aruba AOS-CX (`aruba_aoscx`)

**Supported Devices:**
- Aruba CX series switches

**Example:**
```bash
hier-config-cli remediation \
  --platform aruba_aoscx \
  --running-config aruba_aoscx_running.conf \
  --generated-config aruba_aoscx_intended.conf
```

**Requirements:** Requires hier-config version 4.0.0 or higher.

---

### Huawei VRP (`huawei_vrp`)

**Supported Devices:**
- Huawei routers and switches running VRP

**Example:**
```bash
hier-config-cli remediation \
  --platform huawei_vrp \
  --running-config huawei_vrp_running.conf \
  --generated-config huawei_vrp_intended.conf
```

**Requirements:** Requires hier-config version 4.0.0 or higher.

---

### Nokia SR Linux (`nokia_srl`)

**Supported Devices:**
- Nokia SR Linux data center switches

**Example:**
```bash
hier-config-cli remediation \
  --platform nokia_srl \
  --running-config nokia_srl_running.conf \
  --generated-config nokia_srl_intended.conf
```

**Requirements:** Requires hier-config version 4.0.0 or higher.

---

### Generic (`generic`)

**Use Case:**
- Unknown or unsupported platforms
- Custom network devices
- Basic hierarchical configuration parsing

**Example:**
```bash
hier-config-cli remediation \
  --platform generic \
  --running-config generic_running.conf \
  --generated-config generic_intended.conf
```

**Note:** Generic platform provides basic functionality but may not handle platform-specific syntax optimally.

## Checking Available Platforms

To see the current list of supported platforms in your installation:

```bash
hier-config-cli list-platforms
```

## Platform Selection Tips

1. **Use the specific platform** when available for best results
2. **Avoid using `generic`** unless absolutely necessary
3. **Check platform version compatibility** - some features may require specific versions
4. **Test in a lab environment** first when using a new platform

## Adding New Platforms

Platform support is provided by the underlying [Hier Config](https://github.com/netdevops/hier_config) library. To request a new platform:

1. Check the [Hier Config repository](https://github.com/netdevops/hier_config) for existing support
2. Open an issue in the [hier-config-cli repository](https://github.com/netdevops/hier-config-cli/issues)
3. Provide example configurations from the target platform

## Platform-Specific Considerations

### Configuration Retrieval

Different platforms have different commands for retrieving configurations:

| Platform | Command |
|----------|---------|
| Cisco IOS/NX-OS/EOS | `show running-config` |
| Cisco IOS XR | `show running-config` |
| Juniper JunOS | `show configuration \| display set` |
| VyOS | `show configuration` |
| Fortinet FortiOS | `show full-configuration` |

### Configuration Format

Ensure your configuration files:
- Are saved in plain text format
- Do not include prompts or timestamps
- Are complete (not truncated)
- Match the platform's native format

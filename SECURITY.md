# Security Policy

## Supported Versions

We release patches for security vulnerabilities in the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 0.2.x   | :white_check_mark: |
| 0.1.x   | :x:                |

## Reporting a Vulnerability

We take the security of hier-config-cli seriously. If you believe you have found a security vulnerability, please report it to us as described below.

### Please DO NOT:

- Open a public GitHub issue for security vulnerabilities
- Disclose the vulnerability publicly before it has been addressed

### Please DO:

**Report security vulnerabilities by emailing: james.williams@packetgeek.net**

Include the following information in your report:

1. **Description** of the vulnerability
2. **Steps to reproduce** the issue
3. **Potential impact** of the vulnerability
4. **Affected versions** (if known)
5. **Suggested fix** (if you have one)
6. **Your contact information** for follow-up questions

### What to Expect

- **Acknowledgment**: We will acknowledge receipt of your vulnerability report within 48 hours
- **Updates**: We will send you regular updates about our progress (at least every 5 business days)
- **Disclosure timeline**: We aim to address critical vulnerabilities within 30 days
- **Credit**: If you wish, we will credit you in the security advisory when the vulnerability is disclosed

## Security Best Practices

When using hier-config-cli, follow these security best practices:

### 1. Protect Configuration Files

Network device configurations often contain sensitive information:

- **Passwords and secrets**: Sanitize configs before sharing or storing in version control
- **IP addresses**: Be cautious about exposing internal network topology
- **Community strings**: Remove SNMP community strings from configs
- **Authentication keys**: Strip out authentication keys and certificates

Example of sanitizing a config:
```bash
# Before sharing, replace sensitive data
sed -i 's/enable secret .*/enable secret <REDACTED>/' config.txt
sed -i 's/username .* password .*/username admin password <REDACTED>/' config.txt
```

### 2. File Permissions

Ensure configuration files have appropriate permissions:

```bash
# Set restrictive permissions on config files
chmod 600 configs/*.conf

# Ensure output directory is protected
chmod 700 output/
```

### 3. Use Environment Variables

For automation workflows, avoid hardcoding paths or credentials:

```bash
# Good - use environment variables
export RUNNING_CONFIG_PATH=/secure/path/running.conf
hier-config-cli remediation --platform ios \
  --running-config "$RUNNING_CONFIG_PATH" \
  --generated-config "$GENERATED_CONFIG_PATH"

# Bad - hardcoded paths in scripts
hier-config-cli remediation --platform ios \
  --running-config /tmp/production-router.conf \
  --generated-config /tmp/new-config.conf
```

### 4. Validate Input Files

Always validate configuration files come from trusted sources:

```python
import hashlib

def verify_config_hash(filepath, expected_hash):
    """Verify configuration file integrity."""
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest() == expected_hash
```

### 5. Secure CI/CD Pipelines

When using hier-config-cli in CI/CD:

- Store configs in encrypted CI/CD secrets
- Use temporary files that are cleaned up after use
- Limit permissions of CI/CD service accounts
- Audit who has access to configuration files
- Enable branch protection rules

Example GitHub Actions security:
```yaml
jobs:
  config-check:
    runs-on: ubuntu-latest
    permissions:
      contents: read  # Minimal permissions
    steps:
      - uses: actions/checkout@v4

      - name: Process configs
        env:
          RUNNING_CONFIG: ${{ secrets.RUNNING_CONFIG }}
        run: |
          echo "$RUNNING_CONFIG" > /tmp/running.conf
          chmod 600 /tmp/running.conf

          hier-config-cli remediation \
            --platform ios \
            --running-config /tmp/running.conf \
            --generated-config configs/intended.conf

          # Clean up
          shred -vfz /tmp/running.conf
```

### 6. Output Handling

Be cautious with command output:

```bash
# Don't accidentally log sensitive configs
hier-config-cli remediation ... > remediation.txt
chmod 600 remediation.txt

# In production, consider encrypting output
hier-config-cli remediation ... | gpg -e -r admin@example.com > remediation.txt.gpg
```

## Known Security Considerations

### 1. Configuration Data Sensitivity

This tool processes network device configurations that may contain:
- Passwords and authentication credentials
- SNMP community strings
- Encryption keys
- Internal network topology
- Security policies

**Mitigation**: Always sanitize configurations before sharing or storing in version control.

### 2. File System Access

The tool requires read access to configuration files and write access for output files.

**Mitigation**: Run with least privilege necessary and use restrictive file permissions.

### 3. Dependency Security

We depend on third-party libraries (click, hier-config, pyyaml).

**Mitigation**:
- We regularly update dependencies
- Use `poetry` for dependency management with lock files
- Monitor for security advisories via GitHub Dependabot

### 4. Command Injection

The tool does not execute shell commands based on configuration content.

**Note**: When integrating with other tools, ensure proper input validation.

## Security Update Process

When a security vulnerability is confirmed:

1. We develop and test a fix
2. We prepare a security advisory
3. We release a patched version
4. We publish the security advisory
5. We notify users via GitHub security advisories

## Vulnerability Disclosure Policy

We follow coordinated vulnerability disclosure:

- **Private reporting period**: 90 days from initial report
- **Public disclosure**: After patch is released or 90 days, whichever comes first
- **Early disclosure**: May occur if vulnerability is being actively exploited

## Security Tools

We use the following tools to maintain security:

- **Dependabot**: Automated dependency updates
- **Safety**: Python dependency vulnerability scanning (can be added)
- **Bandit**: Python security linter (can be added)
- **CodeQL**: Static analysis via GitHub (can be enabled)

To run security checks locally:

```bash
# Install security tools
pip install safety bandit

# Check for known vulnerabilities in dependencies
safety check

# Run security linter
bandit -r src/

# Check for outdated dependencies
poetry show --outdated
```

## Contact

For security issues: james.williams@packetgeek.net

For general questions: [GitHub Issues](https://github.com/netdevops/hier-config-cli/issues)

---

Thank you for helping keep hier-config-cli and its users safe!

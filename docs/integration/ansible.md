# Ansible Integration

This guide shows how to integrate hier-config-cli with [Ansible](https://www.ansible.com/) for configuration management and network automation.

## Overview

Ansible is a powerful automation platform that excels at configuration management. By integrating hier-config-cli, you can:

- Generate precise remediation commands for network devices
- Validate configuration changes before deployment
- Create automated rollback procedures
- Implement configuration compliance checks

## Prerequisites

```bash
# Install Ansible and hier-config-cli
pip install ansible hier-config-cli

# For network device management
ansible-galaxy collection install ansible.netcommon
ansible-galaxy collection install cisco.ios
ansible-galaxy collection install cisco.nxos
```

## Basic Integration

### Simple Playbook

```yaml
---
- name: Generate Configuration Remediation
  hosts: network_devices
  gather_facts: false
  tasks:
    - name: Run hier-config-cli remediation
      command: >
        hier-config-cli remediation
        --platform {{ platform }}
        --running-config /tmp/{{ inventory_hostname }}_running.conf
        --generated-config /tmp/{{ inventory_hostname }}_intended.conf
        --output /tmp/{{ inventory_hostname }}_remediation.txt
      register: remediation_result
      changed_when: false

    - name: Display remediation output
      debug:
        msg: "{{ remediation_result.stdout }}"
```

### Inventory Setup

**inventory/hosts.ini:**
```ini
[routers]
router1 ansible_host=192.168.1.1 platform=ios
router2 ansible_host=192.168.1.2 platform=ios

[switches]
switch1 ansible_host=192.168.1.10 platform=nxos
switch2 ansible_host=192.168.1.11 platform=nxos

[firewalls]
firewall1 ansible_host=192.168.1.254 platform=fortios

[network_devices:children]
routers
switches
firewalls
```

## Complete Workflow Playbook

```yaml
---
- name: Network Configuration Management with Hier Config CLI
  hosts: network_devices
  gather_facts: false
  vars:
    config_dir: "./configs"
    running_config_dir: "{{ config_dir }}/running"
    intended_config_dir: "{{ config_dir }}/intended"
    remediation_dir: "{{ config_dir }}/remediation"
    rollback_dir: "{{ config_dir }}/rollback"

  tasks:
    - name: Create directory structure
      delegate_to: localhost
      run_once: true
      file:
        path: "{{ item }}"
        state: directory
      loop:
        - "{{ running_config_dir }}"
        - "{{ intended_config_dir }}"
        - "{{ remediation_dir }}"
        - "{{ rollback_dir }}"

    - name: Fetch running configuration
      cisco.ios.ios_command:
        commands:
          - show running-config
      register: running_config
      when: platform == "ios"

    - name: Save running configuration
      delegate_to: localhost
      copy:
        content: "{{ running_config.stdout[0] }}"
        dest: "{{ running_config_dir }}/{{ inventory_hostname }}.conf"
      when: running_config is defined

    - name: Generate remediation configuration
      delegate_to: localhost
      command: >
        hier-config-cli remediation
        --platform {{ platform }}
        --running-config {{ running_config_dir }}/{{ inventory_hostname }}.conf
        --generated-config {{ intended_config_dir }}/{{ inventory_hostname }}.conf
        --output {{ remediation_dir }}/{{ inventory_hostname }}.txt
      register: remediation_result
      changed_when: false

    - name: Generate rollback configuration
      delegate_to: localhost
      command: >
        hier-config-cli rollback
        --platform {{ platform }}
        --running-config {{ running_config_dir }}/{{ inventory_hostname }}.conf
        --generated-config {{ intended_config_dir }}/{{ inventory_hostname }}.conf
        --output {{ rollback_dir }}/{{ inventory_hostname }}.txt
      register: rollback_result
      changed_when: false

    - name: Read remediation commands
      delegate_to: localhost
      slurp:
        src: "{{ remediation_dir }}/{{ inventory_hostname }}.txt"
      register: remediation_content

    - name: Display remediation summary
      debug:
        msg: "Remediation for {{ inventory_hostname }} generated successfully"

    - name: Store remediation in variable
      set_fact:
        remediation_commands: "{{ remediation_content.content | b64decode }}"
```

## Custom Ansible Module

Create a custom module for cleaner integration:

**library/hier_config_cli.py:**
```python
#!/usr/bin/python
"""Ansible module for hier-config-cli."""

from ansible.module_utils.basic import AnsibleModule
import subprocess


def run_hier_config_cli(module):
    """Run hier-config-cli command."""

    operation = module.params['operation']
    platform = module.params['platform']
    running_config = module.params['running_config']
    generated_config = module.params['generated_config']
    output_file = module.params['output_file']
    output_format = module.params['output_format']

    cmd = [
        'hier-config-cli',
        operation,
        '--platform', platform,
        '--running-config', running_config,
        '--generated-config', generated_config,
        '--format', output_format,
    ]

    if output_file:
        cmd.extend(['--output', output_file])

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True,
        )

        return {
            'changed': True,
            'stdout': result.stdout,
            'stderr': result.stderr,
            'rc': result.returncode,
        }

    except subprocess.CalledProcessError as e:
        module.fail_json(
            msg=f"hier-config-cli failed: {e.stderr}",
            rc=e.returncode,
        )
    except FileNotFoundError:
        module.fail_json(msg="hier-config-cli not found. Is it installed?")


def main():
    """Main module function."""
    module = AnsibleModule(
        argument_spec={
            'operation': {
                'required': True,
                'type': 'str',
                'choices': ['remediation', 'rollback', 'future'],
            },
            'platform': {'required': True, 'type': 'str'},
            'running_config': {'required': True, 'type': 'path'},
            'generated_config': {'required': True, 'type': 'path'},
            'output_file': {'required': False, 'type': 'path'},
            'output_format': {
                'required': False,
                'type': 'str',
                'default': 'text',
                'choices': ['text', 'json', 'yaml'],
            },
        },
        supports_check_mode=False,
    )

    result = run_hier_config_cli(module)
    module.exit_json(**result)


if __name__ == '__main__':
    main()
```

**Using the custom module:**
```yaml
---
- name: Use custom hier-config-cli module
  hosts: network_devices
  tasks:
    - name: Generate remediation with custom module
      hier_config_cli:
        operation: remediation
        platform: "{{ platform }}"
        running_config: "/tmp/{{ inventory_hostname }}_running.conf"
        generated_config: "/tmp/{{ inventory_hostname }}_intended.conf"
        output_file: "/tmp/{{ inventory_hostname }}_remediation.txt"
        output_format: text
      register: result

    - name: Display result
      debug:
        var: result.stdout
```

## JSON Output Processing

```yaml
---
- name: Process JSON output
  hosts: network_devices
  tasks:
    - name: Generate remediation in JSON format
      command: >
        hier-config-cli remediation
        --platform {{ platform }}
        --running-config configs/running/{{ inventory_hostname }}.conf
        --generated-config configs/intended/{{ inventory_hostname }}.conf
        --format json
      register: remediation_json
      changed_when: false

    - name: Parse JSON output
      set_fact:
        remediation_data: "{{ remediation_json.stdout | from_json }}"

    - name: Display configuration commands
      debug:
        msg: "{{ remediation_data.config }}"

    - name: Count commands
      debug:
        msg: "Total commands: {{ remediation_data.config | length }}"

    - name: Filter specific commands
      debug:
        msg: "Interface commands: {{ remediation_data.config | select('match', '^interface') | list }}"
```

## Change Validation Workflow

```yaml
---
- name: Validate Configuration Changes
  hosts: network_devices
  gather_facts: false
  vars:
    max_changes: 50
    requires_approval: true

  tasks:
    - name: Generate remediation
      command: >
        hier-config-cli remediation
        --platform {{ platform }}
        --running-config configs/running/{{ inventory_hostname }}.conf
        --generated-config configs/intended/{{ inventory_hostname }}.conf
        --format json
      register: remediation_output
      delegate_to: localhost
      changed_when: false

    - name: Parse remediation
      set_fact:
        remediation: "{{ remediation_output.stdout | from_json }}"

    - name: Check number of changes
      fail:
        msg: "Too many changes ({{ remediation.config | length }}). Maximum allowed: {{ max_changes }}"
      when: remediation.config | length > max_changes

    - name: Display changes for review
      debug:
        msg: "{{ remediation.config }}"
      when: requires_approval

    - name: Pause for approval
      pause:
        prompt: "Review changes above. Press ENTER to continue or Ctrl+C to abort"
      when: requires_approval

    - name: Apply configuration
      # Your configuration application logic here
      debug:
        msg: "Would apply {{ remediation.config | length }} commands to {{ inventory_hostname }}"
```

## Rollback Workflow

```yaml
---
- name: Configuration Rollback Workflow
  hosts: network_devices
  gather_facts: false
  vars:
    rollback_required: false

  tasks:
    - name: Generate rollback configuration
      command: >
        hier-config-cli rollback
        --platform {{ platform }}
        --running-config configs/running/{{ inventory_hostname }}.conf
        --generated-config configs/intended/{{ inventory_hostname }}.conf
        --output configs/rollback/{{ inventory_hostname }}.txt
      delegate_to: localhost
      changed_when: false

    - name: Read rollback commands
      slurp:
        src: "configs/rollback/{{ inventory_hostname }}.txt"
      register: rollback_file
      delegate_to: localhost

    - name: Parse rollback commands
      set_fact:
        rollback_commands: "{{ rollback_file.content | b64decode }}"

    - name: Display rollback commands
      debug:
        msg: "{{ rollback_commands }}"
      when: rollback_required

    - name: Execute rollback
      # Your rollback execution logic here
      debug:
        msg: "Executing rollback for {{ inventory_hostname }}"
      when: rollback_required
```

## CI/CD Integration with Ansible

**Jenkinsfile:**
```groovy
pipeline {
    agent any

    stages {
        stage('Validate Configurations') {
            steps {
                sh '''
                    ansible-playbook \
                        -i inventory/hosts.ini \
                        playbooks/validate_configs.yml
                '''
            }
        }

        stage('Generate Remediation') {
            steps {
                sh '''
                    ansible-playbook \
                        -i inventory/hosts.ini \
                        playbooks/generate_remediation.yml
                '''
            }
        }

        stage('Review and Approve') {
            steps {
                input message: 'Review remediation and approve deployment?'
            }
        }

        stage('Deploy Changes') {
            steps {
                sh '''
                    ansible-playbook \
                        -i inventory/hosts.ini \
                        playbooks/deploy_changes.yml
                '''
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'configs/**/*.txt', allowEmptyArchive: true
        }
    }
}
```

## Best Practices

1. **Use delegation** (`delegate_to: localhost`) for hier-config-cli tasks
2. **Store configs in version control** for audit trails
3. **Implement approval gates** for production changes
4. **Generate rollback configs** before applying changes
5. **Use JSON format** for programmatic processing
6. **Set command limits** to prevent accidental large-scale changes
7. **Test in staging** before production deployment
8. **Keep playbooks idempotent** where possible

## Troubleshooting

### Command Not Found

```yaml
- name: Check hier-config-cli installation
  command: which hier-config-cli
  register: hier_config_path
  failed_when: hier_config_path.rc != 0
  changed_when: false
```

### File Permission Issues

```yaml
- name: Ensure config directories are writable
  file:
    path: "{{ item }}"
    state: directory
    mode: '0755'
  loop:
    - configs/running
    - configs/intended
    - configs/remediation
```

## Next Steps

- Explore [CI/CD Integration](cicd.md)
- Learn about [Nornir Integration](nornir.md)
- Review [Commands Reference](../commands.md)

# CI/CD Integration

Integrate hier-config-cli into your continuous integration and deployment pipelines to automate configuration validation, testing, and deployment.

## Overview

Using hier-config-cli in CI/CD pipelines enables:

- **Automated validation** of configuration changes
- **Pull request checks** to catch issues early
- **Automated remediation generation** for approved changes
- **Configuration drift detection** in production
- **Compliance checking** against golden configs

## GitHub Actions

### Basic Workflow

**.github/workflows/config-validation.yml:**
```yaml
name: Network Configuration Validation

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]
    paths:
      - 'configs/**'

jobs:
  validate-configs:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install hier-config-cli
        run: |
          pip install hier-config-cli

      - name: Validate configurations
        run: |
          for device in configs/intended/*.conf; do
            device_name=$(basename "$device" .conf)
            echo "Validating $device_name..."

            hier-config-cli remediation \
              --platform ios \
              --running-config "configs/running/${device_name}.conf" \
              --generated-config "$device" \
              --output "remediation/${device_name}.txt"
          done

      - name: Upload remediation artifacts
        uses: actions/upload-artifact@v4
        with:
          name: remediation-configs
          path: remediation/
```

### Advanced Workflow with Matrix

**.github/workflows/multi-platform-validation.yml:**
```yaml
name: Multi-Platform Configuration Validation

on:
  pull_request:
    branches: [main]

jobs:
  validate:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        platform: [ios, nxos, iosxr, eos]
      fail-fast: false

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          cache: 'pip'

      - name: Install dependencies
        run: |
          pip install hier-config-cli

      - name: Generate remediation for ${{ matrix.platform }}
        run: |
          mkdir -p output/remediation output/rollback

          for config in configs/intended/${{ matrix.platform }}/*.conf; do
            if [ -f "$config" ]; then
              device=$(basename "$config" .conf)

              echo "Processing $device (${{ matrix.platform }})"

              # Generate remediation
              hier-config-cli remediation \
                --platform ${{ matrix.platform }} \
                --running-config "configs/running/${{ matrix.platform }}/${device}.conf" \
                --generated-config "$config" \
                --output "output/remediation/${device}.txt"

              # Generate rollback
              hier-config-cli rollback \
                --platform ${{ matrix.platform }} \
                --running-config "configs/running/${{ matrix.platform }}/${device}.conf" \
                --generated-config "$config" \
                --output "output/rollback/${device}.txt"
            fi
          done

      - name: Check for excessive changes
        run: |
          for file in output/remediation/*.txt; do
            if [ -f "$file" ]; then
              lines=$(wc -l < "$file")
              if [ "$lines" -gt 100 ]; then
                echo "::error::Too many changes in $(basename "$file"): $lines lines"
                exit 1
              fi
            fi
          done

      - name: Upload artifacts
        uses: actions/upload-artifact@v4
        if: always()
        with:
          name: configs-${{ matrix.platform }}
          path: output/

      - name: Comment on PR
        uses: actions/github-script@v7
        if: github.event_name == 'pull_request'
        with:
          script: |
            const fs = require('fs');
            const files = fs.readdirSync('output/remediation');

            let comment = '## Configuration Validation Results - ${{ matrix.platform }}\n\n';
            comment += `Found ${files.length} devices to update\n\n`;

            for (const file of files) {
              const content = fs.readFileSync(`output/remediation/${file}`, 'utf8');
              const lines = content.split('\n').length;
              comment += `- **${file}**: ${lines} configuration lines\n`;
            }

            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: comment
            });
```

### Scheduled Compliance Check

**.github/workflows/compliance-check.yml:**
```yaml
name: Configuration Compliance Check

on:
  schedule:
    # Run every day at 2 AM UTC
    - cron: '0 2 * * *'
  workflow_dispatch:

jobs:
  compliance-check:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install hier-config-cli

      - name: Fetch running configs
        run: |
          # This would be replaced with actual config fetching logic
          # For example, using Ansible, NAPALM, or network APIs
          echo "Fetching configs from devices..."

      - name: Check for drift
        id: drift-check
        run: |
          mkdir -p drift-reports

          drift_detected=false

          for device in configs/golden/*.conf; do
            device_name=$(basename "$device" .conf)

            hier-config-cli remediation \
              --platform ios \
              --running-config "configs/running/${device_name}.conf" \
              --generated-config "$device" \
              --output "drift-reports/${device_name}.txt" \
              --format json

            if [ -s "drift-reports/${device_name}.txt" ]; then
              drift_detected=true
            fi
          done

          echo "drift_detected=$drift_detected" >> $GITHUB_OUTPUT

      - name: Create issue if drift detected
        if: steps.drift-check.outputs.drift_detected == 'true'
        uses: actions/github-script@v7
        with:
          script: |
            github.rest.issues.create({
              owner: context.repo.owner,
              repo: context.repo.repo,
              title: 'Configuration Drift Detected',
              body: 'Automated compliance check detected configuration drift. Please review the attached artifacts.',
              labels: ['configuration', 'drift', 'automated']
            });

      - name: Upload drift reports
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: drift-reports
          path: drift-reports/
```

## GitLab CI

**.gitlab-ci.yml:**
```yaml
stages:
  - validate
  - review
  - deploy

variables:
  PYTHON_VERSION: "3.11"

.install_deps: &install_deps
  before_script:
    - pip install hier-config-cli

validate:ios:
  stage: validate
  image: python:${PYTHON_VERSION}
  <<: *install_deps
  script:
    - mkdir -p output/remediation output/rollback
    - |
      for config in configs/intended/ios/*.conf; do
        device=$(basename "$config" .conf)
        echo "Validating $device..."

        hier-config-cli remediation \
          --platform ios \
          --running-config "configs/running/ios/${device}.conf" \
          --generated-config "$config" \
          --output "output/remediation/${device}.txt"

        hier-config-cli rollback \
          --platform ios \
          --running-config "configs/running/ios/${device}.conf" \
          --generated-config "$config" \
          --output "output/rollback/${device}.txt"
      done
  artifacts:
    paths:
      - output/
    expire_in: 1 week
  only:
    changes:
      - configs/**

validate:nxos:
  stage: validate
  image: python:${PYTHON_VERSION}
  <<: *install_deps
  script:
    - mkdir -p output/remediation output/rollback
    - |
      for config in configs/intended/nxos/*.conf; do
        device=$(basename "$config" .conf)
        echo "Validating $device..."

        hier-config-cli remediation \
          --platform nxos \
          --running-config "configs/running/nxos/${device}.conf" \
          --generated-config "$config" \
          --output "output/remediation/${device}.txt"
      done
  artifacts:
    paths:
      - output/
    expire_in: 1 week
  only:
    changes:
      - configs/**

review_changes:
  stage: review
  image: python:${PYTHON_VERSION}
  script:
    - |
      echo "## Configuration Changes Summary" > review.md
      echo "" >> review.md

      for file in output/remediation/*.txt; do
        if [ -f "$file" ]; then
          device=$(basename "$file" .txt)
          lines=$(wc -l < "$file")
          echo "- **$device**: $lines configuration lines" >> review.md
        fi
      done

      cat review.md
  artifacts:
    reports:
      dotenv: review.md
  dependencies:
    - validate:ios
    - validate:nxos
  only:
    - merge_requests

deploy_configs:
  stage: deploy
  image: python:${PYTHON_VERSION}
  script:
    - echo "Deploying configurations..."
    # Add deployment logic here
  when: manual
  only:
    - main
  dependencies:
    - validate:ios
    - validate:nxos
```

## Jenkins

**Jenkinsfile:**
```groovy
pipeline {
    agent {
        docker {
            image 'python:3.11'
        }
    }

    parameters {
        choice(
            name: 'PLATFORM',
            choices: ['ios', 'nxos', 'iosxr', 'eos'],
            description: 'Network platform to validate'
        )
        booleanParam(
            name: 'GENERATE_ROLLBACK',
            defaultValue: true,
            description: 'Generate rollback configurations'
        )
    }

    stages {
        stage('Setup') {
            steps {
                sh 'pip install hier-config-cli'
            }
        }

        stage('Validate Configurations') {
            steps {
                script {
                    sh '''
                        mkdir -p output/remediation output/rollback

                        for config in configs/intended/${PLATFORM}/*.conf; do
                            device=$(basename "$config" .conf)
                            echo "Validating $device..."

                            hier-config-cli remediation \
                                --platform ${PLATFORM} \
                                --running-config "configs/running/${PLATFORM}/${device}.conf" \
                                --generated-config "$config" \
                                --output "output/remediation/${device}.txt"

                            if [ "${GENERATE_ROLLBACK}" = "true" ]; then
                                hier-config-cli rollback \
                                    --platform ${PLATFORM} \
                                    --running-config "configs/running/${PLATFORM}/${device}.conf" \
                                    --generated-config "$config" \
                                    --output "output/rollback/${device}.txt"
                            fi
                        done
                    '''
                }
            }
        }

        stage('Quality Gates') {
            steps {
                script {
                    sh '''
                        # Check for excessive changes
                        for file in output/remediation/*.txt; do
                            if [ -f "$file" ]; then
                                lines=$(wc -l < "$file")
                                if [ "$lines" -gt 100 ]; then
                                    echo "ERROR: Too many changes in $(basename "$file"): $lines lines"
                                    exit 1
                                fi
                            fi
                        done
                    '''
                }
            }
        }

        stage('Generate Report') {
            steps {
                script {
                    sh '''
                        echo "# Configuration Validation Report" > report.md
                        echo "" >> report.md
                        echo "Platform: ${PLATFORM}" >> report.md
                        echo "Date: $(date)" >> report.md
                        echo "" >> report.md
                        echo "## Devices Processed" >> report.md
                        echo "" >> report.md

                        for file in output/remediation/*.txt; do
                            if [ -f "$file" ]; then
                                device=$(basename "$file" .txt)
                                lines=$(wc -l < "$file")
                                echo "- **$device**: $lines configuration lines" >> report.md
                            fi
                        done
                    '''
                }
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'output/**/*.txt', allowEmptyArchive: true
            archiveArtifacts artifacts: 'report.md', allowEmptyArchive: true
        }
        success {
            echo 'Configuration validation successful!'
        }
        failure {
            echo 'Configuration validation failed!'
        }
    }
}
```

## Azure DevOps

**azure-pipelines.yml:**
```yaml
trigger:
  branches:
    include:
      - main
      - develop
  paths:
    include:
      - configs/**

pool:
  vmImage: 'ubuntu-latest'

variables:
  pythonVersion: '3.11'

stages:
  - stage: Validate
    displayName: 'Validate Configurations'
    jobs:
      - job: ValidateIOS
        displayName: 'Validate Cisco IOS Configs'
        steps:
          - task: UsePythonVersion@0
            inputs:
              versionSpec: '$(pythonVersion)'

          - script: |
              pip install hier-config-cli
            displayName: 'Install hier-config-cli'

          - script: |
              mkdir -p output/remediation output/rollback

              for config in configs/intended/ios/*.conf; do
                device=$(basename "$config" .conf)
                echo "Processing $device..."

                hier-config-cli remediation \
                  --platform ios \
                  --running-config "configs/running/ios/${device}.conf" \
                  --generated-config "$config" \
                  --output "output/remediation/${device}.txt"
              done
            displayName: 'Generate Remediation'

          - task: PublishBuildArtifacts@1
            inputs:
              pathToPublish: 'output'
              artifactName: 'configurations'

      - job: ValidateNXOS
        displayName: 'Validate Cisco NX-OS Configs'
        steps:
          - task: UsePythonVersion@0
            inputs:
              versionSpec: '$(pythonVersion)'

          - script: |
              pip install hier-config-cli
            displayName: 'Install hier-config-cli'

          - script: |
              mkdir -p output/remediation

              for config in configs/intended/nxos/*.conf; do
                device=$(basename "$config" .conf)

                hier-config-cli remediation \
                  --platform nxos \
                  --running-config "configs/running/nxos/${device}.conf" \
                  --generated-config "$config" \
                  --output "output/remediation/${device}.txt"
              done
            displayName: 'Generate Remediation'

  - stage: Deploy
    displayName: 'Deploy Configurations'
    dependsOn: Validate
    condition: and(succeeded(), eq(variables['Build.SourceBranch'], 'refs/heads/main'))
    jobs:
      - deployment: DeployConfigs
        displayName: 'Deploy to Production'
        environment: 'production'
        strategy:
          runOnce:
            deploy:
              steps:
                - script: |
                    echo "Deploying configurations..."
                    # Add deployment logic here
                  displayName: 'Deploy'
```

## Best Practices

1. **Run validation on every PR** to catch issues early
2. **Use matrix builds** for multi-platform environments
3. **Set change thresholds** to prevent accidental large deployments
4. **Generate rollback configs** automatically
5. **Archive artifacts** for audit trails
6. **Use approval gates** for production deployments
7. **Implement drift detection** with scheduled jobs
8. **Add status badges** to README for visibility

## Example Status Badges

Add to your README.md:

```markdown
![Config Validation](https://github.com/yourorg/yourrepo/workflows/config-validation/badge.svg)
```

## Next Steps

- Learn about [Nornir Integration](nornir.md)
- Explore [Ansible Integration](ansible.md)
- Review [Commands Reference](../commands.md)

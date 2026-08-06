# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Added support for the Aruba AOS-CX (`aruba_aoscx`), Huawei VRP (`huawei_vrp`),
  and Nokia SR Linux (`nokia_srl`) platforms introduced in hier-config v4

### Changed
- Migrated to hier-config 4.0.0b1: `get_hconfig()` replaced with
  `HConfig.from_text()` and `cisco_style_text()` replaced with `indented_text()`
- Pinned `hier-config` to `>=4.0.0b1,<5.0` (pre-releases allowed)

## [0.2.0] - 2026-01-25

### Added
- Added support for Fortinet FortiOS platform
- Added `--format` option to output results in JSON, YAML, or text formats
- Added `--output` / `-o` flag to save output to file
- Added `list-platforms` command to show all available platforms
- Added `version` command to display tool version
- Added comprehensive error handling for file operations and platform validation
- Added verbose logging support with `-v` (INFO) and `-vv` (DEBUG) flags
- Added complete type hints throughout codebase
- Added comprehensive test suite with 20+ test cases including:
  - Error handling tests
  - All platform tests
  - Output format tests (text, JSON, YAML)
  - File output tests
  - Verbose logging tests
- Added comprehensive documentation:
  - Detailed README with installation instructions and examples
  - CONTRIBUTING.md with development guidelines
  - SECURITY.md with security policy
  - Examples directory with sample configurations
  - Integration examples for Nornir, Ansible, and CI/CD
- Added development tools configuration:
  - Black formatter configuration
  - Ruff linter configuration
  - Mypy type checker configuration
  - Pytest with coverage reporting
- Added `py.typed` marker file for PEP 561 compliance

### Changed
- **BREAKING**: Converted to proper Python package structure with `__init__.py`
- **BREAKING**: Entry point now uses `hier_config_cli:cli` instead of module path
- Refactored duplicate code in commands into shared `process_configs()` function
- Fixed platform-specific output formatting (no longer hardcodes `cisco_style_text()` for all platforms)
- Improved command help text with detailed descriptions and examples
- Enhanced pyproject.toml with comprehensive metadata and classifiers
- Updated Python version support to 3.9-3.13
- Improved error messages to be more descriptive and actionable

### Fixed
- Fixed incorrect output format for Juniper JunOS configurations
- Fixed missing platform support for Fortinet FortiOS
- Fixed lack of error handling for missing or unreadable configuration files
- Fixed unused PyYAML dependency (now actively used for YAML output)

### Removed
- Removed code duplication across remediation, rollback, and future commands

## [0.1.0] - 2024-12-XX

### Added
- Initial release
- Basic remediation, rollback, and future commands
- Support for major network platforms:
  - Cisco IOS
  - Cisco NX-OS
  - Cisco IOS XR
  - Arista EOS
  - Juniper JunOS
  - VyOS
  - HP Comware5
  - HP ProCurve
  - Generic platform
- GitHub Actions CI/CD pipeline
- Basic test coverage
- Apache 2.0 license

[Unreleased]: https://github.com/netdevops/hier-config-cli/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/netdevops/hier-config-cli/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/netdevops/hier-config-cli/releases/tag/v0.1.0

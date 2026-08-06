# Changelog

All notable changes to hier-config-cli will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Comprehensive documentation site with MkDocs
- Detailed integration guides for Nornir, Ansible, and CI/CD
- Development guides for contributing, testing, and code quality
- Support for the Aruba AOS-CX (`aruba_aoscx`), Huawei VRP (`huawei_vrp`),
  and Nokia SR Linux (`nokia_srl`) platforms introduced in hier-config v4

### Changed
- Migrated to hier-config 4.0.0b1: `get_hconfig()` replaced with
  `HConfig.from_text()` and `cisco_style_text()` replaced with `indented_text()`
- Pinned `hier-config` to `>=4.0.0b1,<5.0` (pre-releases allowed)

## [0.2.0] - 2024-01-XX

### Added
- Support for FortiOS platform (requires hier-config 3.4.0+)
- Python 3.13 support
- Modern type annotations using Python 3.10+ syntax

### Changed
- Upgraded to hier-config 3.4.0
- Improved type checking with mypy
- Enhanced code quality with ruff linting
- Applied Python 3.10+ type annotation style

### Fixed
- Resolved mypy type checking errors
- Fixed ruff linting issues including exception chaining
- Improved code documentation and type hints

## [0.1.0] - 2024-01-XX

### Added
- Initial release of hier-config-cli
- Core commands: `remediation`, `rollback`, `future`, `list-platforms`, `version`
- Support for multiple platforms: ios, nxos, iosxr, eos, junos, vyos, hp_comware5, hp_procurve, generic
- Multiple output formats: text, json, yaml
- Verbose and debug logging modes
- Comprehensive test suite with pytest
- Type safety with mypy
- Code formatting with black
- Linting with ruff
- CI/CD integration with GitHub Actions

### Platform Support
- Cisco IOS
- Cisco NX-OS
- Cisco IOS XR
- Arista EOS
- Juniper JunOS
- VyOS
- HP Comware5
- HP ProCurve
- Generic platform

### Dependencies
- hier-config ^3.3.0
- click ^8.1.7
- pyyaml ^6.0.2
- Python ^3.10

## Release Process

### Version Numbering

We follow [Semantic Versioning](https://semver.org/):

- **MAJOR** version for incompatible API changes
- **MINOR** version for new functionality in a backwards compatible manner
- **PATCH** version for backwards compatible bug fixes

### Release Checklist

For maintainers releasing a new version:

1. Update version in `pyproject.toml`
2. Update version in `src/hier_config_cli/__main__.py`
3. Update `CHANGELOG.md` with release notes
4. Commit changes: `git commit -m "Release v0.x.x"`
5. Create git tag: `git tag v0.x.x`
6. Push changes: `git push origin main --tags`
7. GitHub Actions will automatically publish to PyPI

## Upgrade Guide

### Upgrading from 0.1.x to 0.2.x

No breaking changes. Simply upgrade:

```bash
pip install --upgrade hier-config-cli
```

### Upgrading Dependencies

If you're using hier-config-cli in your project:

```toml
# pyproject.toml
[tool.poetry.dependencies]
hier-config-cli = "^0.2.0"
```

## Deprecation Policy

- Features marked as deprecated will be removed in the next major version
- Deprecation warnings will be issued for at least one minor version before removal
- Deprecated features will be documented in the changelog

## Future Plans

### Planned Features

- Configuration templates support
- Batch processing improvements
- Interactive mode
- Configuration validation rules
- Compliance reporting
- More platform support

### Under Consideration

- Plugin system for custom platforms
- Web UI for configuration management
- REST API server mode
- Configuration backup/restore
- Diff visualization

## Community Contributions

We welcome contributions! See [Contributing Guide](development/contributing.md) for details.

### Contributors

Thank you to all contributors who have helped improve hier-config-cli!

- James Williams (@networktocode) - Creator and maintainer

## Security Updates

Security vulnerabilities are taken seriously. See [Security Policy](https://github.com/netdevops/hier-config-cli/security/policy) for reporting procedures.

## Links

- **GitHub Repository**: [netdevops/hier-config-cli](https://github.com/netdevops/hier-config-cli)
- **PyPI Package**: [hier-config-cli](https://pypi.org/project/hier-config-cli/)
- **Documentation**: [hier-config-cli.readthedocs.io](https://hier-config-cli.readthedocs.io/)
- **Issue Tracker**: [GitHub Issues](https://github.com/netdevops/hier-config-cli/issues)
- **Discussions**: [GitHub Discussions](https://github.com/netdevops/hier-config-cli/discussions)

[Unreleased]: https://github.com/netdevops/hier-config-cli/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/netdevops/hier-config-cli/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/netdevops/hier-config-cli/releases/tag/v0.1.0

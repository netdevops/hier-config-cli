"""Hier Config CLI Tool - A command-line interface for network configuration analysis."""

import json
import logging
import sys
from collections.abc import Callable
from pathlib import Path
from typing import TypeVar

import click
import yaml
from hier_config import HConfig, Platform, WorkflowRemediation
from hier_config.utils import read_text_from_file

_CliCommand = TypeVar("_CliCommand", bound=Callable[..., None])

__version__ = "0.2.1a0"

# Mapping for driver platforms - includes all hier-config supported platforms
PLATFORM_MAP = {
    "ios": Platform.CISCO_IOS,
    "nxos": Platform.CISCO_NXOS,
    "iosxr": Platform.CISCO_XR,
    "eos": Platform.ARISTA_EOS,
    "junos": Platform.JUNIPER_JUNOS,
    "vyos": Platform.VYOS,
    "fortios": Platform.FORTINET_FORTIOS,
    "generic": Platform.GENERIC,
    "hp_comware5": Platform.HP_COMWARE5,
    "hp_procurve": Platform.HP_PROCURVE,
    "aruba_aoscx": Platform.ARUBA_AOSCX,
    "huawei_vrp": Platform.HUAWEI_VRP,
    "nokia_srl": Platform.NOKIA_SRL,
}

logger = logging.getLogger(__name__)


def setup_logging(verbose: int) -> None:
    """Configure logging based on verbosity level.

    Args:
        verbose: Verbosity level (0=WARNING, 1=INFO, 2=DEBUG)

    """
    level = logging.WARNING
    if verbose == 1:
        level = logging.INFO
    elif verbose >= 2:
        level = logging.DEBUG

    logging.basicConfig(
        level=level,
        format="%(levelname)s: %(message)s",
        stream=sys.stderr,
    )


def get_output_text(hconfig: HConfig, platform: Platform) -> str:
    """Get text output from HConfig based on platform.

    Args:
        hconfig: The hierarchical configuration object
        platform: The platform type

    Returns:
        Formatted configuration text appropriate for the platform

    """
    if platform is Platform.JUNIPER_JUNOS:
        # Juniper uses curly braces and different syntax
        return "\n".join(line.text for line in hconfig.all_children_sorted())
    # Cisco-style platforms (IOS, NXOS, XR, EOS, etc.)
    return "\n".join(line.indented_text() for line in hconfig.all_children_sorted())


def format_output(hconfig: HConfig, platform: Platform, output_format: str) -> str:
    """Format configuration output in the requested format.

    Args:
        hconfig: The hierarchical configuration object
        platform: The platform type
        output_format: Output format (text, json, yaml)

    Returns:
        Formatted output string

    Raises:
        ValueError: If output format is not supported

    """
    text = get_output_text(hconfig, platform)
    if output_format == "text":
        return text
    if output_format == "json":
        return json.dumps({"config": text.split("\n")}, indent=2)
    if output_format == "yaml":
        return yaml.dump({"config": text.split("\n")}, default_flow_style=False)
    message = f"Unsupported output format: {output_format}"
    raise ValueError(message)


def _resolve_platform(platform_str: str) -> Platform:
    """Resolve a platform name string to a Platform enum member."""
    try:
        return PLATFORM_MAP[platform_str.lower()]
    except KeyError:
        message = (
            f"Unknown platform: {platform_str}. "
            f"Use 'list-platforms' to see available platforms."
        )
        raise click.ClickException(message) from None


def _read_config(path: str, description: str) -> str:
    """Read a configuration file, converting failures to clean CLI errors."""
    logger.info("Reading %s from: %s", description, path)
    try:
        return read_text_from_file(path)
    except FileNotFoundError:
        message = f"{description.capitalize()} file not found: {path}"
        raise click.ClickException(message) from None
    except PermissionError:
        message = f"Permission denied reading {description}: {path}"
        raise click.ClickException(message) from None
    except (OSError, ValueError) as exc:
        message = f"Error reading {description}: {exc}"
        raise click.ClickException(message) from exc


def _parse_config(platform: Platform, config_text: str) -> HConfig:
    """Parse configuration text, converting failures to clean CLI errors."""
    try:
        return HConfig.from_text(platform, config_text)
    except Exception as exc:
        message = f"Error parsing configuration: {exc}"
        raise click.ClickException(message) from exc


def _run_operation(operation: str, running: HConfig, generated: HConfig) -> HConfig:
    """Run the requested config operation and return the resulting HConfig."""
    if operation == "future":
        return running.future(generated)
    workflow = WorkflowRemediation(running, generated)
    if operation == "remediation":
        return workflow.remediation_config
    return workflow.rollback_config


def _generate_config(
    operation: str,
    running: HConfig,
    generated: HConfig,
) -> HConfig:
    """Generate the requested config, converting failures to clean CLI errors."""
    logger.info("Generating %s configuration", operation)
    try:
        return _run_operation(operation, running, generated)
    except Exception as exc:
        message = f"Error generating {operation}: {exc}"
        raise click.ClickException(message) from exc


def process_configs(
    platform_str: str,
    running_config_path: str,
    generated_config_path: str,
    operation: str,
) -> tuple[HConfig, Platform]:
    """Process configuration files and return the result.

    Args:
        platform_str: Platform name string
        running_config_path: Path to running configuration
        generated_config_path: Path to generated configuration
        operation: Operation type (remediation, rollback, future)

    Returns:
        Tuple of (result HConfig, Platform enum)

    """
    platform_enum = _resolve_platform(platform_str)
    logger.info("Using platform: %s", platform_str)

    running_config_text = _read_config(running_config_path, "running config")
    generated_config_text = _read_config(generated_config_path, "generated config")

    logger.info("Parsing configurations")
    running_hconfig = _parse_config(platform_enum, running_config_text)
    generated_hconfig = _parse_config(platform_enum, generated_config_text)

    result = _generate_config(operation, running_hconfig, generated_hconfig)
    return result, platform_enum


@click.group()
@click.option(
    "-v",
    "--verbose",
    count=True,
    help="Increase verbosity (use -v for INFO, -vv for DEBUG)",
)
@click.pass_context
def cli(ctx: click.Context, verbose: int) -> None:
    """Hier Config CLI Tool - Network configuration analysis and remediation.

    This tool provides commands to analyze network device configurations,
    generate remediation steps, rollback configurations, and predict future states.
    """
    ctx.ensure_object(dict)
    ctx.obj["verbose"] = verbose
    setup_logging(verbose)


def common_options(func: _CliCommand) -> _CliCommand:
    """Reusable options for platform, running config, and generated config."""
    func = click.option(
        "--platform",
        type=click.Choice(list(PLATFORM_MAP), case_sensitive=False),
        required=True,
        help=(
            "Platform driver to use "
            "(e.g., ios, nxos, iosxr, eos, junos, vyos, fortios, generic)."
        ),
    )(func)
    func = click.option(
        "--running-config",
        type=click.Path(exists=True, readable=True),
        required=True,
        help="Path to the running configuration file.",
    )(func)
    func = click.option(
        "--generated-config",
        type=click.Path(exists=True, readable=True),
        required=True,
        help="Path to the generated (intended) configuration file.",
    )(func)
    func = click.option(
        "--format",
        "output_format",
        type=click.Choice(["text", "json", "yaml"], case_sensitive=False),
        default="text",
        help="Output format (default: text).",
    )(func)
    return click.option(
        "--output",
        "-o",
        "output_file",
        type=click.Path(),
        default=None,
        help="Write output to file instead of stdout.",
    )(func)


def _format_or_fail(result: HConfig, platform: Platform, output_format: str) -> str:
    """Format the result, converting formatting failures to clean CLI errors."""
    try:
        return format_output(result, platform, output_format)
    except ValueError as exc:
        raise click.ClickException(str(exc)) from exc


def _emit_output(output: str, output_file: str | None, title: str) -> None:
    """Write the output to a file, or echo it to stdout with a title banner."""
    if output_file:
        try:
            Path(output_file).write_text(output, encoding="utf-8")
        except OSError as exc:
            message = f"Error writing output file: {exc}"
            raise click.ClickException(message) from exc
        click.echo(f"{title} written to: {output_file}", err=True)
    else:
        click.echo(f"\n=== {title} ===")
        click.echo(output)


@cli.command()
@common_options
def remediation(
    platform: str,
    running_config: str,
    generated_config: str,
    output_format: str,
    output_file: str | None,
) -> None:
    r"""Generate the remediation configuration.

    Compares the running configuration with the generated (intended) configuration
    and produces the commands needed to transform the running config into the
    generated config.

    Example:
        hier-config-cli remediation --platform ios \
            --running-config running.conf --generated-config intended.conf

    """
    result, platform_enum = process_configs(
        platform,
        running_config,
        generated_config,
        "remediation",
    )
    output = _format_or_fail(result, platform_enum, output_format)
    _emit_output(output, output_file, "Remediation Configuration")


@cli.command()
@common_options
def rollback(
    platform: str,
    running_config: str,
    generated_config: str,
    output_format: str,
    output_file: str | None,
) -> None:
    r"""Generate the rollback configuration.

    Produces the commands needed to revert from the generated configuration
    back to the running configuration. This is useful for preparing rollback
    procedures before making changes.

    Example:
        hier-config-cli rollback --platform ios \
            --running-config running.conf --generated-config intended.conf

    """
    result, platform_enum = process_configs(
        platform,
        running_config,
        generated_config,
        "rollback",
    )
    output = _format_or_fail(result, platform_enum, output_format)
    _emit_output(output, output_file, "Rollback Configuration")


@cli.command()
@common_options
def future(
    platform: str,
    running_config: str,
    generated_config: str,
    output_format: str,
    output_file: str | None,
) -> None:
    r"""Generate the future configuration.

    Predicts what the complete configuration will look like after applying
    the generated configuration to the running configuration.

    Example:
        hier-config-cli future --platform ios \
            --running-config running.conf --generated-config intended.conf

    """
    result, platform_enum = process_configs(
        platform,
        running_config,
        generated_config,
        "future",
    )
    output = _format_or_fail(result, platform_enum, output_format)
    _emit_output(output, output_file, "Future Configuration")


@cli.command()
def list_platforms() -> None:
    """List all available platforms.

    Shows all supported network device platforms that can be used
    with the --platform option.
    """
    click.echo("\n=== Available Platforms ===")
    for platform in sorted(PLATFORM_MAP):
        click.echo(f"  {platform}")
    click.echo()


@cli.command()
def version() -> None:
    """Show the version and exit."""
    click.echo(f"hier-config-cli version {__version__}")


if __name__ == "__main__":  # pragma: no cover - process-entry glue
    # click injects the group's arguments at invocation time.
    cli()  # pylint: disable=no-value-for-parameter

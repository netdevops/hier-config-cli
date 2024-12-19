import click
from hier_config import WorkflowRemediation, get_hconfig, Platform
from hier_config.utils import read_text_from_file

# Mapping for driver platforms
PLATFORM_MAP = {
    "ios": Platform.CISCO_IOS,
    "nxos": Platform.CISCO_NXOS,
    "iosxr": Platform.CISCO_XR,
    "eos": Platform.ARISTA_EOS,
    "junos": Platform.JUNIPER_JUNOS,
    "vyos": Platform.VYOS,
    "generic": Platform.GENERIC,
    "hp_comware5": Platform.HP_COMWARE5,
    "hp_procurve": Platform.HP_PROCURVE,
}


@click.group()
def cli():
    """Hier Config CLI Tool"""
    pass


def common_options(func):
    """Reusable options for platform, running config, and generated config."""
    func = click.option(
        "--platform",
        type=click.Choice(PLATFORM_MAP.keys(), case_sensitive=False),
        required=True,
        help="Platform driver to use (e.g., ios, nxos, iosxr, eos, junos, vyos, generic).",
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
    return func


@cli.command()
@common_options
def remediation(platform, running_config, generated_config):
    """
    Generate the remediation configuration.
    """
    platform_enum = PLATFORM_MAP[platform.lower()]
    running_config_text = read_text_from_file(running_config)
    generated_config_text = read_text_from_file(generated_config)

    running_hconfig = get_hconfig(platform_enum, running_config_text)
    generated_hconfig = get_hconfig(platform_enum, generated_config_text)

    workflow = WorkflowRemediation(running_hconfig, generated_hconfig)

    click.echo("\n=== Remediation Configuration ===")
    for line in workflow.remediation_config.all_children_sorted():
        click.echo(line.cisco_style_text())


@cli.command()
@common_options
def rollback(platform, running_config, generated_config):
    """
    Generate the rollback configuration.
    """
    platform_enum = PLATFORM_MAP[platform.lower()]
    running_config_text = read_text_from_file(running_config)
    generated_config_text = read_text_from_file(generated_config)

    running_hconfig = get_hconfig(platform_enum, running_config_text)
    generated_hconfig = get_hconfig(platform_enum, generated_config_text)

    workflow = WorkflowRemediation(running_hconfig, generated_hconfig)

    click.echo("\n=== Rollback Configuration ===")
    for line in workflow.rollback_config.all_children_sorted():
        click.echo(line.cisco_style_text())


@cli.command()
@common_options
def future(platform, running_config, generated_config):
    """
    Generate the future configuration.
    """
    platform_enum = PLATFORM_MAP[platform.lower()]
    running_config_text = read_text_from_file(running_config)
    generated_config_text = read_text_from_file(generated_config)

    running_hconfig = get_hconfig(platform_enum, running_config_text)
    generated_hconfig = get_hconfig(platform_enum, generated_config_text)

    future_config = running_hconfig.future(generated_hconfig)

    click.echo("\n=== Future Configuration ===")
    for line in future_config.all_children_sorted():
        click.echo(line.cisco_style_text())


@cli.command()
def list_platforms():
    """
    List all available platforms.
    """
    click.echo("\n=== Available Platforms ===")
    for platform in PLATFORM_MAP.keys():
        click.echo(f"- {platform}")


if __name__ == "__main__":
    cli()

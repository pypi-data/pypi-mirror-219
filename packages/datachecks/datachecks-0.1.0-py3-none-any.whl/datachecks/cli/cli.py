import click
from ..__version__ import __version__


@click.version_option(package_name="datachecks", prog_name="datachecks")
@click.group(help=f"Datachecks CLI version {__version__}")
def main():
    pass


@main.command(
    short_help="Runs a scan",
)
def metrics():
    print("====")

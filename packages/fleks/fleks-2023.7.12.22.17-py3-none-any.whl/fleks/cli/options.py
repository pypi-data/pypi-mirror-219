""" fleks.cli.options:

    Common options for CLI
"""
from fleks.cli import click
from fleks.util import lme

LOGGER = lme.get_logger(__name__)

strict = click.flag(
    "--strict",
    help=("if true, runs in strict mode"),
)
script = click.option("--script", default=None, help=("script to use"))
file = click.option("--file", "-f", default="", help=("file to read as input"))
stdout = click.flag("--stdout", help=("whether to write to stdout."))
name = click.option("--name", default="", help=("name to use"))

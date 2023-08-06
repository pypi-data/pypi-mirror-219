"""
Generate command

Produce the require output files for a given YAML file
"""
import logging
import os
from typing import Optional

import click

from fgen.commands.base import cli
from fgen.schema import load_module_definition
from fgen.templator import process_module

logger = logging.getLogger(__name__)


@cli.command(name="generate")
@click.option(
    "-f",
    "--force",
    is_flag=True,
    help="Override any existing files",
)
@click.option(
    "--manager-directory",
    help="""Directory to write the calculator lifecycle manager (Fortran-based).
    This defaults to the same directory as FILENAME which is generally where the
    Fortran code for the calculator is also located.""",
    type=click.Path(exists=True, dir_okay=True, file_okay=False),
)
@click.option(
    "--wrapper-directory",
    help="Directory to write the Python-Fortran wrapper.",
    type=click.Path(exists=True, dir_okay=True, file_okay=False),
    required=True,
)
@click.option(
    "--python-directory",
    help="""Directory to write the python module. This is typically in the magiccly package""",
    type=click.Path(exists=True, dir_okay=True, file_okay=False),
    required=True,
)
@click.option(
    "--extension",
    "-e",
    help="""Name of the Python extension package""",
    required=True,
)
@click.argument(
    "filename",
    type=click.Path(exists=True, dir_okay=False, file_okay=True),
)
def generate_command(  # noqa: PLR0913
    force: bool,
    manager_directory: Optional[str],
    wrapper_directory: str,
    python_directory: str,
    extension: str,
    filename: str,
) -> None:
    """
    Autogenerate python and fortran code according to a module definition

    This function writes 3 files:

    * manager - Lifecycle handling for calculators (in Fortran)

    * wrapper - Provides a fortran wrapper to the generated functions that can be
        made available to Python

    * python module - Python interface for creating and manipulating calculators.

    FILENAME is a path to a YAML file describing the calculator which is being exposed to Python
    """
    if manager_directory is None:
        manager_directory = os.path.dirname(filename)

    module = load_module_definition(filename)

    process_module(
        module,
        extension=extension,
        manager_directory=manager_directory,
        wrapper_directory=wrapper_directory,
        python_directory=python_directory,
        force=force,
    )

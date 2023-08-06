"""
Output file generation from templates
"""
import functools
import logging
import os

from black import Mode, format_str
from jinja2 import Environment, PackageLoader, select_autoescape

from fgen.schema import ModuleDefinition

logger = logging.getLogger(__name__)

env = Environment(
    loader=PackageLoader("fgen"),
    autoescape=select_autoescape(),
    trim_blocks=True,
    lstrip_blocks=True,
)


def _add_trailing_line(inp: str) -> str:
    # jinja trims the trailing line-break from the template
    return inp + "\n"


def generate_calculator_manager(module: ModuleDefinition) -> str:
    """
    Generate manager module for a module

    Parameters
    ----------
    module
        Module configuration

        Each module contains a single calculator

    Returns
    -------
        Serialised fortran code
    """
    template = env.get_template("calculator_manager.f90.jinja")

    result = _add_trailing_line(
        template.render(
            module=module,
            calculator=module.provides,
        )
    )

    return result


def generate_python_module(module: ModuleDefinition, extension: str) -> str:
    """
    Generate python module for a calculator

    Parameters
    ----------
    module
        Module configuration

        Each module contains a single calculator
    extension
        Name of the extension module that will contain the compiled wrappers

    Returns
    -------
        Serialised python code
    """
    template = env.get_template("python_module.py.jinja")

    result = _add_trailing_line(
        template.render(module=module, calculator=module.provides, extension=extension)
    )
    # Format result with black
    # This doesn't automatically read `pyproject.toml` so settings must be prescribed
    return format_str(result, mode=Mode(line_length=88))


def generate_wrap_module(module: ModuleDefinition) -> str:
    """
    Generate the fortran wrapper for a module

    Parameters
    ----------
    module
        Module configuration

        Each module contains a single calculator

    Returns
    -------
        Serialised fortran code
    """
    template = env.get_template("wrap_module.f90.jinja")

    result = _add_trailing_line(
        template.render(
            module=module,
            calculator=module.provides,
            calculator_module=f"mod_{ module.short_name }_manager",
        )
    )

    return result


def _write_file(data: str, filename: str, force: bool = False) -> None:
    if os.path.exists(filename):
        if force:
            logger.warning("Forcefully overwriting existing file: %s", filename)
        else:
            raise FileExistsError(filename)

    with open(filename, mode="w", encoding="utf-8") as file_handle:
        file_handle.write(data)


def process_module(  # noqa: PLR0913
    module: ModuleDefinition,
    extension: str,
    manager_directory: str,
    wrapper_directory: str,
    python_directory: str,
    force: bool = True,
) -> None:
    """
    Autogenerate python and fortran code according to a module definition

    This function writes 3 files:

    * manager - Lifecycle handling for calculators (in Fortran)
    * wrapper - Provides a fortran wrapper to the generated functions that can be
        made available to Python
    * python module - Python interface for creating and manipulating calculators.

    Parameters
    ----------
    module

    extension
        Package name for the compiled extension module

        Typically, this is of the form `my_module._lib`

    manager_directory
        Directory to write the manager module

        This is typically beside the yaml file describing the module and the calculator

    wrapper_directory
        Directory to write the wrapper module

        This is typically ``libmagicc/wrappers``

    python_directory
        Directory to write the python module

        This is typically in magiccly under ``_lib``

    force
        If True, overwrite any existing files

    Raises
    ------
    FileExistError
        If ``not force`` and a targetted file exists
    """
    for desc, generator_function, suffix, outdir in (
        (
            "manager",
            generate_calculator_manager,
            "_manager.f90",
            manager_directory,
        ),
        ("wrapper", generate_wrap_module, "_wrapped.f90", wrapper_directory),
        (
            "python",
            functools.partial(generate_python_module, extension=extension),
            ".py",
            python_directory,
        ),
    ):
        try:
            filename = os.path.join(outdir, f"{module.short_name}{suffix}")
            logger.info("Writing %s module to %s", desc, filename)
            _write_file(generator_function(module), filename, force=force)
        except Exception:
            logger.exception("One or more files maybe partly written")
            raise

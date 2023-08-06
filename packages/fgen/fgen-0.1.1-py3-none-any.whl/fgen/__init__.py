"""
An opinionated framework for wrapping Fortran-based code with Python.
"""
from importlib.metadata import version as _version

try:
    __version__ = _version("fgen")
except Exception:  # pylint: disable=broad-except  # pragma: no cover
    # Local copy, not installed with setuptools
    __version__ = "unknown"

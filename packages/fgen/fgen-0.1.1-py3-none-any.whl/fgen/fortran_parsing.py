"""
Support for parsing Fortran

We want to keep this as minimal as possible because duplicating the Fortran
implementation logic is not the point.
"""
from __future__ import annotations

import re
from collections.abc import Sequence

KNOWN_FORTRAN_TYPES: dict[str, type] = {
    "real": float,
    "integer": int,
    "character": str,
    "logical": bool,
}
"""Fortran types for which we know the equivalent Python type"""

AT_LEAST_ONE_ALPHANUMERIC_REGEXP: str = r"[a-z0-9]+"
"""Regex representing a search for at least one alphanumeric character"""

DIMENSION_SPEC: str = f"(:|{AT_LEAST_ONE_ALPHANUMERIC_REGEXP})"
"""Regex representing a possible dimension specifier in a Fortran definition"""

DIMENSION_REGEX: re.Pattern = re.compile(
    r"dimension\("
    r"(?P<dimension>"
    f"{DIMENSION_SPEC}(,\\s*{DIMENSION_SPEC})*"
    ")"
    r"\)"
)
"""Regex used to check for dimension information of fortran types"""


SUPPORTED_TYPE_ATTRIBUTES: tuple[re.Pattern] = (DIMENSION_REGEX,)
"""Type attributes which we support"""


def get_parts(type_spec: str) -> list[str]:
    """
    Get the parts of a Fortran type specification

    Parameters
    ----------
    type_spec
        Type specification to parse

    Returns
    -------
        Parts of the specification

    Examples
    --------
    >>> get_parts("real")
    ['real']
    >>> get_parts("real, dimension(5)")
    ['real', 'dimension(5)']
    >>> get_parts("real, dimension(5, 3)")
    ['real', 'dimension(5, 3)']
    >>> get_parts("integer, dimension(:, :)")
    ['integer', 'dimension(:, :)']
    >>> get_parts("logical, dimension(2, :)")
    ['logical', 'dimension(2, :)']
    """
    spec_comma_split = type_spec.split(",")
    parts = []
    idx = 0
    while idx < len(spec_comma_split):
        part = spec_comma_split[idx]
        if "(" in part and ")" not in part:
            for j, t_later in enumerate(spec_comma_split[idx + 1 :]):
                if ")" in t_later:
                    # put back together
                    part = ",".join(spec_comma_split[idx : idx + j + 2])
                    idx += j + 2
        else:
            idx += 1

        parts.append(part.strip())

    return parts


def get_fortran_type(type_spec: str) -> str:
    """
    Get Fortran type from type specification

    Parameters
    ----------
    type_spec
        Type specification to parse

    Returns
    -------
        Fortran type
    """
    parts = get_parts(type_spec)
    return get_fortran_type_from_parts(parts)


def get_fortran_type_from_parts(parts: Sequence[str]) -> str:
    """
    Get Fortran type from parts

    Parameters
    ----------
    parts
        Parts of the Fortran type specification e.g.
        ``["real", "dimension(3)"]``

    Returns
    -------
        Fortran type, without any other attributes
    """
    # assume first part is data type and strip off any dimension specs from
    # data type to get Fortran type
    fortran_type = parts[0].split("(")[0]

    return fortran_type


def get_python_type_with_dimensions(
    dimension_info: str,
    base_type: type,
) -> type:
    """
    Get Python type that supports dimension information

    This is derived from a Fortran type specification that includes dimension
    information

    Parameters
    ----------
    dimension_info
        Dimension information

    base_type
        Base type to which the dimension information applies

    Returns
    -------
        Python type

    Examples
    --------
    >>> get_python_type_with_dimensions("2", float)
    tuple[float, float]
    >>> get_python_type_with_dimensions(":", bool)
    tuple[bool, ...]
    >>> get_python_type_with_dimensions("n", int)
    tuple[int, ...]
    >>> get_python_type_with_dimensions("2, 3", float)
    tuple[tuple[float, float], tuple[float, float, float]]
    >>> get_python_type_with_dimensions("2, 1", float)
    tuple[tuple[float, float], tuple[float]]
    >>> get_python_type_with_dimensions("2, :", float)
    tuple[tuple[float, float], tuple[float, ...]]
    >>> get_python_type_with_dimensions("n, m, 2, :", int)
    tuple[tuple[int, ...], tuple[int, ...], tuple[int, int], tuple[int, ...]]
    """
    toks = dimension_info.split(",")

    type_info = []
    for tok in toks:
        try:
            size = int(tok)
            s_type_info = tuple[tuple(base_type for _ in range(size))]
        except ValueError:
            # assume : or n or something i.e. not static size
            s_type_info = tuple[base_type, ...]

        type_info.append(s_type_info)

    if len(type_info) == 1:
        return type_info[0]

    return tuple[tuple(type_info)]

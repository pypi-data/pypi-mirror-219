"""
Configuration schema

This schema is used to serialize and validate the YAML configuration files.
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Optional, TypeVar

from attrs import define, field, fields, validators
from cattrs.preconf.pyyaml import make_converter

from .fortran_parsing import (
    DIMENSION_REGEX,
    KNOWN_FORTRAN_TYPES,
    SUPPORTED_TYPE_ATTRIBUTES,
    get_fortran_type,
    get_fortran_type_from_parts,
    get_parts,
    get_python_type_with_dimensions,
)

if TYPE_CHECKING:
    import attr


T = TypeVar("T")

converter = make_converter(detailed_validation=False, forbid_extra_keys=True)


def fortran_type_validator(
    instance: ValueDefinition,  # pylint: disable=unused-argument
    attribute: attr.Attribute[str],  # pylint: disable=unused-argument
    value: str,
) -> None:
    """
    Validate that a fortran unit is supported by fgen

    We don't support all valid fortran datatypes and attributes. The parsing
    is also quite naive so the ordering matters. See the tests for examples of supported types

    This validation is pretty crude as unsupported/invalid types will be caught at
    compile time.

    Parameters
    ----------
    instance
        Unused
    attribute
        Unused
    value
        Fortran type string

        The type string should be a comma-separated string with the "datatype" being the first item,
         followed by 0 or more attributes such as `dimension`. This is a very small subset of
         possible fortran types

    Raises
    ------
    ValueError
        An unsupported fortran type is supplied

    Examples
    --------
    Below are some examples of valid fortran types

    >>> fortran_type_validator(None, None, "integer")
    >>> fortran_type_validator(None, None, "real, dimension(5)")
    """
    tokens = get_parts(value)
    fortran_type = get_fortran_type_from_parts(tokens)
    if fortran_type not in KNOWN_FORTRAN_TYPES:
        raise ValueError(f"Unsupported fortran type: {value}")

    # Any attributes must match the regex of a supported attribute
    for token in tokens[1:]:
        if not any(
            attribute_regex.search(token)
            for attribute_regex in SUPPORTED_TYPE_ATTRIBUTES
        ):
            raise ValueError(f"Unsupported attribute in the type: {token}")


@define
class ValueDefinition:
    """
    Definition of a value

    This defines the value's unit, Fortran data type and other metadata. It also allows us to get the
    equivalent Python type.

    The following built-in Fortran types are supported:

    * integer
    * real
    * real(8)
    * character

    Some additional attributes are supported including:

    * fixed length dimensions
    * allocatable or variable length dimensions
    """

    name: str
    description: str
    unit: str
    type: str = field(validator=[validators.instance_of(str), fortran_type_validator])
    expose_to_python: bool = True
    truncated_name: Optional[str] = None

    def python_type(self) -> type:
        """
        Determine the equivalent type for Python

        Raises
        ------
        ValueError
            An unknown type is encountered.

        Returns
        -------
            The type corresponding with :attr:`type`
        """
        base_type = KNOWN_FORTRAN_TYPES[get_fortran_type(self.type)]

        # Check if a dimension attribute was specified
        dimension_info = DIMENSION_REGEX.search(self.type)
        if dimension_info:
            return get_python_type_with_dimensions(
                dimension_info.group("dimension"), base_type
            )

        return base_type

    def python_type_as_str(self) -> str:
        """
        Determine the string representation of the Python type

        The python templator uses this function to translate a Python
        type to a string so that it can correctly be read by Python.
        If these type hints are converted to a string naively, the
        corresponding string will not be able to be read by Python as a valid type hint.

        Returns
        -------
            String representation of :attr:`python_type`
        """
        py_type = self.python_type()

        # Works for typehints
        res = repr(py_type)

        if "<class" in res:
            # Required for float, int etc
            res = py_type.__name__

        return res


def _add_name(inp: dict[str, dict[str, str]], cls: type[dict[str, T]]) -> dict[str, T]:
    """
    Add the name to attributes and methods automatically

    This avoids having to write schemas like

    .. ::code-block

    Attributes
    ----------
          k:
            name: k
            description: something

    Methods
    -------
          calculate:
            name: calculate
            description: something else

    Instead we can just write

    .. ::code-block

    Attributes
    ----------
          k:
            description: something

    Methods
    -------
          calculate:
            description: something else

    Where the name is inferred automatically
    """
    value_type = cls.__args__[1]

    res = {}

    if inp is None:
        raise ValueError(f"Unexpected None when structuring {cls}")

    for k, v in inp.items():
        for f in fields(value_type):
            if str(f.type).startswith("dict") and v.get(f.name) is None:
                raise ValueError(
                    f"{f.name!r} in {k!r} is None but a dict was expected: {v}"
                )
        if "name" in v:
            if v["name"] != k:
                raise ValueError(
                    f"Inconsistent name for value: {k!r} and {v['name']!r}"
                )
        res[k] = converter.structure({"name": k} | v, value_type)

    return res


converter.register_structure_hook_func(
    lambda t: t == dict[str, ValueDefinition], _add_name
)


@define
class MethodDefinition:
    """
    Definition of a fortran function

    This
    """

    name: str
    description: str
    parameters: dict[str, ValueDefinition]
    returns: Optional[ValueDefinition]

    def units(self) -> dict[str, str]:
        """
        Units used in the method

        Includes units from of the parameters and the return value.

        Raises
        ------
        ValueError
            If different units are supplied for a given parameter name

        Returns
        -------
            Collection of parameter names and associated units

        """
        res = {key: parameter.unit for key, parameter in self.parameters.items()}

        if self.returns:
            k = self.returns.name
            if k in res and res[k] != self.returns.unit:
                raise ValueError(
                    f"Inconsistent units for attribute '{k}'. In the input parameters it "
                    f"has units '{res[k]}' whereas in the returns it has units '{self.returns.unit}'"
                )

            res[self.returns.name] = self.returns.unit

        return res


converter.register_structure_hook_func(
    lambda t: t == dict[str, MethodDefinition], _add_name
)


@define
class CalculatorDefinition:
    """
    Definition of a calculator

    TODO: document concepts
    """

    name: str
    description: str
    attributes: dict[str, ValueDefinition]
    methods: dict[str, MethodDefinition]

    def exposed_attributes(self) -> dict[str, ValueDefinition]:
        """
        Get the attributes that are marked to be exposed to python

        Returns
        -------
            Collection of exposed attributes
        """
        return dict(
            filter(lambda item: item[1].expose_to_python, self.attributes.items())
        )

    def units(self) -> dict[str, str]:
        """
        Get the unit for each declared value in the calculator

        The unit for a given named value must be consistent across the calculator.
        This includes the unit for ``attributes``, and in the ``parameter`` and
        ``return`` values for each ``method``.

        Raises
        ------
        ValueError
            Inconsistent units were found

        Returns
        -------
            Dictionary containing value names' as keys and the associated units
            as values.
        """
        res: dict[str, tuple[Optional[str], str]] = {
            key: (None, attr.unit) for key, attr in self.attributes.items()
        }

        for name, method in self.methods.items():
            method_units = method.units()

            for k, v in method_units.items():
                if k in res and res[k][1] != v:
                    previous_source, previous_value = res[k]
                    if previous_source is not None:
                        previous_source_type = "method"
                    else:
                        previous_source_type = "calculator"
                        previous_source = self.name

                    raise ValueError(
                        f"Inconsistent units for attribute '{k}'. "
                        f"In the method '{name}' it has units '{v}' whereas in the {previous_source_type} "
                        f"'{previous_source}' it has units '{previous_value}'"
                    )
                res[k] = (name, v)
        return {key: value[1] for key, value in res.items()}


@define
class ModuleDefinition:
    """
    Definition of a Fortran Module

    It is assumed that each fortran module defines a single Calculator

    TODO: document concepts
    """

    name: str
    description: str
    provides: CalculatorDefinition
    prefix: str = "mod_"
    truncated_name: Optional[str] = None

    @property
    def wrapper_module_name(self) -> str:
        """
        Name for the Fortran wrapper module

        By default the module name is derived from the :attr:`name`, but in
        some cases, the complete module name can be too long leading to the
        wrapper module not being able to be built. In this case a
        :attr:`truncated_name` can be used to derive a shorted module name.
        Given that this module is only used by autogenerated code the
        readability of the name isn't as important as the full module.
        """
        return self.truncated_name or f"w_{self.truncated_name or self.short_name}"

    @property
    def short_name(self) -> str:
        """
        Short module name

        Some fortran modules have a prefix, typically `"mod_"` which isn't used in all cases
        when referring to the module, e.g. when writing filenames. ``short_name``
        removes this prefix if it is there.

        Returns
        -------
            Shortened module name
        """
        if self.name.startswith(self.prefix):
            return self.name[len(self.prefix) :]
        return self.name


def load_module_definition(filename: str) -> ModuleDefinition:
    """
    Read a YAML module definition file

    This module definition contains a description of the Fortran module that
    is being wrapped.

    Parameters
    ----------
    filename
        Filename to read

    Returns
    -------
        Loaded module definition
    """
    # Does this ensure the file handle is closed more cleanly?
    with open(filename, encoding="utf-8") as fh:
        txt = fh.read()

    return converter.loads(txt, ModuleDefinition)

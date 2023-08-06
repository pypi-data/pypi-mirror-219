"""
Base class for wrapped calculators
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from contextlib import AbstractContextManager
from functools import wraps
from typing import Callable, TypeVar

import attrs
from attrs import define, field
from typing_extensions import Concatenate, ParamSpec

from fgen_runtime.common import _UNINITIALISED_MODEL_INDEX
from fgen_runtime.exceptions import InitialisationError


@define
class FinalizableWrapperBase(ABC):
    """
    Base class for model wrappers
    """

    model_index: int = field(
        validator=attrs.validators.instance_of(int),
        default=_UNINITIALISED_MODEL_INDEX,
    )
    """
    Model index of wrapper Fortran instance
    """

    @classmethod
    @abstractmethod
    def from_new_connection(cls) -> FinalizableWrapperBase:
        """
        Initialise by establishing a new connection with the Fortran module

        This requests a new model index from the Fortran module and then
        initialises a class instance

        Returns
        -------
        New class instance
        """

    @abstractmethod
    def finalize(self) -> None:
        """
        Finalise the Fortran instance and set self back to being uninitialised

        This method resets ``self.model_index`` back to
        ``_UNINITIALISED_MODEL_INDEX``

        Should be decorated with :func:`check_initialised`
        """
        # call to Fortran module goes here when implementing
        self._unitialise_model_index()

    def _unitialise_model_index(self) -> None:
        self.model_index = _UNINITIALISED_MODEL_INDEX

    @property
    def initialized(self) -> bool:
        """
        Is the instance initialised, i.e. connected to a Fortran instance?
        """
        return self.model_index != _UNINITIALISED_MODEL_INDEX


@define
class FinalizableWrapperBaseContext(AbstractContextManager):
    """
    Context manager for a wrapper
    """

    model: FinalizableWrapperBase
    """
    model instance to be managed
    """

    def __enter__(self) -> FinalizableWrapperBase:
        if not self.model.initialized:
            raise InitialisationError(self.model)

        return self.model

    def __exit__(self, *args, **kwargs) -> None:
        self.model.finalize()


P = ParamSpec("P")
T = TypeVar("T")
Wrapper = TypeVar("Wrapper", bound=FinalizableWrapperBase)


def check_initialised(method: Callable[P, T]) -> Callable[P, T]:
    """
    Check that initialisation is called before execution

    Parameters
    ----------
    method
        Method to wrap

    Returns
    -------
    Wrapped method. Before the method is called, initialisation will first be
    checked. If the model wrapper hasn't been initialised before the method is
    called, an ``InitialisationError`` will be raised.
    """

    @wraps(method)
    def checked(
        ref: Wrapper,
        *args: P.args,
        **kwargs: P.kwargs,
    ):
        if not ref.initialized:
            raise InitialisationError(ref, method)

        return method(ref, *args, **kwargs)

    return checked


# Thank you for type hints info
# https://adamj.eu/tech/2021/05/11/python-type-hints-args-and-kwargs/
def execute_finalize_on_fail(
    inst: FinalizableWrapperBase,
    func_to_try: Callable[Concatenate[int, P], T],
    *args: P.args,
    **kwargs: P.kwargs,
) -> T:
    """
    Execute a function, finalising the instance before raising if any error occurs

    This function is most useful in factory functions where it provides a
    clean way of ensuring that any Fortran is freed up in the event of an
    initialisation failure for any reason

    Parameters
    ----------
    inst
        Instance whose model index we will use when executing the functin

    func_to_try
        Function to try executing, must take ``inst``'s model index as its
        first argument

    *args
        Passed to ``func_to_try``

    **kwargs
        Passed to ``func_to_try``

    Returns
    -------
    Result of calling ``func_to_try(inst.model_index, *args, **kwargs)``

    Raises
    ------
    Exception
        Any exception which occurs when calling ``func_to_try. Before the
        exception is raised, ``inst.finalize()`` is called.
    """
    try:
        return func_to_try(inst.model_index, *args, **kwargs)
    except RuntimeError:
        # finalize the instance before raising
        inst.finalize()

        raise

"""
Exception classes for wrapper-specific errors
"""


class WrapperError(ValueError):
    """
    Base exception for errors that arise from wrapper
    """


class InitialisationError(WrapperError):
    """
    Wrapper around Fortran module hasn't been initialised yet
    """

    def __init__(self, model, method=None):
        if method:
            error_msg = f"{model} must be initialised before {method} is called"
        else:
            error_msg = f"model ({model:r}) is not initialized yet"

        super().__init__(error_msg)

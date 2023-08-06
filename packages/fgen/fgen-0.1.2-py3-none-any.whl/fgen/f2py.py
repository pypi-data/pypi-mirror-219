"""
f2py wrapper

Patches the default behaviour of f2py with some custom error handling. This was inspired by the amazing
[f90wrap](https://github.com/jameskermode/f90wrap).
"""
import sys

import numpy.f2py.rules as f2py_rules
from numpy.f2py import main as f2py_main


def patch_f2py():
    """
    Patch f2py to raise a RuntimeError if :c:func:`on_error` is called during execution

    Interrupt signals are also captured and handled. This has only been tested with numpy 1.21.0
    and may be flakey if f2py has substantial changes
    """
    includes_inject = "#includes0#\n"

    if sys.platform == "win32":
        includes_inject = (
            includes_inject + "#include <signal.h>\n#include <setjmpex.h>\n"
        )
    else:
        includes_inject = includes_inject + "#include <setjmp.h>\n"

    includes_inject = (
        includes_inject
        + """
    #include <stdlib.h>
    #include <string.h>

    #define ABORT_BUFFER_SIZE 512
    extern jmp_buf environment_buffer;
    extern char abort_message[ABORT_BUFFER_SIZE];
    void on_error_(char *message, size_t len);
    void abort_int_handler(int signum);

    jmp_buf environment_buffer;
    char abort_message[ABORT_BUFFER_SIZE];

    // Error handler for magiccly
    void on_error_(char *message, size_t len_message)
    {
      strncpy(abort_message, message, ABORT_BUFFER_SIZE);
      abort_message[ABORT_BUFFER_SIZE-1] = '\\0';
      longjmp(environment_buffer, 0);
    }

    // Handle sigint signals (ctrl + c) during a f2py calls
    void sigint_handler(int signum)
    {
      char message[] = "User interrupt occurred";
      on_error_(message, strlen(message));
    }
    """
    )

    f2py_rules.module_rules["modulebody"] = f2py_rules.module_rules[
        "modulebody"
    ].replace("#includes0#\n", includes_inject)

    f2py_rules.routine_rules["body"] = f2py_rules.routine_rules["body"].replace(
        "volatile int f2py_success = 1;\n",
        "volatile int f2py_success = 1; int setjmp_value;",
    )

    f2py_rules.routine_rules["body"] = f2py_rules.routine_rules["body"].replace(
        "#callfortranroutine#\n",
        """
        PyOS_sighandler_t _npy_sig_save;

        // Catch any sigint (ctrl + c) with a call to sigint_handler
        _npy_sig_save = PyOS_setsig(SIGINT, sigint_handler);
        setjmp_value = setjmp(environment_buffer);

        if (setjmp_value != 0) {
          // jumped back as a result of a call to longjmp
          // Raise a RuntimeError
          PyOS_setsig(SIGINT, _npy_sig_save);
          PyErr_SetString(PyExc_RuntimeError, abort_message);
        } else {
         #callfortranroutine#
         PyOS_setsig(SIGINT, _npy_sig_save);
        }
        """,
    )


if __name__ == "__main__":
    print("PATCHED version of f2py")
    patch_f2py()
    f2py_main()

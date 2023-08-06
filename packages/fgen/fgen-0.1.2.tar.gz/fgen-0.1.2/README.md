# Fortran-Python wrapper

<!---
Can use start-after and end-before directives in docs, see
https://myst-parser.readthedocs.io/en/latest/syntax/organising_content.html#inserting-other-documents-directly-into-the-current-document
-->

<!--- sec-begin-description -->

Automatically generate wrappers to integrate Fortran and Python


This project consists of a few different components:

* fgen
* fgen_runtime
* libfgen

<!--- sec-end-description -->

Full documentation can be found at:
[fgen.readthedocs.io](https://fgen.readthedocs.io/en/latest/).
We recommend reading the docs there because the internal documentation links
don't render correctly on GitLab's viewer. TODO: Create docs

## Installation

<!--- sec-begin-installation -->

Fortran-Python wrapper can be installed with conda or pip:

```bash
pip install fgen
conda install -c conda-forge fgen
```


<!--- sec-end-installation -->

### For developers

<!--- sec-begin-installation-dev -->

For development, we rely on [poetry](https://python-poetry.org) for all our
dependency management. To get started, you will need to make sure that poetry
is installed
([instructions here](https://python-poetry.org/docs/#installing-with-the-official-installer),
we found that pipx and pip worked better to install on a Mac).

For all of work, we use our `Makefile`.
You can read the instructions out and run the commands by hand if you wish,
but we generally discourage this because it can be error prone.
In order to create your environment, run `make virtual-environment`.

Once the virtual environment has been created, `libfgen` can be built
using `make build`. This library contains the common Fortran code used by
all wrappers and uses [CMake](https://cmake.org/) to build and requires
a working Fortran compiler.

If there are any issues, the messages from the `Makefile` should guide you
through. If not, please raise an issue in the [issue tracker][issue_tracker].

For the rest of our developer docs, please see [](development-reference).

[issue_tracker]: https://gitlab.com/magicc/fgen/issues

<!--- sec-end-installation-dev -->

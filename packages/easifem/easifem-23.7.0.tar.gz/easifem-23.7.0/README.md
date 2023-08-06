# easifem

[![PyPI - Version](https://img.shields.io/pypi/v/easifem-cli.svg)](https://pypi.org/project/easifem)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/easifem-cli.svg)](https://pypi.org/project/easifem)

easifem is a command line interface (CLI) for using EASIFEM library.

Expandable And Scalable Infrastructure for Finite Element Methods, EASIFEM, is Modern Fortran framework for solving partial differential equations (PDEs) using finite element methods. EASIFEM eases the efforts to develop scientific programs in Fortran. It is meant for researchers, scientists, and engineers using Fortran to implement numerical methods for solving the initial-boundary-value problems (IBVPs)."

-----

**Table of Contents**

- [Installation](#installation)
- [License](#license)

## Installation

```console
pip install easifem
```

## License

`easifem` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.

## Getting started

`easifem` provides following subcommands:

1. setenv
2. install
4. run

## `setenv`

```bash
easifem setenv --install="PATH_INSTALL_DIR" --build="PATH_BUILD_DIR" --source="PATH_SOURCE_DIR"
```

This will create `easifemvar.sh` (for Bash and Zsh) and `easifemvar.fish` for (Fish shell). These files will be located at `~/.config/easifem`.

## install

```bash
easifem install extpkgs
easifem install base
easifem install classes
easifem install materials
easifem install kernels
easifem install easifem
```

## run

## To-do

Following command will be added in the future.

1. update
2. uninstall
3. build

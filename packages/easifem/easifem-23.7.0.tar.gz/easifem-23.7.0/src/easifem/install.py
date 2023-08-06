import argparse
 
_DESCRIPTION = """
The [install] subcommand helps you installing the components of  
EASIFEM, such as extpkgs, base, classes, materials, kernels, etc.

In order to install a component you should specify following environment variables:
A) EASIFEM_ROOT_DIR: the place where easifem is installed. 
B) EASIFEM_BUILD_DIR: the place where easifem is build. 
C) EASIFEM_SOURCE_DIR: the place where the source of easifem will be stored.

You can specify them by using

easifem setenv --build= --install= --source=

For more see,
easifem setenv --help 

Use:

easifem install option

Option can be:

all: Install everything
extpkgs: install external packages
openblas : install OpenBlas
lapack95: install LAPACK95
sparsekit: install Sparsekit
fftw: install FFTW
superlu: install SuperLU
arpack: install ARPACK
lis: install LIS
base: install easifemBase
classes: install easifemClasses
materials: install easifemMaterials
kernels: install easifemKernels
"""

def parser(subparser):

    ans = subparser.add_parser(
        "install",
        help="Install components of easifem.",
        description=_DESCRIPTION,
        formatter_class=argparse.RawTextHelpFormatter,
    )

    ans.add_argument(
        "-i",
        "--install",
        help="Location where easifem is installed, EASIFEM_INSTALL_DIR",
        required=False,
    )

    ans.add_argument(
        "-b",
        "--build",
        help="Location where easifem will be build, EASIFEM_BUILD_DIR",
        required=False,
    )

    ans.add_argument(
        "-s",
        "--source",
        help="Location where the source-code of easifem will be stored, EASIFEM_SOURCE_DIR",
        required=False,
    )

    ans.add_argument(
        "-q",
        "--quite",
        help="If specified lesser output will be printed",
        action="store_true",
    )

    ans.add_argument(
        "components",
        metavar="c",
        type=str,
        nargs="+",
        help="Names of components to install",
    )

    return ans

import argparse

_DESCRIPTION = """
[clean] subcommand helps you clean the build files and cache
build during the installation of easifem. 
• Cleaning external packages: easifem clean extpkgs
• Cleaning base: easifem clean base
• Cleaning classes: easifem clean classes
• Cleaning everything: easifem clean all
"""


def parser(subparser):

    ans = subparser.add_parser(
        "clean",
        help="Clean the installation files.",
        description=_DESCRIPTION,
        formatter_class=argparse.RawTextHelpFormatter,
    )

    ans.add_argument(
        "components",
        metavar="c",
        type=str,
        nargs="+",
        help="Names of components to clean, e.g. all, extpkgs, base, classes, materials, kernels",
    )

    ans.add_argument(
        "-b",
        "--build",
        help="Location where easifem will be build, EASIFEM_BUILD_DIR",
        required=False,
    )

    return ans

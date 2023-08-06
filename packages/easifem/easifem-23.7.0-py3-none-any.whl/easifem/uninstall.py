import argparse

_DESCRIPTION = """
[uninstall] subcommand helps you to uninstall the easifem components.
• Uninstall external packages: easifem uninstall extpkgs
• Uninstall base: easifem uninstall base
• Uninstall classes: easifem uninstall classes
• Uninstall classes: easifem uninstall materials
• Uninstall classes: easifem uninstall kernels
• Uninstall everything: easifem uninstall all
"""


def parser(subparser):

    ans = subparser.add_parser(
        "uninstall",
        help="Uninstall the installation files.",
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
        "-i",
        "--install",
        help="Location where easifem will is installed, i.e., EASIFEM_INSTALL_DIR",
        required=False,
    )

    return ans

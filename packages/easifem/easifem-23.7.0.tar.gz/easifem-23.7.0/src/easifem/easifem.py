#!/usr/bin/env python3

import argparse
from easifem.utils_run import easifem_run as run
from easifem.utils_setenv import easifem_setenv as setenv
from easifem.utils_install import easifem_install as install
from easifem.utils_clean import easifem_clean as clean
from easifem.utils_uninstall import easifem_uninstall as uninstall
from easifem.parsers import *
import os

_DESCRIPTION = """
easifem is a CLI (Command Line Interface) to libeasifem.
It contains some subcommands to help you work with libeasifem.
It can help you in building an application based on easifem components.
It can also build and install the easifem library.

For more information visit:
website: https://www.easifem.com: 
(c) Vikas Sharma, 2023
"""

parser = argparse.ArgumentParser(
    prog="python3 easifem.py",
    description="""
    easifem.py is a CLI (Command Line Interface) to libeasifem.
    It contains some subcommands to help you work with libeasifem.
    It can help you in building an application based on easifem components.
    It can also build and install the easifem library.
    For more information visit:
    website: www.easifem.com: 
    (c) Vikas Sharma, 2023
    """,
    epilog="www.easifem.com, (c) Vikas Sharma, 2023",
    formatter_class=argparse.RawTextHelpFormatter,
)

subparser = parser.add_subparsers(
    title="subcommand",
    dest="subcommand",
    prog="easifem.py test [options]",
    required=False,
)


def easifem_test(args):
    run(
        file=args.file,
        quite=args.quite,
        targetName=args.target if args.target else "test",
        easifemLibs=args.easifem_libs if args.easifem_libs else "easifemBase",
        installPrefix=args.prefix if args.prefix else "*--testing--*",
    )


def easifem_run(args):
    run(
        file=args.file,
        quite=args.quite,
        targetName=args.target if args.target else "test",
        easifemLibs=args.easifem_libs if args.easifem_libs else "easifemBase",
        installPrefix=args.prefix if args.prefix else ".",
    )


def easifem_setenv(args):
    setenv(
        quite=args.quite,
        install=args.install if args.install else os.environ["HOME"],
        build=args.build if args.build else os.path.join(os.environ["HOME"], "temp"),
        source=args.source if args.source else os.path.join(os.environ["HOME"], "code"),
        shell=args.shell if args.shell else "bash",
    )


def easifem_install(args):
    install(
        components=args.components,
        quite=args.quite,
        install=args.install if args.install else None,
        build=args.build if args.build else None,
        source=args.source if args.source else None,
    )


def easifem_clean(args):
    clean(
        components=args.components,
        build=args.build if args.build else None,
    )


def easifem_uninstall(args):
    uninstall(
        components=args.components,
        install=args.install if args.install else None,
    )


parser_test = testParser(subparser)
parser_run = runParser(subparser)
parser_setenv = setenvParser(subparser)
parser_install = installParser(subparser)
parser_clean = cleanParser(subparser)
parser_uninstall = uninstallParser(subparser)


def main():
    args = parser.parse_args()
    if args.subcommand:
        if args.subcommand == "test":
            easifem_test(args)
        elif args.subcommand == "run":
            easifem_run(args)
        elif args.subcommand == "setenv":
            easifem_setenv(args)
        elif args.subcommand == "install":
            easifem_install(args)
        elif args.subcommand == "uninstall":
            easifem_uninstall(args)
        elif args.subcommand == "clean":
            easifem_clean(args)


if __name__ == "__main__":
    main()

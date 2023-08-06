import argparse

_DESCRIPTION = """
The [setenv] subcommand sets the environment variable for easifem on your system.

While setting the environment you can provide following details.
A) EASIFEM_INSTALL_DIR
B) EASIFEM_BUILD_DIR
C) EASIFEM_SOURCE_DIR

EASIFEM_INSTALL_DIR: denotes the root location where EASIFEM will
be installed. It is specified by --install=value

Following are the good choices for --install variable:
1) ${HOME}
2) ${HOME}/.local
3) /opt
The default value is ${HOME}.

EASIFEM_SOURCE_DIR: specifies the location where the source code of
the components of EASIFEM will be stored.
It is specified by --source=value 

Following are the good choices for --source variable:
1) ${HOME}/code/
The default value is ${HOME}/code.
EASIFEM_BUILD_DIR: specifies the location where the components of 
EASIFEM will be build. It is specified by --build=value 

Following are the good choices for --root variable:
1) ${HOME}/temp 
The default value is ${HOME}/temp.

Example:

easifem setenv --install ${HOME} --build ${HOME}/temp --source ${HOME}/code
easifem setenv -r ${HOME} -b ${HOME}/temp -s ${HOME}/code
"""


def parser(subparser):

    ans = subparser.add_parser(
        "setenv",
        help="Set environment variables for running easifem on your system.",
        description=_DESCRIPTION,
        formatter_class=argparse.RawTextHelpFormatter,
    )

    ans.add_argument(
        "-i",
        "--install",
        help="Root directory for easifem, EASIFEM_INSTALL_DIR",
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
        "--shell",
        help="System shell that you are using, you have following choices: [bash, zsh, fish]",
        required=False,
        choices=[
            "bash",
            "zsh",
            "fish",
        ],
    )

    ans.add_argument(
        "-q",
        "--quite",
        help="If specified lesser output will be printed",
        action="store_true",
    )

    return ans

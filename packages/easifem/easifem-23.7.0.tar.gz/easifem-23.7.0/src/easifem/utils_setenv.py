import os
from easifem.console import console
from rich.panel import Panel
from rich.text import Text

_easifem = "easifem"
_keys = [
    "EASIFEM_BASE",
    "EASIFEM_CLASSES",
    "EASIFEM_EXTPKGS",
    "EASIFEM_APP",
    "EASIFEM_MATERIALS",
    "EASIFEM_KERNELS",
]

_values = [
    "base",
    "classes",
    "extpkgs",
    "app",
    "materials",
    "kernels",
]

_build0 = os.path.join(os.environ["HOME"], "temp")
_install0 = os.environ["HOME"]
_source0 = os.path.join(os.environ["HOME"], "code")


def easifem_setenv(
    quite=False,
    install=_install0,
    build=_build0,
    source=_source0,
    shell="bash",
):

    os.environ["EASIFEM_INSTALL_DIR"] = str(install)
    os.environ["EASIFEM_BUILD_DIR"] = str(build)
    os.environ["EASIFEM_SOURCE_DIR"] = str(source)

    for i in range(len(_keys)):
        os.environ[_keys[i]] = os.path.join(
            install,
            _easifem,
            _values[i],
        )

    if not quite:
        console.print(f"◌ Environment variables for EASIFEM")
        console.print(f"◌ EASIFEM_INSTALL_DIR: {os.environ.get('EASIFEM_INSTALL_DIR')}")
        console.print(f"◌ EASIFEM_BUILD_DIR: {os.environ.get('EASIFEM_BUILD_DIR')}")
        console.print(f"◌ EASIFEM_SOURCE_DIR: {os.environ.get('EASIFEM_SOURCE_DIR')}")

        for key in _keys:
            console.print(f"◌ {key}: {os.environ.get(key)}")

    _config_path = os.path.join(os.environ["HOME"], ".config", "easifem")
    os.makedirs(_config_path, exist_ok=True)

    # -----------------------bash/zsh--------------------------------------
    _config_file_sh = os.path.join(_config_path, "easifemvar.sh")
    easifemrc = open(_config_file_sh, "w")
    # easifemrc.write("#!/bin/bash \n \n")
    easifemrc.write("\n")
    a = os.environ.get("EASIFEM_INSTALL_DIR")
    easifemrc.write(f"export EASIFEM_INSTALL_DIR={a} \n")
    a = os.environ.get("EASIFEM_BUILD_DIR")
    easifemrc.write(f"export EASIFEM_BUILD_DIR={a} \n")
    a = os.environ.get("EASIFEM_SOURCE_DIR")
    easifemrc.write(f"export EASIFEM_SOURCE_DIR={a} \n")

    for key in _keys:
        a = os.environ.get(key)
        easifemrc.write(f"export {key}={a} \n")
        easifemrc.write(
            "export LD_LIBRARY_PATH=" + '"${LD_LIBRARY_PATH}:${' + f"{key}" + '}/lib"\n'
        )

    easifemrc.write(
        "export PKG_CONFIG_PATH="
        + '"${PKG_CONFIG_PATH}:${EASIFEM_EXTPKGS}/lib/pkgconfig"\n'
    )

    easifemrc.write("export PATH=" + '"${PATH}:${EASIFEM_EXTPKGS}/bin"\n')
    easifemrc.write("export PATH=" + '"${PATH}:${EASIFEM_APP}/bin"\n')

    easifemrc.close()

    # -----------------------fish--------------------------------------
    _config_file_fish = os.path.join(_config_path, "easifemvar.fish")
    easifemrc = open(_config_file_fish, "w")
    easifemrc.write("\n")
    a = os.environ.get("EASIFEM_INSTALL_DIR")
    easifemrc.write(f"set -gx EASIFEM_INSTALL_DIR {a} \n")
    a = os.environ.get("EASIFEM_BUILD_DIR")
    easifemrc.write(f"set -gx EASIFEM_BUILD_DIR {a} \n")
    a = os.environ.get("EASIFEM_SOURCE_DIR")
    easifemrc.write(f"set -gx EASIFEM_SOURCE_DIR {a} \n")
    for key in _keys:
        a = os.environ.get(key)
        easifemrc.write(f"set -gx {key} {a} \n")
        easifemrc.write(
            "set -gx LD_LIBRARY_PATH " + '$LD_LIBRARY_PATH $' + f"{key}" + '/lib\n'
        )
    easifemrc.write(
        "set -gx PKG_CONFIG_PATH $PKG_CONFIG_PATH $EASIFEM_EXTPKGS/lib/pkgconfig\n"
    )

    easifemrc.write("set -gx PATH $PATH $EASIFEM_EXTPKGS/bin\n")
    easifemrc.write("set -gx PATH $PATH $EASIFEM_APP/bin\n")

    easifemrc.close()

    console.print("\n Environment variables have been written in  ↓")
    console.print(Panel.fit(f"{_config_file_sh}\n\n" + f"{_config_file_fish}"))

    text = Text()
    text.append("\n🚀 Please perform the following task: ⤵\n\n", style="bold")
    text.append(
        "⊙ Check SHELL by using following command in terminal:\n\n",
        style="italic cyan",
    )
    text.append(
        "which $SHELL \n\n",
        style="bold magenta",
    )

    text.append(
        "◌ BASH: If SHELL is bash, then add following lines to ~/.bashrc\n\n",
        style="",
    )

    text.append(
        f"source {_config_file_sh}\n\n",
        style="underline",
    )

    text.append(
        "◌ ZSH: If SHELL is zsh, then add following lines to ~/.zshrc\n\n",
        style="",
    )

    text.append(
        f"source {_config_file_sh}\n\n",
        style="underline",
    )

    console.print(
        Panel(
            text,
            title="[bold red] Modify SHELL",
        )
    )
    # console.print(f"\n🚀 Please perform the following task: ⤵")
    # console.print(f"\n⊙ Check SHELL by using following command in terminal:\n")
    # console.rule("[bold red] which $SHELL")
    # console.print("\n🔨 If SHELL is bash, then add following lines to ~/.bashrc")
    # console.print(f"source {_config_file}")
    # console.print(f"\n🔨 If SHELL is zsh, then add following lines to ~/.zshrc")
    # console.print(f"source {_config_file}")
    # if shell in ["bash", "zsh"]:

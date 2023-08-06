import os
import shutil
from easifem.console import console
from rich.panel import Panel
from easifem.components import extpkgs as _extpkgs
from easifem.components import easifemlibs as _easifemlibs
from easifem.components import kernelslibs as _kernelslibs
from easifem.components import components as _components
from easifem.components import install as _build

#############################################################################
## easifem_install ##########################################################
#############################################################################


def easifem_uninstall(
    components,
    install=_build,
):

    if _build == "":
        console.print(Panel.fit("❌ ERROR"))
        console.print(f"Environment variable EASIFEM_INSTALL_DIR not found")
        console.print("Make sure you have sourced the easifemvar.sh(fish)")
        raise SystemExit(2)

    for c in components:
        console.print(f"Cleaning {c}", justify="left", style="bold green")
        if c in _components:
            if c == "all":
                easifem_uninstall(components=_extpkgs, install=_build)
                easifem_uninstall(components=_easifemlibs, install=_build)
                easifem_uninstall(components=_kernelslibs, install=_build)
            if c == "easifem":
                easifem_uninstall(components=_easifemlibs, install=_build)
            if c == "extpkgs":
                easifem_uninstall(components=_extpkgs, install=_build)
            if c == "kernels":
                easifem_uninstall(components=_kernelslibs, install=_build)
            elif c in _extpkgs:
                _clean(
                    install=_build if install == None else install,
                    pkg_name="extpkgs",
                )
            elif c == "base":
                _clean(
                    install=_build if install == None else install,
                    pkg_name="base",
                )

            elif c == "classes":
                _clean(
                    install=_build if install == None else install,
                    pkg_name="classes",
                )

            elif c == "materials":
                _clean(
                    install=_build if install == None else install,
                    pkg_name="materials",
                )

            elif c == "kernels":
                _clean(
                    install=_build if install == None else install,
                    pkg_name="kernels",
                )
            elif c in _kernelslibs:
                _clean(
                    install=_build if install == None else install,
                    pkg_name="kernels",
                )


#############################################################################
## classes ##################################################################
#############################################################################


def _clean(install, pkg_name):

    build_dir = os.path.join(install, "easifem", pkg_name)

    # def handler(func, path, exc_info):
    # console.print(f"{build_dir} cannot be removed")
    # console.print(exc_info)

    shutil.rmtree(build_dir, ignore_errors=True)

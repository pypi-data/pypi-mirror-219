import os
import shutil
from easifem.console import console
from rich.panel import Panel

_extpkgs = ["openblas", "lapack95", "sparsekit", "fftw", "superlu", "arpack", "lis"]
_easifemlibs = ["base", "classes", "materials", "kernels"]
_kernelslibs = ["elasticity"]

_components = ["extpkgs", "easifem", "all"] + _easifemlibs + _extpkgs + _kernelslibs

# _build0 = os.path.join(os.environ["HOME"], "temp")
# _install0 = os.environ["HOME"]
# _source0 = os.path.join(os.environ["HOME"], "code")
_build = os.getenv("EASIFEM_BUILD_DIR", "")


#############################################################################
## easifem_install ##########################################################
#############################################################################


def easifem_clean(
    components,
    build=_build,
):

    if _build == "":
        console.print(Panel.fit("❌ ERROR"))
        console.print(f"Environment variable EASIFEM_BUILD_DIR not found")
        console.print("Make sure you have sourced the easifemvar.sh(fish)")
        raise SystemExit(2)

    for c in components:
        console.print(f"Cleaning {c}", justify="left", style="bold green")
        if c in _components:
            if c == "all":
                easifem_clean(components=_extpkgs, build=_build)
                easifem_clean(components=_easifemlibs, build=_build)
                easifem_clean(components=_kernelslibs, build=_build)
            if c == "easifem":
                easifem_clean(components=_easifemlibs, build=_build)
            if c == "extpkgs":
                easifem_clean(components=_extpkgs, build=_build)
            elif c == "lapack95":
                _clean(
                    build=_build if build == None else build,
                    pkg_name=os.path.join("extpkgs", "LAPACK95"),
                )
            elif c == "sparsekit":
                _clean(
                    build=_build if build == None else build,
                    pkg_name=os.path.join("extpkgs", "Sparsekit"),
                )
            elif c == "superlu":
                _clean(
                    build=_build if build == None else build,
                    pkg_name=os.path.join("extpkgs", "superlu"),
                )
            elif c == "arpack":
                _clean(
                    build=_build if build == None else build,
                    pkg_name=os.path.join("extpkgs", "arpack-ng"),
                )
            elif c == "base":
                _clean(
                    build=_build if build == None else build,
                    pkg_name="base",
                )

            elif c == "classes":
                _clean(
                    build=_build if build == None else build,
                    pkg_name="classes",
                )

            elif c == "materials":
                _clean(
                    build=_build if build == None else build,
                    pkg_name="materials",
                )

            elif c == "kernels":
                _clean(
                    build=_build if build == None else build,
                    pkg_name="kernels",
                )
            elif c == "elasticity":
                _clean(
                    build=_build if build == None else build,
                    pkg_name="elasticity",
                )


#############################################################################
## classes ##################################################################
#############################################################################


def _clean(build, pkg_name):

    build_dir = os.path.join(build, "easifem", pkg_name, "build")

    # def handler(func, path, exc_info):
    # console.print(f"{build_dir} cannot be removed")
    # console.print(exc_info)

    shutil.rmtree(build_dir, ignore_errors=True)

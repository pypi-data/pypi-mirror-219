import os
import platform

# import sys
import shutil
import subprocess
from easifem.console import console
from rich.panel import Panel
from rich.text import Text
from distutils.ccompiler import new_compiler
from distutils.sysconfig import customize_compiler

# _easifem = "easifem"

_extpkgs = ["openblas", "lapack95", "sparsekit", "fftw", "superlu", "arpack", "lis"]

_components = ["extpkgs", "base", "classes", "materials", "kernels"] + _extpkgs

# _build0 = os.path.join(os.environ["HOME"], "temp")
# _install0 = os.environ["HOME"]
# _source0 = os.path.join(os.environ["HOME"], "code")
_build = os.getenv("EASIFEM_BUILD_DIR", "")
_install = os.getenv("EASIFEM_INSTALL_DIR", "")
_source = os.getenv("EASIFEM_SOURCE_DIR", "")

EASIFEM_EXTPKGS = os.getenv("EASIFEM_EXTPKGS", "")
EASIFEM_BASE = os.getenv("EASIFEM_BASE", "")
EASIFEM_CLASSES = os.getenv("EASIFEM_CLASSES", "")

#############################################################################
## easifem_install ##########################################################
#############################################################################


def easifem_install(
    components,
    quite=False,
    install=_install,
    build=_build,
    source=_source,
):

    if _build == "":
        console.print(Panel.fit("❌ ERROR"))
        console.print(f"Environment variable EASIFEM_BUILD_DIR not found")
        console.print("Make sure you have sourced the easifemvar.sh(fish)")
        raise SystemExit(2)

    if _install == "":
        console.print(Panel.fit("❌ ERROR"))
        console.print(f"Environment variable EASIFEM_INSTALL_DIR not found")
        console.print("Make sure you have sourced the easifemvar.sh(fish)")
        raise SystemExit(2)

    if _source == "":
        console.print(Panel.fit("❌ ERROR"))
        console.print(f"Environment variable EASIFEM_SOURCE_DIR not found")
        console.print("Make sure you have sourced the easifemvar.sh(fish)")
        raise SystemExit(2)

    if EASIFEM_EXTPKGS == "":
        console.print(Panel.fit("❌ ERROR"))
        console.print(f"Environment variable EASIFEM_EXTPKGS not found")
        console.print("Make sure you have sourced the easifemvar.sh(fish)")
        raise SystemExit(2)

    if EASIFEM_BASE == "":
        console.print(Panel.fit("❌ ERROR"))
        console.print(f"Environment variable EASIFEM_BASE not found")
        console.print("Make sure you have sourced the easifemvar.sh(fish)")
        raise SystemExit(2)

    if EASIFEM_CLASSES == "":
        console.print(Panel.fit("❌ ERROR"))
        console.print(f"Environment variable EASIFEM_CLASSES not found")
        console.print("Make sure you have sourced the easifemvar.sh(fish)")
        raise SystemExit(2)

    for c in components:
        if c in _components:
            console.print(f"\n", justify="left", style="bold green underline")
            console.print(f"\n\nInstalling {c}\n", justify="left", style="bold green")
            console.print(f"\n", justify="left", style="bold green underline")
            if c == "extpkgs":
                _install_extpkgs(
                    quite=quite,
                    install=_install if install == None else install,
                    build=_build if build == None else build,
                    source=_source if source == None else source,
                )
            if c == "openblas":
                _install_openblas(
                    quite=quite,
                    install=_install if install == None else install,
                    build=_build if build == None else build,
                    source=_source if source == None else source,
                )
            elif c == "lapack95":
                _install_lapack95(
                    quite=quite,
                    install=_install if install == None else install,
                    build=_build if build == None else build,
                    source=_source if source == None else source,
                )
            elif c == "sparsekit":
                _install_sparsekit(
                    quite=quite,
                    install=_install if install == None else install,
                    build=_build if build == None else build,
                    source=_source if source == None else source,
                )
            elif c == "fftw":
                _install_fftw(
                    quite=quite,
                    install=_install if install == None else install,
                    build=_build if build == None else build,
                    source=_source if source == None else source,
                )
            elif c == "superlu":
                _install_superlu(
                    quite=quite,
                    install=_install if install == None else install,
                    build=_build if build == None else build,
                    source=_source if source == None else source,
                )
            elif c == "arpack":
                _install_arpack(
                    quite=quite,
                    install=_install if install == None else install,
                    build=_build if build == None else build,
                    source=_source if source == None else source,
                )
            elif c == "lis":
                _install_lis(
                    quite=quite,
                    install=_install if install == None else install,
                    build=_build if build == None else build,
                    source=_source if source == None else source,
                )
            elif c == "base":
                _install_base(
                    quite=quite,
                    install=_install if install == None else install,
                    build=_build if build == None else build,
                    source=_source if source == None else source,
                )
            elif c == "classes":
                _install_classes(
                    quite=quite,
                    install=_install if install == None else install,
                    build=_build if build == None else build,
                    source=_source if source == None else source,
                )

        else:
            console.print(Panel.fit("❌ ERROR 2"))
            console.print(f"Component {c} cannot be installed\n")
            console.print(f"Currently, only {_components} can be installed\n")
            raise SystemExit(2)


#############################################################################
## runCommand ###############################################################
#############################################################################


def runCommand(cargs, quite=False):
    """
    This program runs a command,
    cargs[0] will change on return
    """
    _temp = shutil.which(cargs[0])

    if _temp:
        cargs[0] = _temp.strip()
    else:
        console.print(Panel.fit("❌ ERROR 1"))
        console.print(f"{cargs[0]} not found on system PATH")
        raise SystemExit(2)

    if not quite:
        console.print(f"=> Calling {cargs[0]} with following args ...")
        console.print("=> " + " ".join(cargs))

    p = subprocess.run(
        cargs,
        shell=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=1000000,
        check=False,
        encoding="utf-8",
        errors="strict",
        text=True,
        universal_newlines=True,
    )

    if p.returncode != 0:
        console.print(Panel.fit("❌ ERROR 2"))
        console.print(f"Command {cargs[0]} Failed with following message:\n")
        console.print("=> " + p.stdout)
        console.print("=> " + p.stderr)
        raise SystemExit(2)
    else:
        if not quite:
            console.print(Panel.fit("✔️R SUCCESS"))
            console.print(f"  {id} => command {cargs[0]} was successful")
            console.print(f"\n {id} => Command output: \n")
            console.print(p.stdout)


#############################################################################
## extpkgs ##################################################################
#############################################################################


def _install_extpkgs(quite, install, build, source):
    easifem_install(
        components=_extpkgs,
        quite=quite,
        install=install,
        build=build,
        source=source,
    )


#############################################################################
##  openblas ################################################################
#############################################################################


def _install_openblas(quite, install, build, source):
    print(quite, install, build, source)
    console.print("openblas is Currently not avaiable!")


#############################################################################
## lapack95 #################################################################
#############################################################################


def _install_lapack95(quite, install, build, source):
    pkg_dir = os.path.join(source, "easifem", "extpkgs")
    pkg_name = "LAPACK95"
    pkg_with_path = os.path.join(pkg_dir, pkg_name)
    url = "https://github.com/vickysharma0812/" + pkg_name + ".git"
    cmake_def = []
    cmake_def.append("-D USE_OpenMP:BOOL=ON")
    cmake_def.append("-D CMAKE_BUILD_TYPE:STRING=Release")
    cmake_def.append("-D BUILD_SHARED_LIBS:BOOL=ON")
    cmake_def.append(f"-D CMAKE_INSTALL_PREFIX:PATH={EASIFEM_EXTPKGS}")

    build_dir = os.path.join(build, "easifem", "extpkgs", pkg_name, "build")

    cwd = os.getcwd()

    if os.path.exists(pkg_with_path):
        os.chdir(pkg_with_path)
        cargs = ["git", "pull"]
        runCommand(cargs=cargs, quite=quite)
        # os.system(f"git pull")
    else:
        console.print(f"Path {pkg_with_path} does not exist.")
        console.print(f"Creating {pkg_with_path}")
        cargs = ["git", "clone", f"{url}", f"{pkg_with_path}"]
        runCommand(cargs=cargs, quite=quite)
        # os.system(f"git clone {url} {pkg_with_path}")
        os.chdir(pkg_with_path)

    os.makedirs(build_dir, exist_ok=True)

    os.makedirs(EASIFEM_EXTPKGS, exist_ok=True)
    os.makedirs(os.path.join(EASIFEM_EXTPKGS, "include"), exist_ok=True)
    os.makedirs(os.path.join(EASIFEM_EXTPKGS, "lib"), exist_ok=True)
    os.makedirs(os.path.join(EASIFEM_EXTPKGS, "bin"), exist_ok=True)
    os.makedirs(os.path.join(EASIFEM_EXTPKGS, "share"), exist_ok=True)
    cargs = [
        "cmake",
        "-G",
        "Ninja",
        "-S",
        f"{pkg_with_path}",
        "-B",
        f"{build_dir}",
    ] + cmake_def

    runCommand(cargs=cargs, quite=quite)
    cargs = [
        "cmake",
        "--build",
        f"{build_dir}",
        "--target",
        "install",
    ]
    runCommand(cargs=cargs, quite=quite)
    # os.system(f"cmake -S ./ -B {build_dir} {cmake_def}")
    # os.system(f"cmake --build {build_dir} --target install")

    text = Text()
    text.append(
        Text.assemble(
            ("Package Name: ", "bold yellow"),
            f"{pkg_name}\n",
        )
    )
    text.append(
        Text.assemble(
            ("Package URL: ", "bold yellow"),
            f"{url}\n",
        )
    )
    text.append(
        Text.assemble(
            ("Source Dir: ", "bold yellow"),
            f"{pkg_dir}\n",
        )
    )
    text.append(
        Text.assemble(
            ("Build Dir: ", "bold yellow"),
            f"{build_dir}\n",
        )
    )
    text.append(
        Text.assemble(
            ("Install Dir: ", "bold yellow"),
            f"{EASIFEM_EXTPKGS}\n",
        )
    )
    console.print(Panel(text, title=f"[red] {pkg_name} Info"))

    os.chdir(cwd)


#############################################################################
## sparsekit ################################################################
#############################################################################


def _install_sparsekit(quite, install, build, source):
    pkg_dir = os.path.join(source, "easifem", "extpkgs")
    pkg_name = "Sparsekit"
    pkg_with_path = os.path.join(pkg_dir, pkg_name)
    url = "https://github.com/vickysharma0812/" + pkg_name + ".git"

    cmake_def = []
    cmake_def.append("-D CMAKE_BUILD_TYPE:STRING=Release ")
    cmake_def.append("-D BUILD_SHARED_LIBS:BOOL=ON ")
    cmake_def.append(f"-D CMAKE_INSTALL_PREFIX:PATH={EASIFEM_EXTPKGS}")

    build_dir = os.path.join(build, "easifem", "extpkgs", pkg_name, "build")

    cwd = os.getcwd()

    if os.path.exists(pkg_with_path):
        os.chdir(pkg_with_path)
        cargs = ["git", "pull"]
        runCommand(cargs=cargs, quite=quite)
        # os.system(f"git pull")
    else:
        console.print(f"Path {pkg_with_path} does not exist.")
        console.print(f"Creating {pkg_with_path}")
        cargs = ["git", "clone", f"{url}", f"{pkg_with_path}"]
        runCommand(cargs=cargs, quite=quite)
        # os.system(f"git clone {url} {pkg_with_path}")
        os.chdir(pkg_with_path)

    os.makedirs(build_dir, exist_ok=True)
    os.makedirs(EASIFEM_EXTPKGS, exist_ok=True)
    os.makedirs(os.path.join(EASIFEM_EXTPKGS, "include"), exist_ok=True)
    os.makedirs(os.path.join(EASIFEM_EXTPKGS, "lib"), exist_ok=True)
    os.makedirs(os.path.join(EASIFEM_EXTPKGS, "bin"), exist_ok=True)
    os.makedirs(os.path.join(EASIFEM_EXTPKGS, "share"), exist_ok=True)
    cargs = [
        "cmake",
        "-G",
        "Ninja",
        "-S",
        f"{pkg_with_path}",
        "-B",
        f"{build_dir}",
    ] + cmake_def

    runCommand(cargs=cargs, quite=quite)
    cargs = [
        "cmake",
        "--build",
        f"{build_dir}",
        "--target",
        "install",
    ]
    runCommand(cargs=cargs, quite=quite)
    # os.system(f"cmake -S ./ -B {build_dir} {cmake_def}")
    # os.system(f"cmake --build {build_dir} --target install")

    text = Text()
    text.append(
        Text.assemble(
            ("Package Name: ", "bold yellow"),
            f"{pkg_name}\n",
        )
    )
    text.append(
        Text.assemble(
            ("Package URL: ", "bold yellow"),
            f"{url}\n",
        )
    )
    text.append(
        Text.assemble(
            ("Source Dir: ", "bold yellow"),
            f"{pkg_dir}\n",
        )
    )
    text.append(
        Text.assemble(
            ("Build Dir: ", "bold yellow"),
            f"{build_dir}\n",
        )
    )
    text.append(
        Text.assemble(
            ("Install Dir: ", "bold yellow"),
            f"{EASIFEM_EXTPKGS}\n",
        )
    )
    console.print(Panel(text, title=f"[red] {pkg_name} Info"))

    os.chdir(cwd)


#############################################################################
## fftw #####################################################################
#############################################################################


def _install_fftw(quite, install, build, source):
    pkg_dir = os.path.join(source, "easifem", "extpkgs")
    pkg_name = "fftw-3.3.10"
    pkg_with_path = os.path.join(pkg_dir, pkg_name)
    url = "https://www.fftw.org/fftw-3.3.10.tar.gz"
    compress_file = os.path.join(pkg_dir, "fftw.tar.gz")

    cwd = os.getcwd()

    if os.path.exists(pkg_with_path):
        os.chdir(pkg_with_path)
    else:
        if not os.path.isfile(compress_file):
            cargs = [
                "curl",
                "-L",
                url,
                "-o",
                compress_file,
            ]

        runCommand(cargs=cargs, quite=quite)
        cargs = [
            "tar",
            "-xf",
            compress_file,
            "-C",
            pkg_dir,
        ]
        runCommand(cargs=cargs, quite=quite)
        os.chdir(pkg_with_path)

    os.makedirs(EASIFEM_EXTPKGS, exist_ok=True)
    os.makedirs(os.path.join(EASIFEM_EXTPKGS, "include"), exist_ok=True)
    os.makedirs(os.path.join(EASIFEM_EXTPKGS, "lib"), exist_ok=True)
    os.makedirs(os.path.join(EASIFEM_EXTPKGS, "bin"), exist_ok=True)
    os.makedirs(os.path.join(EASIFEM_EXTPKGS, "share"), exist_ok=True)
    ccompiler = new_compiler()
    customize_compiler(ccompiler)
    print("platform.system = ", platform.system())
    print("c compiler: = ", ccompiler.compiler[0] )
    check_darwin = platform.system() == "Darwin" and  ccompiler.compiler[0] == "clang"

    if(check_darwin):
        cargs = [
            os.path.join(pkg_with_path, "configure"),
            "--prefix",
            EASIFEM_EXTPKGS, 
            "--disable-openmp"
        ]
    else:
        cargs = [
            os.path.join(pkg_with_path, "configure"),
            "--prefix",
            EASIFEM_EXTPKGS,
            "--enable-openmp",
        ]

    runCommand(cargs=cargs, quite=quite)
    cargs = [
        "make",
    ]
    runCommand(cargs=cargs, quite=quite)

    cargs = [
        "make",
        "install",
    ]
    runCommand(cargs=cargs, quite=quite)

    text = Text()
    text.append(
        Text.assemble(
            ("Package Name: ", "bold yellow"),
            f"{pkg_name}\n",
        )
    )
    text.append(
        Text.assemble(
            ("Package URL: ", "bold yellow"),
            f"{url}\n",
        )
    )
    text.append(
        Text.assemble(
            ("Source Dir: ", "bold yellow"),
            f"{pkg_dir}\n",
        )
    )
    text.append(
        Text.assemble(
            ("Install Dir: ", "bold yellow"),
            f"{EASIFEM_EXTPKGS}\n",
        )
    )
    console.print(Panel(text, title=f"[red] {pkg_name} Info"))

    os.chdir(cwd)


#############################################################################
## superlu ##################################################################
#############################################################################


def _install_superlu(quite, install, build, source):
    pkg_dir = os.path.join(source, "easifem", "extpkgs")
    pkg_name = "superlu"
    pkg_with_path = os.path.join(pkg_dir, pkg_name)
    url = "https://github.com/xiaoyeli/" + pkg_name + ".git"
    cmake_def = []
    cmake_def.append("-D CMAKE_BUILD_TYPE:STRING=Release")
    cmake_def.append("-D BUILD_SHARED_LIBS:BOOL=ON")
    cmake_def.append("-D TPL_ENABLE_METISLIB:BOOL=OFF")
    cmake_def.append(f"-D CMAKE_INSTALL_PREFIX:PATH={EASIFEM_EXTPKGS}")

    build_dir = os.path.join(build, "easifem", "extpkgs", pkg_name, "build")

    cwd = os.getcwd()

    if os.path.exists(pkg_with_path):
        os.chdir(pkg_with_path)
        cargs = ["git", "pull"]
        runCommand(cargs=cargs, quite=quite)
        # os.system(f"git pull")
    else:
        console.print(f"Path {pkg_with_path} does not exist.")
        console.print(f"Creating {pkg_with_path}")
        console.print(f"cloning {pkg_name} from git.")
        cargs = ["git", "clone", f"{url}", f"{pkg_with_path}"]
        runCommand(cargs=cargs, quite=quite)
        os.chdir(pkg_with_path)

    os.makedirs(build_dir, exist_ok=True)
    os.makedirs(EASIFEM_EXTPKGS, exist_ok=True)
    os.makedirs(os.path.join(EASIFEM_EXTPKGS, "include"), exist_ok=True)
    os.makedirs(os.path.join(EASIFEM_EXTPKGS, "lib"), exist_ok=True)
    os.makedirs(os.path.join(EASIFEM_EXTPKGS, "bin"), exist_ok=True)
    os.makedirs(os.path.join(EASIFEM_EXTPKGS, "share"), exist_ok=True)
    cargs = [
        "cmake",
        "-G",
        "Ninja",
        "-S",
        f"{pkg_with_path}",
        "-B",
        f"{build_dir}",
    ] + cmake_def

    runCommand(cargs=cargs, quite=quite)
    cargs = [
        "cmake",
        "--build",
        f"{build_dir}",
        "--target",
        "install",
    ]
    runCommand(cargs=cargs, quite=quite)
    # os.system(f"cmake -S ./ -B {build_dir} {cmake_def}")
    # os.system(f"cmake --build {build_dir} --target install")

    text = Text()
    text.append(
        Text.assemble(
            ("Package Name: ", "bold yellow"),
            f"{pkg_name}\n",
        )
    )
    text.append(
        Text.assemble(
            ("Package URL: ", "bold yellow"),
            f"{url}\n",
        )
    )
    text.append(
        Text.assemble(
            ("Source Dir: ", "bold yellow"),
            f"{pkg_dir}\n",
        )
    )
    text.append(
        Text.assemble(
            ("Build Dir: ", "bold yellow"),
            f"{build_dir}\n",
        )
    )
    text.append(
        Text.assemble(
            ("Install Dir: ", "bold yellow"),
            f"{EASIFEM_EXTPKGS}\n",
        )
    )
    console.print(Panel(text, title=f"[red] {pkg_name} Info"))

    os.chdir(cwd)


#############################################################################
## arpac ####################################################################
#############################################################################


def _install_arpack(quite, install, build, source):
    pkg_dir = os.path.join(source, "easifem", "extpkgs")
    pkg_name = "arpack-ng"
    pkg_with_path = os.path.join(pkg_dir, pkg_name)
    url = "https://github.com/opencollab/" + pkg_name + ".git"
    cmake_def = []
    cmake_def.append("-D MPI:BOOL=OFF")
    cmake_def.append("-D CMAKE_BUILD_TYPE:STRING=Release")
    cmake_def.append("-D BUILD_SHARED_LIBS:BOOL=ON")
    cmake_def.append(f"-D CMAKE_INSTALL_PREFIX:PATH={EASIFEM_EXTPKGS}")

    build_dir = os.path.join(build, "easifem", "extpkgs", pkg_name, "build")

    cwd = os.getcwd()

    if os.path.exists(pkg_with_path):
        os.chdir(pkg_with_path)
        cargs = ["git", "pull"]
        runCommand(cargs=cargs, quite=quite)
        # os.system(f"git pull")
    else:
        console.print(f"Path {pkg_with_path} does not exist.")
        console.print(f"Creating {pkg_with_path}")
        cargs = ["git", "clone", f"{url}", f"{pkg_with_path}"]
        runCommand(cargs=cargs, quite=quite)
        # os.system(f"git clone {url} {pkg_with_path}")
        os.chdir(pkg_with_path)

    os.makedirs(build_dir, exist_ok=True)
    os.makedirs(EASIFEM_EXTPKGS, exist_ok=True)
    os.makedirs(os.path.join(EASIFEM_EXTPKGS, "include"), exist_ok=True)
    os.makedirs(os.path.join(EASIFEM_EXTPKGS, "lib"), exist_ok=True)
    os.makedirs(os.path.join(EASIFEM_EXTPKGS, "bin"), exist_ok=True)
    os.makedirs(os.path.join(EASIFEM_EXTPKGS, "share"), exist_ok=True)
    cargs = [
        "cmake",
        "-G",
        "Ninja",
        "-S",
        f"{pkg_with_path}",
        "-B",
        f"{build_dir}",
    ] + cmake_def

    runCommand(cargs=cargs, quite=quite)
    cargs = [
        "cmake",
        "--build",
        f"{build_dir}",
        "--target",
        "install",
    ]
    runCommand(cargs=cargs, quite=quite)
    # os.system(f"cmake -S ./ -B {build_dir} {cmake_def}")
    # os.system(f"cmake --build {build_dir} --target install")

    text = Text()
    text.append(
        Text.assemble(
            ("Package Name: ", "bold yellow"),
            f"{pkg_name}\n",
        )
    )
    text.append(
        Text.assemble(
            ("Package URL: ", "bold yellow"),
            f"{url}\n",
        )
    )
    text.append(
        Text.assemble(
            ("Source Dir: ", "bold yellow"),
            f"{pkg_dir}\n",
        )
    )
    text.append(
        Text.assemble(
            ("Build Dir: ", "bold yellow"),
            f"{build_dir}\n",
        )
    )
    text.append(
        Text.assemble(
            ("Install Dir: ", "bold yellow"),
            f"{EASIFEM_EXTPKGS}\n",
        )
    )
    console.print(Panel(text, title=f"[red] {pkg_name} Info"))

    os.chdir(cwd)


#############################################################################
## lis ######################################################################
#############################################################################


def _install_lis(quite, install, build, source):
    pkg_dir = os.path.join(source, "easifem", "extpkgs")
    pkg_name = "lis"
    pkg_with_path = os.path.join(pkg_dir, pkg_name)
    url = "https://github.com/anishida/" + pkg_name + ".git"
    cmake_def = []
    cmake_def.append(f"--prefix={EASIFEM_EXTPKGS}")
    cmake_def.append("--enable-omp")
    cmake_def.append("--enable-f90")
    cmake_def.append("--enable-shared")
    cmake_def.append("--enable-saamg")
    ##cmake_def.append("FC=gfortran")
    # cmake_def.append("CC=gcc")

    cwd = os.getcwd()

    if os.path.exists(pkg_with_path):
        os.chdir(pkg_with_path)
        cargs = ["git", "pull"]
        runCommand(cargs=cargs, quite=quite)
        # os.system(f"git pull")
    else:
        console.print(f"Path {pkg_with_path} does not exist.")
        console.print(f"Creating {pkg_with_path}")
        cargs = ["git", "clone", f"{url}", f"{pkg_with_path}"]
        runCommand(cargs=cargs, quite=quite)
        # os.system(f"git clone {url} {pkg_with_path}")
        os.chdir(pkg_with_path)

    os.makedirs(EASIFEM_EXTPKGS, exist_ok=True)
    os.makedirs(os.path.join(EASIFEM_EXTPKGS, "include"), exist_ok=True)
    os.makedirs(os.path.join(EASIFEM_EXTPKGS, "lib"), exist_ok=True)
    os.makedirs(os.path.join(EASIFEM_EXTPKGS, "bin"), exist_ok=True)
    os.makedirs(os.path.join(EASIFEM_EXTPKGS, "share"), exist_ok=True)

    cargs = [
        os.path.join(pkg_with_path, "configure"),
    ] + cmake_def
    runCommand(cargs=cargs, quite=quite)

    cargs = ["make"]
    runCommand(cargs=cargs, quite=quite)

    cargs = ["make", "check"]
    runCommand(cargs=cargs, quite=quite)

    cargs = ["make", "install"]
    runCommand(cargs=cargs, quite=quite)

    cargs = ["make", "installcheck"]
    runCommand(cargs=cargs, quite=quite)

    text = Text()
    text.append(
        Text.assemble(
            ("Package Name: ", "bold yellow"),
            f"{pkg_name}\n",
        )
    )

    text.append(
        Text.assemble(
            ("Package URL: ", "bold yellow"),
            f"{url}\n",
        )
    )

    text.append(
        Text.assemble(
            ("Source Dir: ", "bold yellow"),
            f"{pkg_dir}\n",
        )
    )

    text.append(
        Text.assemble(
            ("Install Dir: ", "bold yellow"),
            f"{EASIFEM_EXTPKGS}\n",
        )
    )
    console.print(Panel(text, title=f"[red] {pkg_name} Info"))

    os.chdir(cwd)


#############################################################################
## blas #####################################################################
#############################################################################


def _install_base(quite, install, build, source):
    pkg_dir = os.path.join(source, "easifem")
    pkg_name = "base"
    pkg_with_path = os.path.join(pkg_dir, pkg_name)
    url = "https://github.com/vickysharma0812/easifem-base.git"
    cmake_def = []
    cmake_def.append("-D USE_OpenMP:BOOL=ON")
    cmake_def.append(f"-D CMAKE_INSTALL_PREFIX:PATH={EASIFEM_BASE}")
    cmake_def.append("-D CMAKE_BUILD_TYPE:STRING=Release")
    cmake_def.append("-D BUILD_SHARED_LIBS:BOOL=ON")
    cmake_def.append("-D USE_PLPLOT:BOOL=ON")
    cmake_def.append("-D USE_BLAS95:BOOL=ON")
    cmake_def.append("-D USE_LAPACK95:BOOL=ON")
    cmake_def.append("-D USE_FFTW:BOOL=ON")
    cmake_def.append("-D USE_GTK:BOOL=OFF")
    cmake_def.append("-D USE_ARPACK:BOOL=ON")
    cmake_def.append("-D USE_PARPACK:BOOL=OFF")
    cmake_def.append("-D USE_METIS:BOOL=OFF")
    cmake_def.append("-D USE_SUPERLU:BOOL=ON")
    cmake_def.append("-D USE_LIS:BOOL=ON")
    cmake_def.append("-D USE_Int32:BOOL=ON")
    cmake_def.append("-D USE_Real64:BOOL=ON")
    cmake_def.append("-D COLOR_DISP:BOOL=OFF")

    build_dir = os.path.join(build, "easifem", pkg_name, "build")

    cwd = os.getcwd()

    if os.path.exists(pkg_with_path):
        os.chdir(pkg_with_path)
        cargs = ["git", "pull"]
        runCommand(cargs=cargs, quite=quite)
    else:
        console.print(f"Path {pkg_with_path} does not exist.")
        console.print(f"Creating {pkg_with_path}")
        cargs = ["git", "clone", url, pkg_with_path]
        # cargs = ["gh", "repo", "clone", "vickysharma0812/easifem-base", pkg_with_path]
        runCommand(cargs=cargs, quite=quite)
        os.chdir(pkg_with_path)

    os.makedirs(build_dir, exist_ok=True)
    os.makedirs(EASIFEM_BASE, exist_ok=True)
    os.makedirs(os.path.join(EASIFEM_BASE, "include"), exist_ok=True)
    os.makedirs(os.path.join(EASIFEM_BASE, "lib"), exist_ok=True)
    os.makedirs(os.path.join(EASIFEM_BASE, "bin"), exist_ok=True)
    os.makedirs(os.path.join(EASIFEM_BASE, "share"), exist_ok=True)
    cargs = [
        "cmake",
        "-G",
        "Ninja",
        "-S",
        f"{pkg_with_path}",
        "-B",
        f"{build_dir}",
    ] + cmake_def

    runCommand(cargs=cargs, quite=quite)
    cargs = [
        "cmake",
        "--build",
        f"{build_dir}",
        "--target",
        "install",
    ]
    runCommand(cargs=cargs, quite=quite)

    text = Text()
    text.append(
        Text.assemble(
            ("Package Name: ", "bold yellow"),
            f"{pkg_name}\n",
        )
    )
    text.append(
        Text.assemble(
            ("Package URL: ", "bold yellow"),
            f"{url}\n",
        )
    )
    text.append(
        Text.assemble(
            ("Source Dir: ", "bold yellow"),
            f"{pkg_dir}\n",
        )
    )
    text.append(
        Text.assemble(
            ("Build Dir: ", "bold yellow"),
            f"{build_dir}\n",
        )
    )
    text.append(
        Text.assemble(
            ("Install Dir: ", "bold yellow"),
            f"{EASIFEM_BASE}\n",
        )
    )
    console.print(Panel(text, title=f"[red] {pkg_name} Info"))

    os.chdir(cwd)


#############################################################################
## classes ##################################################################
#############################################################################


def _install_classes(quite, install, build, source):
    pkg_dir = os.path.join(source, "easifem")
    pkg_name = "classes"
    pkg_with_path = os.path.join(pkg_dir, pkg_name)
    url = "https://github.com/vickysharma0812/easifem-classes.git"

    cmake_def = []
    cmake_def.append(f"-D CMAKE_INSTALL_PREFIX:PATH={EASIFEM_CLASSES}")
    cmake_def.append("-D CMAKE_BUILD_TYPE:STRING=Release")
    cmake_def.append("-D BUILD_SHARED_LIBS:BOOL=ON")
    cmake_def.append("-D USE_GMSH_SDK:BOOL=OFF")

    build_dir = os.path.join(build, "easifem", pkg_name, "build")

    cwd = os.getcwd()

    if os.path.exists(pkg_with_path):
        os.chdir(pkg_with_path)
        cargs = ["git", "pull"]
        runCommand(cargs=cargs, quite=quite)
    else:
        console.print(f"Path {pkg_with_path} does not exist.")
        console.print(f"Creating {pkg_with_path}")
        cargs = ["git", "clone", url, pkg_with_path]
        # cargs = [
        #     "gh",
        #     "repo",
        #     "clone",
        #     "vickysharma0812/easifem-classes",
        #     pkg_with_path,
        # ]
        runCommand(cargs=cargs, quite=quite)
        os.chdir(pkg_with_path)

    os.makedirs(build_dir, exist_ok=True)
    os.makedirs(EASIFEM_CLASSES, exist_ok=True)
    os.makedirs(os.path.join(EASIFEM_CLASSES, "include"), exist_ok=True)
    os.makedirs(os.path.join(EASIFEM_CLASSES, "lib"), exist_ok=True)
    os.makedirs(os.path.join(EASIFEM_CLASSES, "bin"), exist_ok=True)
    os.makedirs(os.path.join(EASIFEM_CLASSES, "share"), exist_ok=True)
    cargs = [
        "cmake",
        "-G",
        "Ninja",
        "-S",
        f"{pkg_with_path}",
        "-B",
        f"{build_dir}",
    ] + cmake_def

    runCommand(cargs=cargs, quite=quite)
    cargs = [
        "cmake",
        "--build",
        build_dir,
        "--target",
        "install",
    ]
    runCommand(cargs=cargs, quite=quite)

    text = Text()
    text.append(
        Text.assemble(
            ("Package Name: ", "bold yellow"),
            f"{pkg_name}\n",
        )
    )
    text.append(
        Text.assemble(
            ("Package URL: ", "bold yellow"),
            f"{url}\n",
        )
    )
    text.append(
        Text.assemble(
            ("Source Dir: ", "bold yellow"),
            f"{pkg_dir}\n",
        )
    )
    text.append(
        Text.assemble(
            ("Build Dir: ", "bold yellow"),
            f"{build_dir}\n",
        )
    )
    text.append(
        Text.assemble(
            ("Install Dir: ", "bold yellow"),
            f"{EASIFEM_EXTPKGS}\n",
        )
    )
    console.print(Panel(text, title=f"[red] {pkg_name} Info"))

    os.chdir(cwd)

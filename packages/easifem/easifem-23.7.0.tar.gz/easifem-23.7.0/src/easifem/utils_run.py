from pathlib import Path
import shutil
import subprocess
import os
from easifem.cmake import cmakeListBase
from easifem.console import console, print
from rich.panel import Panel
from rich.table import Column
from rich.progress import Progress, BarColumn, TextColumn


def _actOnFile(input: str, check=True):
    """
    ⁃ Absolute path parent : /home/easifem/Dropbox/easifem/easifem-docs/apps/python/test/
    ⁃ Absolute path        : /home/easifem/Dropbox/easifem/easifem-docs/apps/python/test/hello
    ⁃ File basename        : hello.F90
    ⁃ File ext             : .F90
    """

    path = Path(input)

    if check:
        if not path.is_file():
            print(
                """
                --file is not a file, it must be a file, 
                Also, make sure it exists
                """
            )
            raise SystemExit(2)

    # make path absolute

    absPath = path.absolute()

    return (
        str(absPath.parent),
        str(absPath.parent.joinpath(absPath.stem)),
        absPath.name,
        absPath.suffix,
    )


def runCommand(cargs, quite=False, id: str = "", lastOutput=False):
    """
    This program runs a command,
    cargs[0] will change on return
    """
    _temp = shutil.which(cargs[0])

    if _temp:
        cargs[0] = _temp.strip()
    else:
        console.print(Panel.fit(" ERROR 1"))
        console.print(f" {id} {cargs[0]} not found on system PATH")
        raise SystemExit(2)

    if not quite:
        console.print(f"=> Calling {cargs[0]} with following args ...")
        console.print("=> " + " ".join(cargs))

    p = subprocess.run(
        cargs,
        shell=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=100,
        check=False,
        encoding="utf-8",
        errors="strict",
        text=True,
        universal_newlines=True,
    )

    if p.returncode != 0:
        console.print(Panel.fit(" ERROR 2"))
        console.print(f" {id} command {cargs[0]} Failed with following message:\n")
        console.print("=> " + p.stdout)
        console.print("=> " + p.stderr)
        raise SystemExit(2)
    else:
        if not quite:
            console.print(Panel.fit("✔️R SUCCESS"))
            console.print(f"  {id} => command {cargs[0]} was successful")
            console.print(f"\n {id} => Command output: \n")
            console.print(p.stdout)
        else:
            if lastOutput:
                console.print(Panel.fit("✔️R SUCCESS"))
                console.print(f"\n {id} => Command output: \n")
                console.print(p.stdout)


def _makeEasifemLibsTree(easifemLibs):
    """
    Dependencies among easifem components
    """
    if easifemLibs == "easifemBase":
        return ("easifemBase",)
    elif easifemLibs == "easifemClasses":
        return ("easifemClasses",)
    elif easifemLibs == "easifemMaterials":
        return (
            "easifemBase",
            "easifemClasses",
            "easifemMaterials",
        )
    elif easifemLibs == "easifemKernels":
        return (
            "easifemBase",
            "easifemClasses",
            "easifemMaterials",
            "easifemKernels",
        )
    elif easifemLibs == "StokesFlow":
        return (
            "easifemBase",
            "easifemClasses",
            "easifemMaterials",
            "easifemKernels",
            "StokesFlow",
        )
    elif easifemLibs == "MovingMesh":
        return (
            "easifemBase",
            "easifemClasses",
            "easifemMaterials",
            "easifemKernels",
            "MovingMesh",
        )
    else:
        raise ValueError(
            f"Given easifemLibs {easifemLibs} not supported, yet! Please use easifemBase, easifemClasses"
        )


def _makeExtpkgs(easifemLibs):
    """
    Dependencies of easifem components on external libs
    """
    # return ""
    return (
        "LAPACK95",
        "Sparsekit",
        "arpackng",
        "OpenMP",
    )


def easifem_run(
    file: str,
    quite=False,
    targetName="test",
    projectName="easifemApp",
    easifemLibs="easifemBase",
    buildPath=os.environ["HOME"] + "/temp/tests/build/",
    installPrefix=".",
):
    inputAbsParent, inputAbsPath, inputFileBase, inputFileExt = _actOnFile(file)

    if not quite:
        console.print(f"\n=> Following properties of input file {file} is used: ")
        console.print(f"=> Absolute parent: {inputAbsParent}")
        console.print(f"=> Absolute path  : {inputAbsPath}")
        console.print(f"=> File basename  : {inputFileBase}")
        console.print(f"=> File ext       : {inputFileExt}\n")

    progress = Progress(
        TextColumn("{task.description}", table_column=Column(ratio=1)),
        BarColumn(bar_width=None, table_column=Column(ratio=2)),
        expand=False,
        console=console,
        refresh_per_second=5,
        transient=False,
    )

    with progress:
        if inputFileExt == ".md":

            console.print(Panel.fit(" Markdown File Detected"))

            _actOnMdFile(
                inputAbsPath,
                projectName,
                targetName,
                quite,
                _makeEasifemLibsTree(easifemLibs),
                buildPath,
                installPrefix,
                progress,
            )

            # easifem test is used for testing development only
            # I keep tests generated from the markdown parser in
            # $EASIFEM_TEST_DIR
            # for testing I use installPrefix = "*--testing--*" as wild flag
            # all other values of installPrefix options will build in
            # the parent director of markdown or source file

        elif inputFileExt in [".F90", ".f90", ".f95", ".f"]:

            console.print(Panel.fit(" Fortran File Detected"))

            _actOnFortranFile(
                inputAbsPath,
                projectName,
                targetName,
                quite,
                _makeEasifemLibsTree(easifemLibs),
                buildPath,
                installPrefix,
                progress,
            )

        else:
            console.print(
                f"""
                unrecognized file extension in {inputFileExt}, should be md, F90, f90"
                """
            )
            raise SystemExit(1)


def _actOnF90File(
    outputAbsParent,
    outputAbsPath,
    outputFileBase,
    installPrefix,
    buildPath,
    targetName,
    projectName,
    easifemLibs,
    quite,
    progress,
    job,
):
    _cmakeFile = os.path.join(outputAbsParent, "CMakeLists.txt")
    cmakeFile = open(_cmakeFile, "w")
    srcPath = outputAbsParent

    for line in cmakeListBase(
        projectName=projectName,
        srcPath=srcPath,
        targetName=targetName,
        easifemLibs=easifemLibs,
        extLibs=(
            "LAPACK95",
            "Sparsekit",
            "arpackng",
            "OpenMP",
        ),
    ):
        cmakeFile.write(line + "\n")

    cmakeFile.close()

    # Go to TESTDir and Depending upon TESTDir
    # If installPrefix is *--testing--* then
    # we go to EASIFEM_TEST_DIR/parent/ and run the test
    #
    if installPrefix == "*--testing--*":
        testDir = os.environ["EASIFEM_TEST_DIR"]
        if not testDir:
            console.print(f" {id} Error env variable EASIFEM_TEST_DIR not found:\n")
            raise SystemExit(2)
        else:
            #
            # Update outputAbsParent outputAbsPath
            #
            _outputAbsParent = outputAbsParent + ""
            outputAbsParent = os.path.join(testDir, Path(outputAbsParent).stem)
            os.makedirs(outputAbsParent, exist_ok=True)
            os.rename(_cmakeFile, os.path.join(outputAbsParent, "CMakeLists.txt"))

            outputAbsPath = os.path.join(outputAbsParent, Path(outputFileBase).stem)
            os.rename(
                os.path.join(_outputAbsParent, outputFileBase),
                os.path.join(outputAbsParent, outputFileBase),
            )
    cwd = os.getcwd()
    os.chdir(outputAbsParent)

    if os.path.exists(buildPath):
        if not quite:
            console.print(f"  Found {buildPath}, removing it")
        shutil.rmtree(buildPath)

    cargs = [
        "cmake",
        "-G",
        "Ninja",
        "-B",
        buildPath,
        f"-DFILE={outputAbsPath}.F90",
    ]

    runCommand(cargs, quite=quite, id="Config App")
    # progress.advance(job)
    #
    # Command
    #
    cargs = [
        "cmake",
        "--build",
        buildPath,
    ]

    runCommand(cargs, quite=quite, id="Building App")

    progress.advance(job)
    #
    # Command
    #
    cargs = [os.path.join(buildPath, targetName)]
    runCommand(cargs, quite=True, id="Running App", lastOutput=True)

    progress.advance(job)
    #
    # console.save_svg(
    #     path=os.path.join(outputAbsParent, targetName) + ".svg",
    #     title=targetName,
    # )
    console.save_text(
        path=os.path.join(outputAbsParent, targetName) + ".txt",
        styles=False,
    )

    os.chdir(cwd)

    progress.advance(job)


def _actOnMdFile(
    inputAbsPath: str,
    projectName: str,
    targetName: str,
    quite: bool,
    easifemLibs: str,
    buildPath: str,
    installPrefix: str,
    progress,
):

    """
    Parse markdown file and run the app
    """

    job = progress.add_task("[red]" + targetName, total=5)

    outputAbsParent, outputAbsPath, outputFileBase, outputFileExt = _actOnFile(
        inputAbsPath + ".F90",
        check=False,
    )
    progress.advance(job)

    cargs = ["md2src", "-i", inputAbsPath.strip() + ".md"]

    if not quite:
        console.print(f"\n=> Following source file will be generated:")
        console.print(f"=> Absolute path: ", outputAbsPath + outputFileExt)
        console.print(" Calling md2src with following args ...")
        console.print("=> " + "".join(cargs))

    runCommand(cargs, quite=quite, id="(Parsing  )")

    progress.advance(job)

    _actOnF90File(
        outputAbsParent,
        outputAbsPath,
        outputFileBase,
        installPrefix,
        buildPath,
        targetName,
        projectName,
        easifemLibs,
        quite,
        progress,
        job,
    )


def _actOnFortranFile(
    inputAbsPath: str,
    projectName: str,
    targetName: str,
    quite: bool,
    easifemLibs: str,
    buildPath: str,
    installPrefix: str,
    progress,
):
    job = progress.add_task("[red]" + targetName, total=5)

    outputAbsParent, outputAbsPath, outputFileBase, outputFileExt = _actOnFile(
        inputAbsPath + ".F90",
        check=False,
    )
    progress.advance(job)

    _actOnF90File(
        outputAbsParent,
        outputAbsPath,
        outputFileBase,
        installPrefix,
        buildPath,
        targetName,
        projectName,
        easifemLibs,
        quite,
        progress,
        job,
    )

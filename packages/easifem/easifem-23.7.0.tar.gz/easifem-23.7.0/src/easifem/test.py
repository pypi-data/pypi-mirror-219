def parser(subparser):

    ans = subparser.add_parser(
        "test",
        help="Run an app build using easifem components, easifemBase, easifemClasses",
        description="""
        The [test] subcommand compiles and links an application, which is build
        by using easifem components, such as, easifemBase, easifemClasses, etc.
        This program can also PARSE a fortran code kept in the code-fences of 
        markdown file with extension [.md]
        The example of code fence which can be used in the markdown file is given below.

        ---- markdown file hello.md ---

        ```fortran
            program main
            use easifemBase
        ```

        Any thing outside fortran code fence will be ignored by the parser.

        Also you can use as many fences as you want, good for Documentation.

        ```fortran
            call display("Hello world")
            end program main
        ```

        To run this file  you can use:

        python3 easifem.py -f hello.md
        """,
    )

    ans.add_argument(
        "-f",
        "--file",
        help="Input filename, e.g. foo.md, ./foo.md, /path/to/foo.md",
    )

    ans.add_argument(
        "-q",
        "--quite",
        help="If specified lesser output will be printed",
        action="store_true",
    )

    ans.add_argument(
        "-t",
        "--target",
        help="Target name, optional[test]",
        required=False,
    )

    ans.add_argument(
        "-e",
        "--easifem_libs",
        help="EASIFEM application library used to build, choices, [easifemBase, easifemClasses, easifemMaterials, easifemKernels, StokesFlow]",
        required=False,
        choices=[
            "easifemBase",
            "easifemClasses",
            "easifemMaterials",
            "easifemKernels",
            "StokesFlow",
            "MovingMesh",
        ],
    )

    ans.add_argument(
        "--prefix",
        help="""
        Install location of source file generated from the markdown parser (md2src). The program will be run from this location. Default is parent directory of markdown file. 
        """,
        required=False,
    )

    return ans

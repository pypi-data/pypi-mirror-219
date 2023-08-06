import os

extpkgs = ["openblas", "lapack95", "sparsekit", "fftw", "superlu", "arpack", "lis"]
easifemlibs = ["base", "classes", "materials", "kernels"]
kernelslibs = ["elasticity"]
components = ["extpkgs", "easifem", "all"] + easifemlibs + extpkgs + kernelslibs
build = os.getenv("EASIFEM_BUILD_DIR", "")
install = os.getenv("EASIFEM_INSTALL_DIR", "")

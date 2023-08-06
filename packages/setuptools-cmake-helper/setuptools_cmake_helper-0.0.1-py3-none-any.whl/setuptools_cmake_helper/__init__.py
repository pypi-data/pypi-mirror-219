import os
import platform
import re
import subprocess
import sys
from distutils.command.build_ext import build_ext
from pathlib import Path

from setuptools import Extension

is_windows = platform.system() == "Windows"


class CMakeExtension(Extension):
    def __init__(self, name, sources, cmake_options, *args, **kw):
        super().__init__(name, sources, *args, **kw)
        cmake_options["dir"] = os.fspath(Path(cmake_options["dir"]).resolve())
        self.cmake_options = cmake_options


class CMakeBuild(build_ext):
    def run(self):
        try:
            out = subprocess.run(
                ["cmake", "--version"], stdout=subprocess.PIPE, check=True, text=True
            )
        except (FileNotFoundError, subprocess.CalledProcessError):
            raise RuntimeError(
                "CMake must be installed to build the following extensions: "
                + ", ".join(e.name for e in self.extensions)
            )

        if is_windows:
            cmake_version = tuple(
                int(d)
                for d in re.search(r"version\s*([\d.]+)", out.stdout)
                .group(1)
                .split(".")
            )
            if cmake_version < (3, 26, 2):
                raise RuntimeError("CMake >= 3.1.0 is required on Windows")

        super().run()

    def build_extension(self, ext):
        cmake_options = ext.cmake_options
        extdir = Path(self.get_ext_fullpath(ext.name)).parent.resolve()
        cmake_args = [
            f"-DCMAKE_ARCHIVE_OUTPUT_DIRECTORY={extdir}",
            f"-DPYTHON_EXECUTABLE={sys.executable}",
            "-DCMAKE_POSITION_INDEPENDENT_CODE=YES",
        ]
        library_output_dir = extdir

        cfg = "Debug" if self.debug else "Release"
        build_args = ["--config", cfg]
        if self.verbose:
            build_args.append("--verbose")

        if is_windows:
            cmake_args += [f"-DCMAKE_ARCHIVE_OUTPUT_DIRECTORY_{cfg.upper()}={extdir}"]
            if sys.maxsize > 2**32:
                cmake_args += ["-A", "x64"]
            build_args += ["--", "/m", "/verbosity:minimal"]
            library_name_format = "{}.lib"
        else:
            cmake_args += ["-DCMAKE_BUILD_TYPE=" + cfg]
            build_args += ["--", "-j2"]
            library_name_format = "lib{}.a"

        env = os.environ.copy()
        env["CXXFLAGS"] = '{} -DVERSION_INFO=\\"{}\\"'.format(
            env.get("CXXFLAGS", ""), self.distribution.get_version()
        )
        Path(self.build_temp).mkdir(parents=True, exist_ok=True)

        subprocess.run(
            ["cmake", cmake_options["dir"]] + cmake_args,
            cwd=self.build_temp,
            env=env,
            check=True,
        )
        if self.force:
            subprocess.run(
                ["cmake", "--build", ".", "--target", "clean"] + build_args,
                cwd=self.build_temp,
                check=True,
            )

        for target, target_output in cmake_options["targets"].items():
            if self.verbose:
                print(["cmake", "--build", ".", "--target", target] + build_args)
            subprocess.run(
                ["cmake", "--build", ".", "--target", target] + build_args,
                cwd=self.build_temp,
                check=True,
            )

            ext.extra_objects.append(
                os.fspath(
                    library_output_dir.joinpath(library_name_format.format(target))
                )
            )

        super().build_extension(ext)

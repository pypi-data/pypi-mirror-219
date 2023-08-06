from pathlib import Path

import build

simple_cpp_path = Path(__file__).parent.joinpath("test_package_simple_cpp")


def test_something(tmp_path):
    builder = build.ProjectBuilder(simple_cpp_path)
    builder.build("wheel", tmp_path)

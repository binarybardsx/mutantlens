from pathlib import PurePath

import pytest

from mutantlens.mutate.scope import is_test_file


@pytest.mark.parametrize(
    "path",
    [
        "test_shapes.py",
        "shapes_test.py",
        "conftest.py",
        "tests/shapes.py",
        "pkg/tests/helpers.py",
        "test/helpers.py",
    ],
)
def test_test_files_are_recognised(path: str) -> None:
    assert is_test_file(PurePath(path))


@pytest.mark.parametrize(
    "path", ["shapes.py", "pkg/core.py", "pkg/contest.py", "latest.py", "attests/a.py"]
)
def test_other_files_are_not(path: str) -> None:
    assert not is_test_file(PurePath(path))

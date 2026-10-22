from pathlib import PurePath

_TEST_DIRS = {"test", "tests"}


def is_test_file(path: PurePath) -> bool:
    """True for files that hold tests, which are never mutated.

    `path` should be relative to the project root, so that a project that
    lives inside a folder called "tests" is not skipped as a whole.
    """
    name = path.name
    return (
        name.startswith("test_")
        or name.endswith("_test.py")
        or name == "conftest.py"
        or any(part in _TEST_DIRS for part in path.parts[:-1])
    )

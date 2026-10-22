from pathlib import Path

import pytest

from mutantlens import __version__
from mutantlens.cli import main


def test_version_flag(capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit) as exit_info:
        main(["--version"])
    assert exit_info.value.code == 0
    assert capsys.readouterr().out.strip() == f"mutantlens {__version__}"


def test_assess_prints_mutant_counts_per_operator(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    (tmp_path / "shapes.py").write_text("def f(a, b):\n    return a + b > 3\n")
    (tmp_path / "test_shapes.py").write_text("def test_f():\n    assert 1 + 1 > 1\n")
    (tmp_path / "broken.py").write_text("def broken(:\n")
    (tmp_path / "tests").mkdir()
    (tmp_path / "tests" / "helpers.py").write_text("x = 1 + 2\n")

    assert main(["assess", str(tmp_path)]) == 0

    out = capsys.readouterr().out
    assert "files: 1 scanned, 2 test files skipped, 1 could not be read" in out
    assert "  arithmetic_replace   1\n" in out
    assert "  comparison_boundary  1\n" in out
    assert "  constant_replace     1\n" in out
    assert "  return_replace       1\n" in out
    assert "  boolean_replace      0\n" in out
    assert "total mutants: 4" in out
    assert "skipped as invalid syntax: 0" in out
    assert "tests are not run yet" in out


def test_assess_accepts_a_single_file(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    file = tmp_path / "one.py"
    file.write_text("ok = a and b\n")
    assert main(["assess", str(file)]) == 0
    out = capsys.readouterr().out
    assert "files: 1 scanned" in out
    assert "  boolean_replace      1\n" in out


def test_assess_never_writes_to_the_project(tmp_path: Path) -> None:
    file = tmp_path / "shapes.py"
    file.write_text("x = a > b\n")
    before = file.read_bytes()
    main(["assess", str(tmp_path)])
    assert file.read_bytes() == before
    assert sorted(p.name for p in tmp_path.iterdir()) == ["shapes.py"]


def test_assess_reports_a_missing_path_without_raising(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    assert main(["assess", str(tmp_path / "nope")]) == 2
    assert "path not found" in capsys.readouterr().err

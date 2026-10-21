import pytest

from mutantlens import __version__
from mutantlens.cli import main


def test_version_flag(capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit) as exit_info:
        main(["--version"])
    assert exit_info.value.code == 0
    assert capsys.readouterr().out.strip() == f"mutantlens {__version__}"


def test_assess_is_a_stub(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["assess", "toy/"]) == 0
    assert capsys.readouterr().out.strip() == "not implemented"

from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

import libcst as cst

from mutantlens.mutate.find import scan
from mutantlens.mutate.operators import ALL_OPERATORS
from mutantlens.mutate.scope import is_test_file

_SKIPPED_DIRS = {"__pycache__", "build", "dist"}


@dataclass
class Survey:
    """What `assess` found in a project. Mutants are only listed, not run yet."""

    scanned: int = 0
    test_files_skipped: int = 0
    unreadable: int = 0
    by_operator: Counter[str] = field(default_factory=Counter[str])
    skipped_invalid: int = 0


def _python_files(root: Path) -> list[Path]:
    if root.is_file():
        return [root]
    return sorted(
        p
        for p in root.rglob("*.py")
        if not any(
            part.startswith(".") or part in _SKIPPED_DIRS
            for part in p.relative_to(root).parts[:-1]
        )
    )


def survey(path: Path) -> Survey:
    root = path if path.is_dir() else path.parent
    result = Survey()
    for file in _python_files(path):
        if is_test_file(file.relative_to(root)):
            result.test_files_skipped += 1
            continue
        try:
            found = scan(file.read_text(encoding="utf-8"))
        except (cst.ParserSyntaxError, UnicodeDecodeError):
            result.unreadable += 1
            continue
        result.scanned += 1
        result.by_operator.update(m.operator for m in found.mutants)
        result.skipped_invalid += found.skipped_invalid
    return result


def format_survey(path: Path, result: Survey) -> str:
    width = max(len(op.id) for op in ALL_OPERATORS)
    lines = [
        f"mutantlens assess {path}",
        f"files: {result.scanned} scanned, {result.test_files_skipped} test files "
        f"skipped, {result.unreadable} could not be read or parsed",
        "mutants by operator:",
    ]
    for op in sorted(ALL_OPERATORS, key=lambda o: o.id):
        lines.append(f"  {op.id:<{width}}  {result.by_operator[op.id]}")
    lines += [
        f"total mutants: {sum(result.by_operator.values())}",
        f"skipped as invalid syntax: {result.skipped_invalid}",
        "note: tests are not run yet; this only lists the mutants",
    ]
    return "\n".join(lines)

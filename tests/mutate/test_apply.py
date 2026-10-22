import hashlib
import io
import tokenize
from pathlib import Path

import libcst as cst
import pytest

from mutantlens.contracts.mutant import Mutant
from mutantlens.mutate.apply import StaleMutantError, apply
from mutantlens.mutate.find import COMPARISON_BOUNDARY, find_mutants
from mutantlens.mutate.hashing import source_hash

FIXTURE = Path(__file__).parent.parent / "fixtures" / "shapes.py"

SOURCES = {
    "toy": FIXTURE.read_text(),
    "comments_and_blank_lines": (
        "# header: a > b stays\n\n\ndef f(x):\n"
        "    # check x\n    return x > 3  # tail\n"
    ),
    "windows_newlines": "a = 1\r\nb = a > 0\r\n\r\nc = b < 2  # c\r\n",
    "non_ascii": 'name = "é"; big = n >= 3\n',
}


def boundary_mutants(source: str) -> list[Mutant]:
    return [m for m in find_mutants(source) if m.operator == COMPARISON_BOUNDARY]


def test_hand_written_case() -> None:
    source = "def f(x):\n    return x > 3  # keep me\n"
    (mutant,) = boundary_mutants(source)
    assert apply(source, mutant) == "def f(x):\n    return x >= 3  # keep me\n"


@pytest.mark.parametrize("name", SOURCES)
def test_only_the_span_changes(name: str) -> None:
    source = SOURCES[name]
    mutants = find_mutants(source)
    assert mutants
    for mutant in mutants:
        mutated = apply(source, mutant)
        start, end = mutant.span.start, mutant.span.end
        assert mutated[:start] == source[:start]
        assert mutated[start : start + len(mutant.replacement)] == mutant.replacement
        assert mutated[start + len(mutant.replacement) :] == source[end:]
        assert mutated != source


@pytest.mark.parametrize("name", SOURCES)
def test_result_still_parses(name: str) -> None:
    source = SOURCES[name]
    for mutant in find_mutants(source):
        cst.parse_module(apply(source, mutant))


def test_line_endings_and_comments_survive() -> None:
    source = SOURCES["windows_newlines"]
    for mutant in find_mutants(source):
        mutated = apply(source, mutant)
        assert mutated.count("\r\n") == source.count("\r\n")
        assert "# c" in mutated


def tokens(source: str) -> list[str]:
    return [t.string for t in tokenize.generate_tokens(io.StringIO(source).readline)]


def test_every_toy_mutant_differs_at_exactly_one_token() -> None:
    source = SOURCES["toy"]
    mutants = boundary_mutants(source)
    assert len(mutants) == 14
    for mutant in mutants:
        before, after = tokens(source), tokens(apply(source, mutant))
        assert len(before) == len(after)
        differing = [(a, b) for a, b in zip(before, after, strict=True) if a != b]
        assert differing == [(mutant.original, mutant.replacement)]


def test_applying_the_reverse_swap_restores_the_source() -> None:
    source = SOURCES["toy"]
    for mutant in find_mutants(source):
        mutated = apply(source, mutant)
        reverse = Mutant(
            operator=mutant.operator,
            span=mutant.span.model_copy(
                update={"end": mutant.span.start + len(mutant.replacement)}
            ),
            original=mutant.replacement,
            replacement=mutant.original,
            source_hash=source_hash(mutated),
        )
        assert apply(mutated, reverse) == source


def test_stale_mutant_is_rejected_with_a_clear_error() -> None:
    source = "def f(x):\n    return x > 3\n"
    (mutant,) = boundary_mutants(source)
    edited = "# new comment\n" + source
    with pytest.raises(StaleMutantError, match="hash"):
        apply(edited, mutant)


def test_one_character_change_makes_every_mutant_stale() -> None:
    source = SOURCES["toy"]
    edited = source + " "
    for mutant in find_mutants(source):
        with pytest.raises(StaleMutantError):
            apply(edited, mutant)


def test_mutants_carry_the_hash_of_their_source() -> None:
    source = SOURCES["toy"]
    assert source_hash(source) == hashlib.sha256(source.encode()).hexdigest()
    assert {m.source_hash for m in find_mutants(source)} == {source_hash(source)}


def test_apply_never_writes_a_file() -> None:
    before = FIXTURE.read_bytes()
    source = FIXTURE.read_text()
    for mutant in find_mutants(source):
        apply(source, mutant)
    assert FIXTURE.read_bytes() == before

import json
from pathlib import Path

import libcst as cst
import pytest

from mutantlens.contracts.mutant import Mutant
from mutantlens.mutate.find import COMPARISON_BOUNDARY, find_mutants

FIXTURES = Path(__file__).parent.parent / "fixtures"

SOURCES = {
    "toy": (FIXTURES / "shapes.py").read_text(),
    "chained": "ok = 1 < x <= 10\n",
    "windows_newlines": "a = 1\r\nb = a > 0\r\nc = b < 2\r\n",
    "non_ascii": 'name = "é"; big = n >= 3\n',
}


def boundary_mutants(source: str) -> list[Mutant]:
    return [m for m in find_mutants(source) if m.operator == COMPARISON_BOUNDARY]


def apply_by_slice(source: str, mutant: Mutant) -> str:
    return source[: mutant.span.start] + mutant.replacement + source[mutant.span.end :]


def test_golden_mutants_for_toy_file() -> None:
    expected = json.loads((FIXTURES / "shapes.mutants.json").read_text())
    found = [m.model_dump() for m in boundary_mutants(SOURCES["toy"])]
    assert found == expected


def test_toy_file_has_fourteen_boundary_mutants() -> None:
    mutants = boundary_mutants(SOURCES["toy"])
    assert len(mutants) == 14
    assert {m.operator for m in mutants} == {COMPARISON_BOUNDARY}


def test_is_deterministic() -> None:
    assert boundary_mutants(SOURCES["toy"]) == boundary_mutants(SOURCES["toy"])


def test_order_is_source_order() -> None:
    starts = [m.span.start for m in boundary_mutants(SOURCES["toy"])]
    assert starts == sorted(starts)


@pytest.mark.parametrize("name", SOURCES)
def test_span_covers_exactly_the_original_operator(name: str) -> None:
    source = SOURCES[name]
    for mutant in boundary_mutants(source):
        assert source[mutant.span.start : mutant.span.end] == mutant.original
        assert mutant.original in {">", ">=", "<", "<="}


@pytest.mark.parametrize("name", SOURCES)
def test_every_mutant_parses_and_changes_one_operator(name: str) -> None:
    source = SOURCES[name]
    for mutant in boundary_mutants(source):
        mutated = apply_by_slice(source, mutant)
        cst.parse_module(mutated)
        assert mutated != source
        assert len(mutated) - len(source) == len(mutant.replacement) - len(
            mutant.original
        )


def test_each_operator_swaps_to_its_boundary_partner() -> None:
    source = "a > b\nc >= d\ne < f\ng <= h\n"
    pairs = [(m.original, m.replacement) for m in boundary_mutants(source)]
    assert pairs == [(">", ">="), (">=", ">"), ("<", "<="), ("<=", "<")]


def test_chained_comparison_gives_one_mutant_per_operator() -> None:
    pairs = [(m.original, m.replacement) for m in boundary_mutants(SOURCES["chained"])]
    assert pairs == [("<", "<="), ("<=", "<")]


def test_nothing_inside_strings_or_comments_is_mutated() -> None:
    source = (
        '"""Docstring with a > b and c <= d."""\n'
        "# comment: x < y\n"
        'label = "a >= b"\n'
        "fmt = f'{1} > {2}'\n"
    )
    assert boundary_mutants(source) == []


def test_only_real_comparisons_are_found_next_to_text_that_looks_like_one() -> None:
    source = 'msg = "x > y"  # a < b\nok = p > q\n'
    mutants = boundary_mutants(source)
    assert [m.original for m in mutants] == [">"]
    assert source[mutants[0].span.start :].startswith("> q")


def test_other_operators_are_left_alone() -> None:
    assert boundary_mutants("a == b\nc != d\ne in f\ng is h\nx = y + z\n") == []


def test_columns_and_offsets_are_right_after_non_ascii_and_crlf() -> None:
    for name, count in (("windows_newlines", 2), ("non_ascii", 1)):
        source = SOURCES[name]
        mutants = boundary_mutants(source)
        assert len(mutants) == count
        for mutant in mutants:
            assert source[mutant.span.start : mutant.span.end] == mutant.original


def test_source_that_does_not_parse_raises() -> None:
    with pytest.raises(cst.ParserSyntaxError):
        boundary_mutants("def broken(:\n")


def test_source_is_not_modified() -> None:
    source = SOURCES["toy"]
    before = str(source)
    boundary_mutants(source)
    assert source == before

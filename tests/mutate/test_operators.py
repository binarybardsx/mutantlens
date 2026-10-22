"""One fixture per operator: what it changes, and what it leaves alone."""

from collections import Counter
from pathlib import Path

import libcst as cst
import pytest

from mutantlens.contracts.mutant import Span
from mutantlens.mutate.apply import apply
from mutantlens.mutate.find import find_mutants, scan
from mutantlens.mutate.operators.base import Candidate, Locator

FIXTURES = Path(__file__).parent.parent / "fixtures" / "operators"


def fixture(name: str) -> str:
    return (FIXTURES / f"{name}.py").read_text()


def fixture_shapes() -> str:
    return (FIXTURES.parent / "shapes.py").read_text()


def pairs(source: str, operator: str) -> list[tuple[str, str]]:
    return [
        (m.original, m.replacement)
        for m in find_mutants(source)
        if m.operator == operator
    ]


@pytest.mark.parametrize("path", sorted(FIXTURES.glob("*.py")), ids=lambda p: p.stem)
def test_every_mutant_in_every_fixture_parses(path: Path) -> None:
    source = path.read_text()
    mutants = find_mutants(source)
    assert mutants
    for mutant in mutants:
        cst.parse_module(apply(source, mutant))


def test_arithmetic_replace() -> None:
    assert pairs(fixture("arithmetic_replace"), "arithmetic_replace") == [
        ("+", "-"),
        ("-", "+"),
        ("*", "/"),
        ("/", "*"),
        ("//", "/"),
        ("%", "*"),
        ("**", "*"),
        ("+=", "-="),
        ("-=", "+="),
        ("*=", "/="),
        ("/=", "*="),
        ("//=", "/="),
        ("%=", "*="),
        ("**=", "*="),
    ]


def test_boolean_replace() -> None:
    assert pairs(fixture("boolean_replace"), "boolean_replace") == [
        ("and", "or"),
        ("or", "and"),
        ("and", "or"),
        ("and", "or"),
        ("or", "and"),
        ("and", "or"),
    ]


def test_constant_replace() -> None:
    assert pairs(fixture("constant_replace"), "constant_replace") == [
        ("10", "11"),
        ("0xFF", "256"),
        ("1_000", "1001"),
        ("True", "False"),
        ("False", "True"),
        ('["a", "b"]', "[]"),
        ('{"k": "v"}', "{}"),
        ('{"x", "y"}', "set()"),
        ("7", "8"),
    ]


def test_conditional_negate() -> None:
    assert pairs(fixture("conditional_negate"), "conditional_negate") == [
        ("a > b", "not (a > b)"),
        ("a", "not (a)"),
        ("a < 3", "not (a < 3)"),
        ("a", "not (a)"),
        ("a and\n            b", "not (a and\n            b)"),
    ]


def test_return_replace() -> None:
    assert pairs(fixture("return_replace"), "return_replace") == [
        ("a + b", "None"),
        ("a, b", "None"),
        ("a\n        + 1", "None"),
        ("a", "None"),
        ('"return a"', "None"),
    ]


def test_no_operator_touches_strings_comments_docstrings_or_dunder_all() -> None:
    source = (
        '"""Doc: a > b, 5, True, return x, if a: a and b, [1, 2]."""\n'
        "# comment: a + b and c > 5, return x, while a:\n"
        'label = "a + b and 5 if x else y, True, return z"\n'
        '__all__ = ["a", "b"]\n'
        '__all__ += ["c"]\n'
        '__all__: list[str] = ["d"]\n'
    )
    assert find_mutants(source) == []


def test_toy_file_counts_per_operator() -> None:
    counts = Counter(m.operator for m in find_mutants(fixture_shapes()))
    assert dict(sorted(counts.items())) == {
        "arithmetic_replace": 3,
        "boolean_replace": 5,
        "comparison_boundary": 14,
        "conditional_negate": 7,
        "constant_replace": 8,
        "return_replace": 10,
    }


def test_order_is_stable_and_repeatable() -> None:
    source = fixture("return_replace") + fixture("constant_replace")
    first = find_mutants(source)
    assert first == find_mutants(source)
    keys = [(m.span.start, m.span.end, m.operator, m.replacement) for m in first]
    assert keys == sorted(keys)


class _Bogus:
    id = "bogus"

    def candidates(self, module: cst.Module, locator: Locator) -> list[Candidate]:
        return [Candidate(span=Span(start=0, end=1), replacement="(((")]


def test_candidates_that_would_not_parse_are_skipped_and_counted() -> None:
    result = scan("x = 1\n", operators=[_Bogus()])
    assert result.mutants == []
    assert result.skipped_invalid == 1


def test_valid_candidates_are_not_counted_as_skipped() -> None:
    assert scan(fixture_shapes()).skipped_invalid == 0

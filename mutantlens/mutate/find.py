from collections.abc import Sequence

import libcst as cst
from libcst.metadata import MetadataWrapper, PositionProvider
from pydantic import BaseModel, ConfigDict

from mutantlens.contracts.mutant import Mutant
from mutantlens.mutate.apply import apply
from mutantlens.mutate.hashing import source_hash
from mutantlens.mutate.operators import ALL_OPERATORS
from mutantlens.mutate.operators.base import Locator, Operator
from mutantlens.mutate.operators.comparison_boundary import ID as COMPARISON_BOUNDARY

__all__ = ["COMPARISON_BOUNDARY", "FindResult", "find_mutants", "scan"]


class FindResult(BaseModel):
    model_config = ConfigDict(frozen=True)

    mutants: list[Mutant]
    skipped_invalid: int


def scan(source: str, operators: Sequence[Operator] = ALL_OPERATORS) -> FindResult:
    """Find every mutant for `operators`, in a stable order.

    A candidate whose mutated source does not parse is dropped and counted in
    `skipped_invalid`. Raises libcst.ParserSyntaxError if `source` does not parse.
    """
    wrapper = MetadataWrapper(cst.parse_module(source))
    locator = Locator(source, wrapper.resolve(PositionProvider))
    digest = source_hash(source)
    found: list[Mutant] = []
    for operator in operators:
        for candidate in operator.candidates(wrapper.module, locator):
            found.append(
                Mutant(
                    operator=operator.id,
                    span=candidate.span,
                    original=locator.text_of(candidate.span),
                    replacement=candidate.replacement,
                    source_hash=digest,
                )
            )
    found.sort(key=lambda m: (m.span.start, m.span.end, m.operator, m.replacement))
    mutants: list[Mutant] = []
    skipped = 0
    for mutant in found:
        try:
            cst.parse_module(apply(source, mutant))
        except cst.ParserSyntaxError:
            skipped += 1
        else:
            mutants.append(mutant)
    return FindResult(mutants=mutants, skipped_invalid=skipped)


def find_mutants(source: str) -> list[Mutant]:
    """Find every mutant in `source`, in source order.

    Raises libcst.ParserSyntaxError if `source` does not parse.
    """
    return scan(source).mutants

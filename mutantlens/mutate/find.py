import re
from collections.abc import Mapping

import libcst as cst
from libcst.metadata import CodeRange, MetadataWrapper, PositionProvider

from mutantlens.contracts.mutant import Mutant, Span
from mutantlens.mutate.hashing import source_hash

COMPARISON_BOUNDARY = "comparison_boundary"

_REPLACEMENTS: dict[type[cst.CSTNode], str] = {
    cst.GreaterThan: ">=",
    cst.GreaterThanEqual: ">",
    cst.LessThan: "<=",
    cst.LessThanEqual: "<",
}

_NEWLINE = re.compile(r"\r\n|\r|\n")


class _BoundaryFinder(cst.CSTVisitor):
    def __init__(self, source: str, positions: Mapping[cst.CSTNode, CodeRange]) -> None:
        self._source = source
        self._source_hash = source_hash(source)
        self._positions = positions
        self._line_starts = [0] + [m.end() for m in _NEWLINE.finditer(source)]
        self.mutants: list[Mutant] = []

    def _offset(self, line: int, column: int) -> int:
        return self._line_starts[line - 1] + column

    def _record(self, node: cst.CSTNode, replacement: str) -> None:
        position = self._positions[node]
        start = self._offset(position.start.line, position.start.column)
        end = self._offset(position.end.line, position.end.column)
        self.mutants.append(
            Mutant(
                operator=COMPARISON_BOUNDARY,
                span=Span(start=start, end=end),
                original=self._source[start:end],
                replacement=replacement,
                source_hash=self._source_hash,
            )
        )

    def on_visit(self, node: cst.CSTNode) -> bool:
        replacement = _REPLACEMENTS.get(type(node))
        if replacement is not None:
            self._record(node, replacement)
        return True


def find_mutants(source: str) -> list[Mutant]:
    """Find every comparison-boundary mutant in `source`, in source order.

    Raises libcst.ParserSyntaxError if `source` does not parse.
    """
    wrapper = MetadataWrapper(cst.parse_module(source))
    finder = _BoundaryFinder(source, wrapper.resolve(PositionProvider))
    wrapper.module.visit(finder)
    return sorted(finder.mutants, key=lambda m: m.span.start)

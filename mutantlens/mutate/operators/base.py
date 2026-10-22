import re
from collections.abc import Mapping
from typing import Protocol

import libcst as cst
from libcst.metadata import CodeRange
from pydantic import BaseModel, ConfigDict

from mutantlens.contracts.mutant import Span

_NEWLINE = re.compile(r"\r\n|\r|\n")


class Candidate(BaseModel):
    """One possible mutation: replace the source at `span` with `replacement`."""

    model_config = ConfigDict(frozen=True)

    span: Span
    replacement: str


class Locator:
    """Turns libcst positions into character offsets into the source string."""

    def __init__(self, source: str, positions: Mapping[cst.CSTNode, CodeRange]) -> None:
        self.source = source
        self._positions = positions
        self._line_starts = [0] + [m.end() for m in _NEWLINE.finditer(source)]

    def span_of(self, node: cst.CSTNode) -> Span:
        position = self._positions[node]
        return Span(
            start=self._line_starts[position.start.line - 1] + position.start.column,
            end=self._line_starts[position.end.line - 1] + position.end.column,
        )

    def text_of(self, span: Span) -> str:
        return self.source[span.start : span.end]


class Operator(Protocol):
    id: str

    def candidates(self, module: cst.Module, locator: Locator) -> list[Candidate]: ...


def _assigns_dunder_all(node: cst.CSTNode) -> bool:
    if isinstance(node, cst.Assign):
        targets = [t.target for t in node.targets]
    elif isinstance(node, (cst.AnnAssign, cst.AugAssign)):
        targets = [node.target]
    else:
        return False
    return any(isinstance(t, cst.Name) and t.value == "__all__" for t in targets)


class CandidateVisitor(cst.CSTVisitor):
    """Base for operators. Subclasses override `consider`. Never enters `__all__`."""

    def __init__(self, locator: Locator) -> None:
        self.locator = locator
        self.candidates: list[Candidate] = []

    def consider(self, node: cst.CSTNode) -> None:
        raise NotImplementedError

    def add(self, node: cst.CSTNode, replacement: str) -> None:
        self.candidates.append(
            Candidate(span=self.locator.span_of(node), replacement=replacement)
        )

    def on_visit(self, node: cst.CSTNode) -> bool:
        if _assigns_dunder_all(node):
            return False
        self.consider(node)
        return super().on_visit(node)

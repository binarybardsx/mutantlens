import libcst as cst

from mutantlens.mutate.operators.base import Candidate, CandidateVisitor, Locator

ID = "boolean_replace"

_REPLACEMENTS: dict[type[cst.CSTNode], str] = {
    cst.And: "or",
    cst.Or: "and",
}


class _Visitor(CandidateVisitor):
    def consider(self, node: cst.CSTNode) -> None:
        replacement = _REPLACEMENTS.get(type(node))
        if replacement is not None:
            self.add(node, replacement)


class BooleanReplace:
    id = ID

    def candidates(self, module: cst.Module, locator: Locator) -> list[Candidate]:
        visitor = _Visitor(locator)
        module.visit(visitor)
        return visitor.candidates

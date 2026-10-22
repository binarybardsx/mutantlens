import libcst as cst

from mutantlens.mutate.operators.base import Candidate, CandidateVisitor, Locator

ID = "comparison_boundary"

_REPLACEMENTS: dict[type[cst.CSTNode], str] = {
    cst.GreaterThan: ">=",
    cst.GreaterThanEqual: ">",
    cst.LessThan: "<=",
    cst.LessThanEqual: "<",
}


class _Visitor(CandidateVisitor):
    def consider(self, node: cst.CSTNode) -> None:
        replacement = _REPLACEMENTS.get(type(node))
        if replacement is not None:
            self.add(node, replacement)


class ComparisonBoundary:
    id = ID

    def candidates(self, module: cst.Module, locator: Locator) -> list[Candidate]:
        visitor = _Visitor(locator)
        module.visit(visitor)
        return visitor.candidates

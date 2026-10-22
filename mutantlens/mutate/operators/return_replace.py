import libcst as cst

from mutantlens.mutate.operators.base import Candidate, CandidateVisitor, Locator

ID = "return_replace"


class _Visitor(CandidateVisitor):
    def consider(self, node: cst.CSTNode) -> None:
        if not isinstance(node, cst.Return) or node.value is None:
            return
        if isinstance(node.value, cst.Name) and node.value.value == "None":
            return
        self.add(node.value, "None")


class ReturnReplace:
    id = ID

    def candidates(self, module: cst.Module, locator: Locator) -> list[Candidate]:
        visitor = _Visitor(locator)
        module.visit(visitor)
        return visitor.candidates

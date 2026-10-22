import libcst as cst

from mutantlens.mutate.operators.base import Candidate, CandidateVisitor, Locator

ID = "conditional_negate"


class _Visitor(CandidateVisitor):
    def consider(self, node: cst.CSTNode) -> None:
        if isinstance(node, (cst.If, cst.While, cst.IfExp)):
            span = self.locator.span_of(node.test)
            text = self.locator.text_of(span)
            self.add(node.test, f"not ({text})")


class ConditionalNegate:
    id = ID

    def candidates(self, module: cst.Module, locator: Locator) -> list[Candidate]:
        visitor = _Visitor(locator)
        module.visit(visitor)
        return visitor.candidates

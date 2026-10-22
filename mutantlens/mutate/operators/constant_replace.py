import libcst as cst

from mutantlens.mutate.operators.base import Candidate, CandidateVisitor, Locator

ID = "constant_replace"


class _Visitor(CandidateVisitor):
    def consider(self, node: cst.CSTNode) -> None:
        if isinstance(node, cst.Integer):
            try:
                self.add(node, str(int(node.value, 0) + 1))
            except ValueError:
                pass
        elif isinstance(node, cst.Name) and node.value in ("True", "False"):
            self.add(node, "False" if node.value == "True" else "True")
        elif isinstance(node, cst.List) and node.elements:
            self.add(node, "[]")
        elif isinstance(node, cst.Set) and node.elements:
            self.add(node, "set()")
        elif isinstance(node, cst.Dict) and node.elements:
            self.add(node, "{}")


class ConstantReplace:
    id = ID

    def candidates(self, module: cst.Module, locator: Locator) -> list[Candidate]:
        visitor = _Visitor(locator)
        module.visit(visitor)
        return visitor.candidates

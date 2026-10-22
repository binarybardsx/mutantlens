import libcst as cst

from mutantlens.mutate.operators.base import Candidate, CandidateVisitor, Locator

ID = "arithmetic_replace"

_REPLACEMENTS: dict[type[cst.CSTNode], str] = {
    cst.Add: "-",
    cst.Subtract: "+",
    cst.Multiply: "/",
    cst.Divide: "*",
    cst.FloorDivide: "/",
    cst.Modulo: "*",
    cst.Power: "*",
    cst.AddAssign: "-=",
    cst.SubtractAssign: "+=",
    cst.MultiplyAssign: "/=",
    cst.DivideAssign: "*=",
    cst.FloorDivideAssign: "/=",
    cst.ModuloAssign: "*=",
    cst.PowerAssign: "*=",
}


class _Visitor(CandidateVisitor):
    def consider(self, node: cst.CSTNode) -> None:
        replacement = _REPLACEMENTS.get(type(node))
        if replacement is not None:
            self.add(node, replacement)


class ArithmeticReplace:
    id = ID

    def candidates(self, module: cst.Module, locator: Locator) -> list[Candidate]:
        visitor = _Visitor(locator)
        module.visit(visitor)
        return visitor.candidates

from mutantlens.mutate.operators.arithmetic_replace import ArithmeticReplace
from mutantlens.mutate.operators.base import Operator
from mutantlens.mutate.operators.boolean_replace import BooleanReplace
from mutantlens.mutate.operators.comparison_boundary import ComparisonBoundary
from mutantlens.mutate.operators.conditional_negate import ConditionalNegate
from mutantlens.mutate.operators.constant_replace import ConstantReplace
from mutantlens.mutate.operators.return_replace import ReturnReplace

ALL_OPERATORS: list[Operator] = [
    ArithmeticReplace(),
    BooleanReplace(),
    ComparisonBoundary(),
    ConditionalNegate(),
    ConstantReplace(),
    ReturnReplace(),
]

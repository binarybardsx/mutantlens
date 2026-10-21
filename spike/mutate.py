"""Throwaway: print one mutant per comparison operator as a diff."""

import ast
import copy
import difflib
import sys

# Each comparison operator and the one it is swapped with.
# Every swap is a classic off-by-one / boundary bug.
SWAP = {
    ast.Gt: ast.GtE, ast.GtE: ast.Gt,
    ast.Lt: ast.LtE, ast.LtE: ast.Lt,
    ast.Eq: ast.NotEq, ast.NotEq: ast.Eq,
}


def mutants(tree):
    """Yield (lineno, mutated_tree), one per swappable operator."""
    # ast.walk visits every node in the tree in a fixed order.
    # ni is this node's position in that order, so we can find the same node in a copy.
    for ni, node in enumerate(ast.walk(tree)):
        # Only comparisons (a < b, x == y, ...) are mutated.
        if not isinstance(node, ast.Compare):
            continue
        # A chained comparison like a < b < c holds several operators in node.ops.
        # oi is the operator's position inside this one node.
        for oi, op in enumerate(node.ops):
            # Skip operators we have no swap for (in, is, ...).
            if type(op) not in SWAP:
                continue
            # Copy the whole tree so each mutant starts from the original
            # and the original is never modified.
            t = copy.deepcopy(tree)
            # The copy is walked in the same order, so index ni is the same node.
            target = list(ast.walk(t))[ni]
            # The mutation: replace this one operator with its swap.
            target.ops[oi] = SWAP[type(op)]()
            yield node.lineno, t


def main(path):
    # The file is only read, never written.
    with open(path) as f:
        tree = ast.parse(f.read())
    # Diff against the unparsed original, not the raw text, so the only
    # difference in each diff is the mutated operator (formatting is normalised).
    original = ast.unparse(tree).splitlines()
    n = 0
    for lineno, t in mutants(tree):
        n += 1
        # n=0 means no context lines: show only the changed line.
        diff = difflib.unified_diff(
            original, ast.unparse(t).splitlines(),
            "original", f"mutant {n} (line {lineno})", lineterm="", n=0,
        )
        print("\n".join(diff))
        print()
    print(f"{n} mutants")


if __name__ == "__main__":
    main(sys.argv[1])

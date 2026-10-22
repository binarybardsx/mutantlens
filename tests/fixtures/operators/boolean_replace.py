def f(a, b, c):
    both = a and b
    either = a or b
    chain = a and b and c  # two operators, two mutants
    mixed = a or b and c
    negated = not a  # not is left alone
    bits = a & b | c  # bitwise is left alone
    text = "a and b or c"  # a or b in a comment
    return both

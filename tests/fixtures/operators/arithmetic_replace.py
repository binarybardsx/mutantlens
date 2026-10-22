def f(a, b):
    total = a + b
    diff = a - b
    prod = a * b
    quot = a / b
    floor = a // b
    rem = a % b
    power = a**b
    total += a
    total -= a
    total *= a
    total /= a
    total //= a
    total %= a
    total **= a
    neg = -a  # unary minus is left alone
    pos = +a
    mask = a & b  # bitwise is left alone
    shifted = a << b
    text = "a + b"  # a * b in a comment
    return text

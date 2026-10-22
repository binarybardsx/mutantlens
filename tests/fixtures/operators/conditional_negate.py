def f(a, b, items):
    if a > b:
        pass
    elif a:
        pass
    while a < 3:
        a += 1
    label = "big" if a else "small"
    flag = (
        a
        and b
    )
    if (a and
            b):
        pass
    for item in items:  # a for loop has no condition
        pass
    squares = [i for i in items if i]  # comprehension filters are left alone
    text = "if a: pass"  # while a: in a comment
    return label

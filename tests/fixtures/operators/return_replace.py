def total(a, b):
    return a + b


def pair(a, b):
    return a, b


def nothing():
    return


def already_none():
    return None


def long_value(a):
    return (
        a
        + 1
    )


def guard(a):
    if a:
        return a
    return "return a"  # return b in a comment

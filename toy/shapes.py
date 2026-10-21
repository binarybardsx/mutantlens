def is_valid_triangle(a, b, c):
    if a <= 0 or b <= 0 or c <= 0:
        return False
    return a + b > c and a + c > b and b + c > a


def classify_age(age):
    if age < 0:
        raise ValueError("age must not be negative")
    if age < 13:
        return "child"
    if age < 20:
        return "teen"
    if age >= 65:
        return "senior"
    return "adult"


def clamp(x, lo, hi):
    if x < lo:
        return lo
    if x > hi:
        return hi
    return x


def can_fit(w, h, max_w, max_h):
    return w <= max_w and h <= max_h

def add(x, y):
    return x + y


def substract(x, y):
    return x - y


def inc(x):
    return x + 1


def test_add():
    assert add(1, 2) == 3


def test_substact():
    assert substract(2, 1) == 1


def test_inc():
    assert inc(3) == 4

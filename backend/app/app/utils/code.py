from random import randint


def fake_gen(n: int) -> str:
    return f"{randint(1, 10 ** n + 1):0100d}"[-n:]

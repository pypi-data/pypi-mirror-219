from __future__ import annotations
import math
import random


class GaussGenerators:
    def __init__(self, seed: int):
        random.seed(seed)
        self.characters = [chr(x) for x in range(ord("a"), ord("z") + 1)]
        self.characters.extend([chr(x) for x in range(ord("A"), ord("Z") + 1)])
        self.digits = [str(x) for x in range(0, 10)]

    def strings(self, n: int, avglen: int):
        if n / 2 >= math.pow(len(self.characters), avglen):
            raise Exception(f"{n} is too big")
        out = set()
        while len(out) < n:
            l = int(random.gauss(avglen, 1))
            s = "".join(
                [
                    self.characters[random.randint(0, len(self.characters) - 1)]
                    for _ in range(l)
                ]
            )
            out.add(s)

        return list(out)

    def integers(self, n: int, mean: float, std: float):
        return [int(random.gauss(mean, std)) for _ in range(n)]


if __name__ == "__main__":
    lst = GaussGenerators(72).strings(20, 5)
    print(lst)
    print("\n".join(lst))

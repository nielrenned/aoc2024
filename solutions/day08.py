from collections import defaultdict
from itertools import permutations

DAY = 8
RAW_INPUT = None
INPUT = None


def load_input(use_test_input=False):
    global RAW_INPUT
    path = f'inputs/actual/day{DAY:02}.txt'
    if use_test_input:
        path = f'inputs/test/day{DAY:02}.txt'
    with open(path) as f:
        RAW_INPUT = f.read()


class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __neg__(self):
        return Vector(-self.x, -self.y)

    def __mul__(self, i):
        return Vector(i*self.x, i*self.y)
    
    def __rmul__(self, i):
        return self.__mul__(i)

    def __eq__(self, other):
        if not isinstance(other, Vector): return False
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))
    
    def __str__(self):
        return f'({self.x}, {self.y})'
    
    def __repr__(self):
        return self.__str__()


def parse_input():
    global INPUT
    INPUT = []
    antennas = defaultdict(list)
    w = 0
    h = 0

    for y, line in enumerate(RAW_INPUT.split('\n')):
        if line == '': continue
        h = max(h, y+1)
        for x, c in enumerate(line):
            w = max(w, x+1)
            if c != '.': antennas[c].append(Vector(x, y))
    
    INPUT = w, h, antennas


def inbounds(p):
    w, h, _ = INPUT
    return (0 <= p.x < w) and (0 <= p.y < h)


def part1():
    _, _, antennas = INPUT
    antinodes = set()
    for id in antennas:
        for p1, p2 in permutations(antennas[id], 2):
            antinodes.add(p1 + 2*(p2 - p1))
    return len(list(filter(inbounds, antinodes)))


def part2():
    _, _, antennas = INPUT
    antinodes = set()
    for id in antennas:
        for p1, p2 in permutations(antennas[id], 2):
            v = p2 - p1
            while inbounds(p1):
                antinodes.add(p1)
                p1 += v
    return len(antinodes)


def main():
    load_input(use_test_input=False)
    parse_input()
    print('PART 1:', part1())
    print('PART 2:', part2())


if __name__ == "__main__":
    main()

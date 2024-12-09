from collections import defaultdict
from itertools import combinations

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


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __neg__(self):
        return Point(-self.x, -self.y)

    def __mul__(self, i):
        if not isinstance(i, int):
            raise ValueError(f"Cannot multiply a point by {type(i)}. Only multiplication by integers is supported.")
        return Point(i*self.x, i*self.y)
    
    def __rmul__(self, i):
        return self.__mul__(i)

    def __eq__(self, other):
        if not isinstance(other, Point): return False
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))


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
            if c != '.': antennas[c].append(Point(x, y))
    
    INPUT = w, h, antennas


def inbounds(p):
    w, h, _ = INPUT
    return (0 <= p.x < w) and (0 <= p.y < h)

def part1():
    w, h, antennas = INPUT
    antinodes = set()
    for id in antennas:
        for p1, p2 in combinations(antennas[id], 2):
            v = p2 - p1
            antinodes.add(p1 + 2*v)
            antinodes.add(p2 - 2*v)
    return len(list(filter(inbounds, antinodes)))


def part2():
    w, h, antennas = INPUT
    antinodes = set()
    for id in antennas:
        for p1, p2 in combinations(antennas[id], 2):
            v = p2 - p1
            p3 = p1
            while inbounds(p3):
                antinodes.add(p3)
                p3 += v
            p3 = p1
            while inbounds(p3):
                antinodes.add(p3)
                p3 -= v
    return len(antinodes)


def main():
    load_input(use_test_input=False)
    parse_input()
    print('PART 1:', part1())
    print('PART 2:', part2())


if __name__ == "__main__":
    main()

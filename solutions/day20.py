from day08 import Vector as Point
from collections import defaultdict

DAY = 20
RAW_INPUT = None
INPUT = None


def load_input(use_test_input=False):
    global RAW_INPUT
    path = f'inputs/actual/day{DAY:02}.txt'
    if use_test_input:
        path = f'inputs/test/day{DAY:02}.txt'
    with open(path) as f:
        RAW_INPUT = f.read()


def parse_input():
    global INPUT
    map = []
    start = None
    end = None
    for y, line in enumerate(RAW_INPUT.split('\n')):
        if line == '': continue
        map_line = []
        for x, c in enumerate(line):
            if c == 'S': start = (x, y)
            if c == 'E': end = (x, y)
            map_line.append('#' if c == '#' else '.')
        map.append(map_line)
    INPUT = start, end, map


DIRECTIONS = [(0, -1), (1, 0), (0, 1), (-1, 0)]
TWO_STEPS = [(0, -2), (2, 0), (0, 2), (-2, 0)]

def print_map(map, route):
    for y, line in enumerate(map):
        for x, c in enumerate(line):
            if (x, y) in route: print('O', end='')
            else: print(c, end='')
        print()

def part1():
    start, end, map = INPUT
    route = [start]
    while route[-1] != end:
        for (dx, dy) in DIRECTIONS:
            x, y = route[-1]
            nx, ny = x + dx, y + dy
            if len(route) >= 2 and route[-2] == (nx, ny): continue
            if map[ny][nx] == '.':
                route.append((nx, ny))
                break
    
    SAVE_GOAL = 50
    LENGTH_MIN = 2
    LENGTH_MAX = 20

    total = 0
    counter = defaultdict(int)
    for i1, (x1, y1) in enumerate(route):
        for i2, (x2, y2) in enumerate(route[i1+SAVE_GOAL+1:]):
            if LENGTH_MIN <= abs(x1 - x2) + abs(y1 - y2) <= LENGTH_MAX:
                counter[i2+SAVE_GOAL-1] += 1
                total += 1
    
    for saved_steps in sorted(counter.keys()):
        print(f'There are {counter[saved_steps]} cheats that save {saved_steps} picoseconds')

    return total

def part2():
    pass


def main():
    load_input(use_test_input=True)
    parse_input()
    print('PART 1:', part1())
    # print('PART 2:', part2())


if __name__ == "__main__":
    main()

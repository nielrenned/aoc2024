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


def count_cheats(min_length, max_length, min_savings):
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

    cheats = defaultdict(int)
    for i1, (x1, y1) in enumerate(route):
        for i2, (x2, y2) in enumerate(route[i1+2:]):
            cheat_len = abs(x2 - x1) + abs(y2 - y1)
            if min_length <= cheat_len <= max_length:
                cheats[i2+2-cheat_len] += 1

    return sum(cheats[s] for s in cheats if s >= min_savings)


def part1():
    return count_cheats(2, 2, 100)


def part2():
    return count_cheats(2, 20, 100)


def main():
    load_input(use_test_input=False)
    parse_input()
    print('PART 1:', part1())
    print('PART 2:', part2())


if __name__ == "__main__":
    main()

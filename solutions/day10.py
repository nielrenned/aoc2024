DAY = 10
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
    INPUT = []
    for line in RAW_INPUT.split('\n'):
        if line == '': continue
        INPUT.append(list(map(int, line)))


def get_neighbors(x0, y0):
    w, h = len(INPUT[0]), len(INPUT)
    neighbors = []
    for dx, dy in [(1, 0), (0, -1), (-1, 0), (0, 1)]:
        x, y = x0 + dx, y0 + dy
        if 0 <= x < w and 0 <= y < h:
            neighbors.append((x, y))
    return neighbors


def find_distinct_paths(path: tuple):
    x0, y0 = path[-1]
    h0 = INPUT[y0][x0]

    paths = set()
    for x, y in get_neighbors(x0, y0):
        h = INPUT[y][x]
        if h != h0 + 1: continue

        new_path = path + ((x, y),)
        if h0 == 8: paths.add(new_path)
        else:       paths |= find_distinct_paths(new_path)
    return paths


ALL_PATHS = [] # We'll use a list for faster iteration


def part1():
    for y, line in enumerate(INPUT):
        for x, h in enumerate(line):
            if h != 0: continue
            path_start = ((x, y), )
            ALL_PATHS.extend(find_distinct_paths(path_start))
    
    # Number of distinct start and end points
    return len(set((path[0], path[-1]) for path in ALL_PATHS))


def part2():
    # Number of distinct trails
    return len(ALL_PATHS)


def main():
    load_input(use_test_input=False)
    parse_input()
    print('PART 1:', part1())
    print('PART 2:', part2())


if __name__ == "__main__":
    main()

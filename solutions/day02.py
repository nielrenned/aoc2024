import math

DAY = 2
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
        INPUT.append(list(map(int, line.split())))


sign = lambda x: math.copysign(1, x)


def is_safe(level):
    direction = None
    for i in range(len(level)-1):
        a, b = level[i:i+2]
        if direction is None: direction = sign(a-b)
        if sign(a-b) != direction or not (1 <= abs(a-b) <= 3):
            return False
    return True


def part1():
    return sum(1 for level in INPUT if is_safe(level))


def is_loosely_safe(level):
    if is_safe(level): return True
    for i in range(len(level)):
        level_copy = level[:i] + level[i+1:]
        if is_safe(level_copy): return True
    return False


def part2():
    return sum(1 for level in INPUT if is_loosely_safe(level))


def main():
    load_input(use_test_input=False)
    parse_input()
    print('PART 1:', part1())
    print('PART 2:', part2())


if __name__ == "__main__":
    main()

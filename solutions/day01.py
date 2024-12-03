from collections import Counter

DAY = 1
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
    left = []
    right = []
    for line in RAW_INPUT.split('\n'):
        if line == '': continue
        nums = list(map(int, line.split()))
        left.append(nums[0])
        right.append(nums[1])
    INPUT = (left, right)


def part1():
    left, right = INPUT
    return sum(abs(l - r) for l, r in zip(sorted(left), sorted(right)))


def part2():
    left, right = INPUT
    counted_right = Counter(right)
    return sum(counted_right[n]*n for n in left)


def main():
    load_input(use_test_input=False)
    parse_input()
    print('PART 1:', part1())
    print('PART 2:', part2())


if __name__ == "__main__":
    main()

from itertools import product
from operator import add, mul

DAY = 7
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
        goal, numbers = line.split(': ')
        INPUT.append((int(goal), tuple(map(int, numbers.split()))))


def apply_ops(numbers, ops):
    value = numbers[0]
    for i, op in enumerate(ops):
        value = op(value, numbers[i+1])
    return value


def is_achievable(goal, numbers, valid_ops):
    op_combos = product(valid_ops, repeat=len(numbers)-1)
    return any(apply_ops(numbers, ops) == goal for ops in op_combos)


def part1():
    return sum(goal for goal, numbers in INPUT if is_achievable(goal, numbers, [add, mul]))


def part2():
    cat = lambda x,y: int(str(x) + str(y))
    return sum(goal for goal, numbers in INPUT if is_achievable(goal, numbers, [add, mul, cat]))


def main():
    load_input(use_test_input=False)
    parse_input()
    print('PART 1:', part1())
    print('PART 2:', part2())


if __name__ == "__main__":
    main()

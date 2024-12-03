import re

DAY = 3
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
    INPUT = RAW_INPUT


def part1():
    instr_regex = r'mul\((\d{1,3}),(\d{1,3})\)'
    return sum(int(a)*int(b) for a, b in re.findall(instr_regex, INPUT))


def part2():
    instr_regex = r"(do\(\))|(don't\(\))|mul\((\d{1,3}),(\d{1,3})\)"
    enabled = True
    total = 0
    for do, do_not, a, b in re.findall(instr_regex, INPUT):
        if do_not: enabled = False
        elif do:   enabled = True

        if enabled and a and b:
            total += int(a)*int(b)
    return total

def main():
    load_input(use_test_input=False)
    parse_input()
    print('PART 1:', part1())
    print('PART 2:', part2())


if __name__ == "__main__":
    main()

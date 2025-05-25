DAY = 21
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
        INPUT.append(line)


def part1():
    pass


def part2():
    pass


def main():
    load_input(use_test_input=False)
    parse_input()
    print('PART 1:', part1())
    # print('PART 2:', part2())


if __name__ == "__main__":
    main()

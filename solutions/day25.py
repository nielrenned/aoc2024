from itertools import product

DAY = 25
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
    lines = RAW_INPUT.split('\n')
    keys = []
    locks = []

    for i in range(0, len(lines), 8):
        tool = lines[i:i+8]

        if tool[0] == '#####':
            lock = []
            for c in range(5):
                height = min(r-1 for r in range(7) if tool[r][c] == '.')
                lock.append(height)
            locks.append(lock)
        else:
            key = []
            for c in range(5):
                height = 6 - min(r for r in range(7) if tool[r][c] == '#')
                key.append(height)
            keys.append(key)
    
    INPUT = locks, keys

def part1():
    locks, keys = INPUT
    count = 0
    for lock, key in product(locks, keys):
        if all(lock[i] + key[i] <= 5 for i in range(5)):
            count += 1
    return count


def part2():
    pass


def main():
    load_input(use_test_input=False)
    parse_input()
    print('PART 1:', part1())
    # print('PART 2:', part2())


if __name__ == "__main__":
    main()

from collections import defaultdict

DAY = 22
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
        INPUT.append(int(line))


def mix(n1, n2):
    return n1 ^ n2


def prune(n):
    return n % 16777216


def evolve(n):
    n = prune(mix(n, n*64))
    n = prune(mix(n, n//32))
    n = prune(mix(n, n*2048))
    return n


def part1():
    total = 0
    for n in INPUT:
        for _ in range(2000):
            n = evolve(n)
        total += n
    return total


def solve():
    part1_total = 0
    part2_totals = defaultdict(int)
    for n in INPUT:
        values = [n % 10]
        for _ in range(2000):
            n = evolve(n)
            values.append(n % 10)
        part1_total += n
        
        seen = set()
        for i in range(2001-5):
            seq = values[i:i+5]
            diffs = tuple(seq[j+1] - seq[j] for j in range(4))
            if diffs not in seen:
                seen.add(diffs)
                part2_totals[diffs] += seq[-1]
    
    return part1_total, max(part2_totals.values())


def main():
    load_input(use_test_input=False)
    parse_input()
    part1_solution, part2_solution = solve()
    print('PART 1:', part1_solution)
    print('PART 2:', part2_solution)


if __name__ == "__main__":
    main()

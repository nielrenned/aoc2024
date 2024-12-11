from collections import defaultdict

DAY = 11
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
        INPUT = list(map(int, line.split()))
        break


def blink(stones):
    new_stones = defaultdict(int)
    for stone, count in stones.items():
        if stone == 0:
            new_stones[1] += count
        elif len(str(stone)) % 2 == 0:
            s = str(stone)
            a = int(s[:len(s)//2])
            b = int(s[len(s)//2:])
            new_stones[a] += count
            new_stones[b] += count
        else:
            new_stones[stone*2024] += count
    return new_stones


def part1():
    stones = defaultdict(int)
    for stone in INPUT: stones[stone] += 1

    for _ in range(25):
        stones = blink(stones)
    
    return sum(v for _, v in stones.items())
    


def part2():
    stones = defaultdict(int)
    for stone in INPUT: stones[stone] += 1

    for _ in range(75):
        stones = blink(stones)
    
    return sum(v for _, v in stones.items())


def main():
    load_input(use_test_input=False)
    parse_input()
    print('PART 1:', part1())
    print('PART 2:', part2())


if __name__ == "__main__":
    main()

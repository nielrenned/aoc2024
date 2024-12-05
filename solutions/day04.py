from itertools import product

DAY = 4
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
    DIRECTIONS = [(1,0), (1,1), (0,1), (-1,1), (-1,0), (-1,-1), (0,-1), (1,-1)]
    w, h = len(INPUT[0]), len(INPUT)
    
    count = 0
    for dx, dy in DIRECTIONS:
        for x, y in product(range(w), range(h)):
            if not (0 <= x + 3*dx < w and 0 <= y + 3*dy < h): continue

            word = ''.join(INPUT[y+i*dy][x+i*dx] for i in range(4))
            if word == 'XMAS':
                count += 1
    
    return count


def part2():
    w, h = len(INPUT[0]), len(INPUT)
    
    count = 0
    # Restricting these ranges guarantees we'll never run into an out-of-bounds error
    for x, y in product(range(1, w-1), range(1, h-1)):
        if INPUT[y][x] != 'A': continue # We need 'A' in the center of our X-MAS

        main_diagonal = {INPUT[y-1][x-1], INPUT[y+1][x+1]}
        anti_diagonal = {INPUT[y+1][x-1], INPUT[y-1][x+1]}
        if main_diagonal == anti_diagonal == {'M', 'S'}:
            count += 1
    
    return count


def main():
    load_input(use_test_input=False)
    parse_input()
    print('PART 1:', part1())
    print('PART 2:', part2())


if __name__ == "__main__":
    main()

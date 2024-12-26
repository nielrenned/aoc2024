from functools import cache

DAY = 19
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
    patterns = lines[0].split(', ')
    goals = []
    for line in lines[2:]:
        if line == '': continue
        goals.append(line)
    INPUT = patterns, goals


def check_goal(goal):
    if goal == '': return True
    
    for pattern in INPUT[0]:
        if not goal.startswith(pattern): continue
        if check_goal(goal[len(pattern):]):
            return True
    return False


def part1():
    return sum(1 for goal in INPUT[1] if check_goal(goal))


@cache
def count_combos(goal):
    if goal == '': return 1
    
    total = 0
    for pattern in INPUT[0]:
        if not goal.startswith(pattern): continue
        total += count_combos(goal[len(pattern):])
    return total


def part2():
    return sum(count_combos(goal) for goal in INPUT[1])


def main():
    load_input(use_test_input=False)
    parse_input()
    print('PART 1:', part1())
    print('PART 2:', part2())


if __name__ == "__main__":
    main()

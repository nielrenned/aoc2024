DAY = 5
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
    blank_line = lines.index('')
    
    rules = []
    for line in lines[:blank_line]:
        if line == '': continue
        rules.append(tuple(map(int, line.split('|'))))

    updates = []
    for line in lines[blank_line:]:
        if line == '': continue
        updates.append(tuple(map(int, line.split(','))))
    
    INPUT = rules, updates


def passes_all_rules(update, rules):
    for a, b in rules:
        if a in update and b in update and update.index(a) > update.index(b):
            return False
    return True


def part1():
    rules, updates = INPUT
    return sum(update[len(update)//2] for update in updates if passes_all_rules(update, rules))


def part2():
    rules, updates = INPUT

    total = 0
    for update in updates:
        if passes_all_rules(update, rules): continue

        # For each rule that applies to this update, and each number x in the update, the correct
        # location for x is the number of times it appears as the second number in a rule.
        counts = {x: 0 for x in update}
        for a, b in rules:
            if a not in update or b not in update: continue
            counts[b] += 1
        
        # We don't need the entire list, just the middle number
        for n, i in counts.items():
            if i == len(update) // 2:
                total += n
    
    return total


def main():
    load_input(use_test_input=False)
    parse_input()
    print('PART 1:', part1())
    print('PART 2:', part2())


if __name__ == "__main__":
    main()

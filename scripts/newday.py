import requests
import sys
import os

template = """DAY = {day}
RAW_INPUT = None
INPUT = None


def load_input(use_test_input=False):
    global RAW_INPUT
    path = f'inputs/actual/day{{DAY:02}}.txt'
    if use_test_input:
        path = f'inputs/test/day{{DAY:02}}.txt'
    with open(path) as f:
        RAW_INPUT = f.read()


def parse_input():
    global INPUT
    INPUT = []
    for line in RAW_INPUT.split('\\n'):
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
"""

def main():
    if len(sys.argv) != 2:
        print('Usage: python newday.py <day_num>')
        return
    
    try:
        day_num = int(sys.argv[1])
    except ValueError:
        print(f'Error: {sys.argv[1]} is not an integer.')
        return
    
    solution_filename = f'solutions/day{day_num:02}.py'
    if os.path.exists(solution_filename):
        print(f'Error: {solution_filename} already exists.')
        return
    
    input_filename = f'inputs/actual/day{day_num:02}.txt'
    if os.path.exists(input_filename):
        print(f'Error: {input_filename} already exists.')
        return
    
    test_input_filename = f'inputs/test/day{day_num:02}.txt'
    if os.path.exists(test_input_filename):
        print(f'Error: {test_input_filename} already exists.')
        return
    
    with open(solution_filename, 'w') as f:
        f.write(template.format(day=day_num))
    
    with open(input_filename, 'w'):
        pass

    with open(test_input_filename, 'w'):
        pass

    print('Files created!')


if __name__ == "__main__":
    main()
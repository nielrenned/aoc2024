DAY = 24
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
    lines = RAW_INPUT.split('\n')
    first_blank = lines.index('')

    inital_inputs = {}
    for line in lines[:first_blank]:
        if line == '': continue
        name, value = line.split(': ')
        inital_inputs[name] = int(value)
    
    connections = {}
    for line in lines[first_blank+1:]:
        if line == '': continue
        expression, output = line.split(' -> ')
        connections[output] = expression.split(' ')
    
    INPUT = inital_inputs, connections


def perform(a, op, b):
    if op == 'AND': return a and b
    if op == 'OR': return a or b
    if op == 'XOR': return a ^ b


def part1():
    values, connections = INPUT

    did_change = True
    while did_change:
        did_change = False
        for output, (a, op, b) in connections.items():
            if output in values or not (a in values and b in values): continue
            values[output] = perform(values[a], op, values[b])
            did_change = True
    
    z_outputs = sorted(filter(lambda s: s.startswith('z'), values.keys()))[::-1]
    z_bits = ''.join(str(values[z]) for z in z_outputs)
    return int(z_bits, 2)


def part2():
    pass


def main():
    load_input(use_test_input=False)
    parse_input()
    print('PART 1:', part1())
    # print('PART 2:', part2())


if __name__ == "__main__":
    main()

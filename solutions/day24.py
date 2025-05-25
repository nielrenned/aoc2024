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
        connections[output] = tuple(expression.split(' '))
    
    INPUT = inital_inputs, connections


def perform(a, op, b):
    if op == 'AND': return a and b
    if op == 'OR': return a or b
    if op == 'XOR': return a ^ b


def simulate_to_steady_state(starting_values, connections):
    values = {name: value for name, value in starting_values.items()}

    did_change = True
    while did_change:
        did_change = False
        for output, (a, op, b) in connections.items():
            if output in values or not (a in values and b in values): continue
            values[output] = perform(values[a], op, values[b])
            did_change = True
    
    return values


def part1():
    initial_values, connections = INPUT

    values = simulate_to_steady_state(initial_values, connections)
    
    z_outputs = sorted(filter(lambda s: s.startswith('z'), values.keys()))[::-1]
    z_bits = ''.join(str(values[z]) for z in z_outputs)
    return int(z_bits, 2)


def find_output(a, op, b):
    _, connections = INPUT
    for output in connections:
        if connections[output] == (a, op, b) or connections[output] == (b, op, a):
            return output
    return None


def find_operations_on(wire):
    _, connections = INPUT
    operations = set()
    for a, op, b in connections.values():
        if a == wire or b == wire:
            operations.add(op)
    return operations


def part2():
    given_values, connections = INPUT
    precision = len(given_values)//2 + 1

    last_output = f'z{precision-1:02}'
    
    wrong_outputs = set()
    for output, (a, op, b) in connections.items():
        xy_inputs = {a[0], b[0]} == {'x', 'y'}
        ops_on_output = find_operations_on(output)

        if op == 'AND' and ops_on_output != {'OR'} and {a, b} != {'x00', 'y00'}:
            wrong_outputs.add(output)
        elif op == 'OR' and ops_on_output != {'XOR', 'AND'} and output != last_output:
            wrong_outputs.add(output)
        elif op == 'XOR':
            if not xy_inputs and ops_on_output != set():
                wrong_outputs.add(output)
            elif xy_inputs and ops_on_output != {'XOR', 'AND'} and output != 'z00':
                wrong_outputs.add(output)

    return ','.join(sorted(wrong_outputs))


def main():
    load_input(use_test_input=False)
    parse_input()
    print('PART 1:', part1())
    print('PART 2:', part2())


if __name__ == "__main__":
    main()

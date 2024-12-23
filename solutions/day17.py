DAY = 17
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
    a_line, b_line, c_line, _, prog_line = RAW_INPUT.split('\n')[:5]
    INPUT.append(int(a_line[len('Register X: '):]))
    INPUT.append(int(b_line[len('Register X: '):]))
    INPUT.append(int(c_line[len('Register X: '):]))
    INPUT.append(list(map(int, prog_line[len('Program: '):].split(','))))


def combo_operand(operand, ra, rb, rc):
    if operand == 4: return ra
    if operand == 5: return rb
    if operand == 6: return rc
    return operand


def run_program(ra_init, rb_init, rc_init, prog):
    ra, rb, rc = ra_init, rb_init, rc_init
    ip = 0
    output = []
    while ip < len(prog):
        instr = prog[ip]
        operand = prog[ip+1]

        if instr == 3 and ra != 0: # jnz
            ip = operand
            continue
        
        elif instr == 2: # bst
            rb = combo_operand(operand, ra, rb, rc) % 8
        
        elif instr == 1: # bxl
            rb = rb ^ operand
        elif instr == 4: # bxc
            rb = rb ^ rc
        
        elif instr == 0: # adv
            ra = ra // 2**combo_operand(operand, ra, rb, rc)
        elif instr == 6: # bdv
            rb = ra // 2**combo_operand(operand, ra, rb, rc)
        elif instr == 7: # cdv
            rc = ra // 2**combo_operand(operand, ra, rb, rc)
        
        elif instr == 5: # out
            output.append(combo_operand(operand, ra, rb, rc) % 8)
        
        ip += 2
    return output


def part1():
    return ','.join(map(str, run_program(*INPUT)))


def find_quine(seq, ra_init=0):
    # We can use recursion and the stack to implement backtracking for us!
    if len(seq) == 0: return ra_init

    for delta in range(8):
        ra = ra_init*8 + delta
        # This is a hand-compiled version of one loop of
        # the program defined by my input.
        if ((ra % 8) ^ (ra >> ((ra%8)^2)) ^ 1) % 8 == seq[-1]:
            solution = find_quine(seq[:-1], ra)
            if solution is not None: return solution


def part2():
    return find_quine(INPUT[-1])


def main():
    load_input(use_test_input=True)
    parse_input()
    print('PART 1:', part1())
    print('PART 2:', part2())


if __name__ == "__main__":
    main()

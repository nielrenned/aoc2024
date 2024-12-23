from copy import deepcopy

DAY = 15
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

    map_lines = lines[:first_blank]
    map = []
    robot = None
    for y, line in enumerate(map_lines):
        for x, c in enumerate(line):
            if c == '@': robot = (x, y)
        map.append(list(line))
    
    moves = ''.join(lines[first_blank:])
    INPUT = robot, map, moves


DIRECTIONS = {'<': (-1, 0), '>': (1, 0), '^': (0, -1), 'v': (0, 1)}


def print_map(map):
    for line in map:
        print(''.join(line))
    print()


def check_move_part1(rx, ry, dx, dy, map):
    x, y = rx + dx, ry + dy
    while True:
        if map[y][x] == '.': return True,  (x, y)
        if map[y][x] == '#': return False, (None, None)
        x, y = x + dx, y + dy


def part1():
    (rx, ry), map, moves = INPUT
    map = deepcopy(map) # So we don't mess up part 2

    for move in moves:
        dx, dy = DIRECTIONS[move]
        can_move, (blank_x, blank_y) = check_move_part1(rx, ry, dx, dy, map)
        if not can_move: continue

        # Move everything that's in line
        map[ry][rx] = '.'
        rx, ry = rx + dx, ry + dy
        if map[ry][rx] == 'O':
            map[blank_y][blank_x] = 'O'
        map[ry][rx] = '@'
    
    total = 0
    for y, line in enumerate(map):
        for x, c in enumerate(line):
            if c == 'O':
                total += 100*y + x
    return total


def can_move_part2(rx, ry, dx, dy, map):
    if dy == 0:
        # Left and right movement validation is the same
        can_move, _ = check_move_part1(rx, ry, dx, dy, map)
        return can_move
    else:
        c = map[ry + dy][rx]
        if c == '.': return True
        elif c == '#': return False
        else: return can_move_box_vertically(rx, ry + dy, dy, map)


def can_move_box_vertically(bx, by, dy, map):
    if map[by][bx] == ']': bx -= 1

    lx, ly = bx, by + dy
    left_c = map[ly][lx]
    left_clear = None
    if left_c == '#': left_clear = False
    elif left_c == '.': left_clear = True
    else: left_clear = can_move_box_vertically(lx, ly, dy, map)
    if not left_clear: return False

    rx, ry = lx + 1, ly
    right_c = map[ry][rx]
    right_clear = None
    if right_c == '#': right_clear = False
    elif right_c == '.': right_clear = True
    else: right_clear = can_move_box_vertically(rx, ry, dy, map)
    if not right_clear: return False

    return left_clear and right_clear


def move_box_vertically(bx, by, dy, map):
    if map[by][bx] == ']': bx -= 1

    lx, ly = bx, by + dy
    rx, ry = lx + 1, ly

    if map[ly][lx] != '.': move_box_vertically(lx, ly, dy, map)
    if map[ry][rx] != '.': move_box_vertically(rx, ry, dy, map)

    # Move the box
    map[ly][lx] = map[by][lx]
    map[ry][rx] = map[by][rx]
    map[by][lx] = '.'
    map[by][rx] = '.'


def part2():
    (rx, ry), mini_map, moves = INPUT
    map = []
    for line in mini_map:
        map_line = []
        for c in line:
            if c == '#': map_line.extend('##')
            if c == 'O': map_line.extend('[]')
            if c == '@': map_line.extend('@.')
            if c == '.': map_line.extend('..')
        map.append(map_line)
    rx = 2*rx

    for move in moves:
        dx, dy = DIRECTIONS[move]
        if not can_move_part2(rx, ry, dx, dy, map): continue

        if dy == 0:
            # Find end of stack that we're pushing
            x = rx + dx
            while map[ry][x] != '.': x += dx
            x -= dx

            # Move stack if we need to
            while x != rx:
                map[ry][x + dx] = map[ry][x]
                x -= dx
        elif map[ry + dy][rx] != '.':
            move_box_vertically(rx, ry + dy, dy, map)
            
        # Move the robot
        map[ry + dy][rx + dx] = '@'
        map[ry][rx] = '.'
        rx, ry = rx + dx, ry + dy
    
    total = 0
    for y, line in enumerate(map):
        for x, c in enumerate(line):
            if c == '[':
                total += 100*y + x
    return total


def main():
    load_input(use_test_input=False)
    parse_input()
    print('PART 1:', part1())
    print('PART 2:', part2())


if __name__ == "__main__":
    main()

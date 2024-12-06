DAY = 6
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
    obstacles = set()
    guard = None
    w = 0
    h = 0

    for y, line in enumerate(RAW_INPUT.split('\n')):
        if line == '': continue
        h = max(h, y+1)
        for x, c in enumerate(line):
            if c == '#': obstacles.add((x, y))
            if c == '^': guard = (x, y)
            w = max(w, x+1)
    
    INPUT = w, h, guard, obstacles


DIRECTIONS = [(0, -1), (1, 0), (0, 1), (-1, 0)]
PART_1_LOCATIONS = None


def guard_step(direction, position, obstacles):
    next_position = (position[0] + direction[0], position[1] + direction[1])
    if next_position in obstacles:
        direction_index = DIRECTIONS.index(direction)
        new_direction = DIRECTIONS[(direction_index + 1) % 4]
        return guard_step(new_direction, position, obstacles)
    else:
        return direction, next_position


def part1():
    global PART_1_LOCATIONS
    w, h, (gx, gy), obstacles = INPUT
    direction = DIRECTIONS[0]
    locations = set()
    while 0 <= gx < w and 0 <= gy < h:
        locations.add((gx, gy))
        direction, (gx, gy) = guard_step(direction, (gx, gy), obstacles)
    PART_1_LOCATIONS = locations
    return len(locations)


def part2():
    w, h, (start_x, start_y), start_obstacles = INPUT
    count = 0
    for x, y in PART_1_LOCATIONS:
        if (x, y) == (start_x, start_y): continue
        obstacles = start_obstacles | {(x, y)}
        direction = DIRECTIONS[0]
        locations = set()
        gx, gy = start_x, start_y
        while 0 <= gx < w and 0 <= gy < h:
            if (direction, gx, gy) in locations:
                count += 1
                break
            locations.add((direction, gx, gy))
            direction, (gx, gy) = guard_step(direction, (gx, gy), obstacles)
    return count

def main():
    load_input(use_test_input=False)
    parse_input()
    print('PART 1:', part1())
    print('PART 2:', part2())


if __name__ == "__main__":
    main()

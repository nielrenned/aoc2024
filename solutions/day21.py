from functools import cache
from queue import Queue

DAY = 21
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


DIRECTIONS = [(0, -1), (1, 0), (0, 1), (-1, 0)]

DIRECTIONAL_KEYPAD = (
    (None, '^', 'A'),
    ('<',  'v', '>')
)
NUMERIC_KEYPAD = (
    ('7',  '8', '9'),
    ('4',  '5', '6'),
    ('1',  '2', '3'),
    (None, '0', 'A')
)

DIRECTIONAL_ACTIVATE_COORD = (2, 0)
NUMERIC_ACTIVATE_COORD = (2, 3)

NUMERIC_COORD_LOOKUP = {c: (x, y) for y, row in enumerate(NUMERIC_KEYPAD) for x, c in enumerate(row) if c is not None}
DELTA_TO_DIR_BUTTON = {
    (-1, 0): (0, 1),
    (1, 0):  (2, 1),
    (0, -1): (1, 0),
    (0, 1):  (1, 1)
}


def path_to_directional_key_coords(path):
    coords = [DIRECTIONAL_ACTIVATE_COORD]
    for i in range(1, len(path)):
        p1, p2 = path[i-1:i+1]
        dx, dy = p2[0] - p1[0], p2[1] - p1[1]
        coords.append(DELTA_TO_DIR_BUTTON[(dx, dy)])
    coords.append(DIRECTIONAL_ACTIVATE_COORD)
    return coords


def get_all_shortest_paths(p1, p2, keypad):
    if p1 == p2: return [[]]
    
    min_length = None
    routes = []
    w, h = len(keypad[0]), len(keypad)

    q = Queue()
    q.put(([p1], 0))
    while not q.empty():
        route, length = q.get()
        if length == min_length: continue
        for dx, dy in DIRECTIONS:
            x, y = route[-1]
            nx, ny = x + dx, y + dy
            if not (0 <= nx < w and 0 <= ny < h) or keypad[ny][nx] is None:
                continue
            elif (nx, ny) in route:
                continue
            elif (nx, ny) == p2:
                if min_length is None: min_length = length + 1
                routes.append(route + [p2])
            else:
                q.put((route + [(nx, ny)], length + 1))
    return routes


@cache
def shortest_directional_pad_sequence_length(p1, p2, robot_number, initial_keypad=DIRECTIONAL_KEYPAD):
    if robot_number == 0 or p1 == p2: return 1

    min_length = 10**100
    for path in get_all_shortest_paths(p1, p2, initial_keypad):
        coords = path_to_directional_key_coords(path)
        length = sum(shortest_directional_pad_sequence_length(coords[i-1], coords[i], robot_number-1) for i in range(1, len(coords)))
        min_length = min(min_length, length)    
    return min_length


def shortest_numeric_pad_sequence_length(code, num_robots):
    coords = [NUMERIC_ACTIVATE_COORD] + [NUMERIC_COORD_LOOKUP[c] for c in code]
    return sum(shortest_directional_pad_sequence_length(coords[i-1], coords[i], num_robots+1, NUMERIC_KEYPAD) for i in range(1, len(coords)))


def part1():
    return sum(shortest_numeric_pad_sequence_length(code, 2) * int(code[:3]) for code in INPUT)


def part2():
    return sum(shortest_numeric_pad_sequence_length(code, 25) * int(code[:3]) for code in INPUT)


def main():
    load_input(use_test_input=False)
    parse_input()
    print('PART 1:', part1())
    print('PART 2:', part2())


if __name__ == "__main__":
    main()

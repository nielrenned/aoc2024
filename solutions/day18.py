from day08 import Vector as Point
from queue import Queue


DAY = 18
RAW_INPUT = None
INPUT = None


def load_input(use_test_input=False):
    global RAW_INPUT, INPUT
    path = f'inputs/actual/day{DAY:02}.txt'
    INPUT = [70, 1024]
    if use_test_input:
        INPUT = [6, 12]
        path = f'inputs/test/day{DAY:02}.txt'
    with open(path) as f:
        RAW_INPUT = f.read()


def parse_input():
    global INPUT
    bytes = []
    for line in RAW_INPUT.split('\n'):
        if line == '': continue
        x, y = list(map(int, line.split(',')))
        bytes.append(Point(x, y))
    INPUT.append(bytes)


def bfs(walls):
    width, _, _ = INPUT
    start = Point(0, 0)
    end = Point(width, width)

    q = Queue()
    q.put(start)
    seen = {start}
    path_map = dict()
    while not q.empty():
        u = q.get()
        if u == end:
            # Determine path length
            total = 0
            while u != start:
                u = path_map[u]
                total += 1
            return total

        for delta in [Point(1, 0), Point(0, -1), Point(-1, 0), Point(0, 1)]:
            n = u + delta
            if n in walls or n in seen: continue
            if not (0 <= n.x <= width and 0 <= n.y <= width): continue
            
            seen.add(n)
            path_map[n] = u
            q.put(n)
    
    # We couldn't find a path
    return float('inf')


def part1():
    _, bound, bytes = INPUT
    walls = set(bytes[:bound])
    return bfs(walls)


def part2():
    _, bound, bytes = INPUT
    min, max = bound+1, len(bytes)

    # Binary search
    while min != max:
        current = (min + max + 1) // 2 # +1 because we want to round up
        walls = set(bytes[:current])
        
        d = bfs(walls)
        if d == float('inf'):
            max = current - 1
        else:
            min = current
    
    p = bytes[min]
    return f'{p.x},{p.y}'


def main():
    load_input(use_test_input=False)
    parse_input()
    print('PART 1:', part1())
    print('PART 2:', part2())


if __name__ == "__main__":
    main()

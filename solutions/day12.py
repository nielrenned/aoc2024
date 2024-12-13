from day08 import Vector as Point
from queue import Queue
from itertools import combinations

DAY = 12
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


def inbounds(p):
    w, h = len(INPUT[0]), len(INPUT)
    return (0 <= p.x < w) and (0 <= p.y < h)


def find_region(starting_point: Point):
    DIRECTIONS = [Point(1, 0), Point(0, -1), Point(-1, 0), Point(0, 1)]
    region_letter = INPUT[starting_point.y][starting_point.x]
    region = {starting_point}
    fencing = set()

    # Region fill
    search_queue = Queue()
    search_queue.put(starting_point)
    while not search_queue.empty():
        p = search_queue.get()
        for v in DIRECTIONS:
            n = p + v
            if n in region: continue
            if not inbounds(n) or INPUT[n.y][n.x] != region_letter:
                perp_v = Point(v.y, v.x)
                # Anywhere there isn't a  valid neighbor, there _is_ fencing. The coefficient
                # of 0.25 on v ensures that fencing doesn't mistakenly become collinear. The
                # coefficient of 0.75 on perp_v ensures collinear fence segments overlap.
                fencing.add(frozenset([p + 0.25*v + 0.75*perp_v, p + 0.25*v - 0.75*perp_v]))
            else:
                region.add(n)
                search_queue.put(n)
    return region, fencing


ALL_REGIONS = []


def part1():
    # We only want to calculate the regions once
    global ALL_REGIONS
    w, h = len(INPUT[0]), len(INPUT)
    all_points = set(Point(x, y) for x in range(w) for y in range(h))
    while len(all_points) > 0:
        region, fencing = find_region(all_points.pop())
        ALL_REGIONS.append((region, fencing))
        all_points -= region
    
    return sum(len(region) * len(fencing) for region, fencing in ALL_REGIONS)


def join_segments_if_possible(a, b):
    # We know all segments are either horizontal or vertical, so we can simplify our logic
    a0, a1 = list(a)
    b0, b1 = list(b)

    if a0.x == a1.x == b0.x == b1.x:
        if min(a0.y, a1.y) < min(b0.y, b1.y) < max(a0.y, a1.y) or min(b0.y, b1.y) < min(a0.y, a1.y) < max(b0.y, b1.y):
            y_values = [a0.y, a1.y, b0.y, b1.y]
            return frozenset([Point(a0.x, min(y_values)), Point(a0.x, max(y_values))])
    if a0.y == a1.y == b0.y == b1.y:
        if min(a0.x, a1.x) < min(b0.x, b1.x) < max(a0.x, a1.x) or min(b0.x, b1.x) < min(a0.x, a1.x) < max(b0.x, b1.x):
            x_values = [a0.x, a1.x, b0.x, b1.x]
            return frozenset([Point(min(x_values), a0.y), Point(max(x_values), a0.y)])
    
    return None


def part2():
    total = 0
    # Repeatedly merge pairs of segments until there are no more to merge.
    for region, fencing in ALL_REGIONS:
        while True:
            for a, b in combinations(fencing, 2):
                if c := join_segments_if_possible(a, b):
                    fencing.remove(a)
                    fencing.remove(b)
                    fencing.add(c)
                    break
            else:
                # We couldn't combine any two fence segments
                break

        total += len(region)*len(fencing)
    return total


def main():
    load_input(use_test_input=False)
    parse_input()
    print('PART 1:', part1())
    print('PART 2:', part2())


if __name__ == "__main__":
    main()

from day08 import Vector
from collections import defaultdict
from itertools import combinations
Point = Vector

DAY = 16
RAW_INPUT = None
INPUT = None

DIRECTIONS = [Vector(1, 0), Vector(0, -1), Vector(0, 1), Vector(-1, 0)]


def load_input(use_test_input=False):
    global RAW_INPUT
    path = f'inputs/actual/day{DAY:02}.txt'
    if use_test_input:
        path = f'inputs/test/day{DAY:02}.txt'
    with open(path) as f:
        RAW_INPUT = f.read()


def parse_input():
    global INPUT
    map = set()
    start = None
    end = None
    for y, line in enumerate(RAW_INPUT.split('\n')):
        if line == '': continue
        for x, c in enumerate(line):
            if c == '#': continue
            if c == 'S': start = Point(x, y)
            if c == 'E': end = Point(x, y)
            map.add(Point(x, y))
    INPUT = start, end, map


def add_edge(edges, p1, p2, w, via=None):
    edges[p1][p2] = w, via
    edges[p2][p1] = w, via


def solve():
    start, end, map = INPUT

    # Build edge-weighted graph of all non-intersection points
    points = set()
    edges = defaultdict(lambda: defaultdict(lambda: float('inf')))
    for p in map:
        neighbors = [p + v for v in DIRECTIONS if (p + v) in map]
        if len(neighbors) == 1: # Dead end
            points.add(p)
            add_edge(edges, p, neighbors[0], 1)
        elif len(neighbors) == 2: # Maybe corner
            n1, n2 = neighbors
            if n1.x == n2.x or n1.y == n2.y: # Not a corner
                points.add(p)
                add_edge(edges, p, n1, 1)
                add_edge(edges, p, n2, 1)
            else: # Corner, need to add turning cost and jump intersection
                add_edge(edges, n1, n2, 1002, p)
        elif len(neighbors) >= 3:
            # T or 4-way: jump intersection and add turning cost if necessary
            for n1, n2 in combinations(neighbors, 2):
                if n1.x == n2.x or n1.y == n2.y:
                    add_edge(edges, n1, n2, 2, p)
                else:
                    add_edge(edges, n1, n2, 1002, p)
    
    # Add in the start and end points
    # This assumes start is the an L-shaped corner and end is in a ┐-shaped corner
    # and that both are not next to an intersection.
    points.add(start)
    add_edge(edges, start, start + Vector(0, -1), 1001) # We start facing east
    add_edge(edges, start, start + Vector(1, 0), 1)
    
    points.add(end)
    add_edge(edges, end, end + Vector(0, 1), 1)
    add_edge(edges, end, end + Vector(-1, 0), 1)

    # Run Djikstra's (all shortest paths variant)
    distance_to = defaultdict(lambda: float('inf'))
    previous = defaultdict(set)
    queue = points.copy()
    distance_to[start] = 0
    while len(queue) > 0:
        u = None
        best_dist = float('inf')
        for candidate in queue:
            if distance_to[candidate] < best_dist:
                best_dist = distance_to[candidate]
                u = candidate
        queue.remove(u)
        
        for v in edges[u]:
            if v not in queue: continue
            cost = distance_to[u] + edges[u][v][0]
            if cost < distance_to[v]:
                distance_to[v] = cost
                previous[v] = {u}
            if cost == distance_to[v]:
                previous[v].add(u)
    
    # Reconstruct all paths
    path_points = {end}
    q = {end}
    while len(q) > 0:
        u = q.pop()
        for prev in previous[u]:
            if (via := edges[u][prev][1]) is not None:
                path_points.add(via)
            path_points.add(prev)
            q.add(prev)

    return distance_to[end], len(path_points)


def main():
    load_input(use_test_input=False)
    parse_input()
    part1_answer, part2_answer = solve()
    print('PART 1:', part1_answer)
    print('PART 2:', part2_answer)


if __name__ == "__main__":
    main()

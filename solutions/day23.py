from collections import defaultdict

DAY = 23
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
    vertices = set()
    edges = defaultdict(set)
    for line in RAW_INPUT.split('\n'):
        if line == '': continue
        a, b = line.split('-')
        vertices.add(a)
        vertices.add(b)
        edges[a].add(b)
        edges[b].add(a)
    
    INPUT = vertices, edges


def part1():
    vertices, edges = INPUT
    
    triplets = set()
    for u in vertices:
        for v in edges[u]:
            for w in edges[u] & edges[v]:
                if u.startswith('t') or v.startswith('t') or w.startswith('t'):
                    triplets.add(frozenset((u,v,w)))
    
    return len(triplets)


def find_a_maximal_clique(R, P, X, edges):
    if len(P) == 0:
        if len(X) == 0: return R
        else: return set()

    
    pivot = sorted(P, key=lambda u: len(edges[u]))[-1]
    maximal = set()

    for v in P - edges[pivot]:
        result = find_a_maximal_clique(R | {v}, P & edges[v], X & edges[v], edges)
        if len(result) > len(maximal): maximal = result
        P -= {v}
        X |= {v}
    
    return maximal


def part2():
    vertices, edges = INPUT
    clique = find_a_maximal_clique(set(), vertices, set(), edges)
    return ','.join(sorted(clique))


def main():
    load_input(use_test_input=False)
    parse_input()
    print('PART 1:', part1())
    print('PART 2:', part2())


if __name__ == "__main__":
    main()

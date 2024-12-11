from collections import defaultdict
from bisect import insort

DAY = 9
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
    INPUT = list(map(int, RAW_INPUT))


def part1():
    file_id = 0
    disk = []
    for i, size in enumerate(INPUT):
        if i % 2 == 0:
            disk.extend([file_id]*size)
            file_id += 1
        else:
            disk.extend([-1]*size)

    index = len(disk) - 1
    dest = 0
    while dest < index:
        while disk[dest] != -1 and dest < index:  dest += 1
        while disk[index] == -1 and dest < index: index -= 1
        disk[dest] = disk[index]
        disk[index] = -1
    
    return sum(i*v for i, v in enumerate(disk[:index]))


def part2():
    files = {}
    empty_spans = defaultdict(list)
    file_id = 0
    index = 0
    for i, size in enumerate(INPUT):
        if i % 2 == 0:
            if size > 0:
                files[file_id] = (index, size)
            file_id += 1
        elif size > 0:
            empty_spans[size].append(index)
        index += size
    
    max_file_id = file_id - 1
    for file_id in range(max_file_id, -1, -1):
        file_index, file_size = files[file_id]
        # Find left-most empty space
        new_index, empty_size = min(((empty_spans[size][0], size) for size in empty_spans if size >= file_size), key=lambda t: t[0], default=(None, None))
        if new_index is None or new_index >= file_index: continue

        files[file_id] = (new_index, file_size)
        del empty_spans[empty_size][0]
        if empty_size > file_size:
            insort(empty_spans[empty_size - file_size], new_index + file_size)
    
    total = 0
    for file_id, (index, size) in files.items():
        total += file_id*sum(range(index, index + size))
    return total


def main():
    load_input(use_test_input=False)
    parse_input()
    print('PART 1:', part1())
    print('PART 2:', part2())


if __name__ == "__main__":
    main()

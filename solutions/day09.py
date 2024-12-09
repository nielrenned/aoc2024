from collections import namedtuple

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


def find_with_predicate(iterable, pred, default_index=-1):
    return next(((i, e) for i, e in enumerate(iterable) if pred(e)), (default_index, None))


def part2():
    Span = namedtuple('Block', ['id', 'size'])

    # Build the spans
    file_id = 0
    spans = []
    for i, size in enumerate(INPUT):
        if i % 2 == 0:
            if size > 0:
                spans.append(Span(file_id, size))
            file_id += 1
        elif size > 0:
            spans.append(Span(-1, size))
    
    # Condense the span
    max_file_id = file_id - 1 # The loop ends with file_id overcounted by 1
    for file_id in range(max_file_id, -1, -1):
        file_index, file_span = find_with_predicate(spans, lambda b: b.id == file_id)
        if file_span is None: continue
        empty_index, empty_span = find_with_predicate(spans, lambda b: b.id == -1 and b.size >= file_span.size)
        if empty_span is None or file_index < empty_index: continue

        # Move the span
        spans[empty_index] = file_span
        spans[file_index] = Span(-1, file_span.size)
        if empty_span.size > file_span.size:
            remainder = Span(-1, empty_span.size - file_span.size)
            spans.insert(empty_index + 1, remainder)
        
    total = 0
    i = 0
    for span in spans:
        if span.id != -1: total += sum(range(i, i + span.size)) * span.id
        i += span.size
    return total


def main():
    load_input(use_test_input=False)
    parse_input()
    print('PART 1:', part1())
    print('PART 2:', part2())


if __name__ == "__main__":
    main()

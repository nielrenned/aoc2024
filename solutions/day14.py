import operator
import re

from functools import reduce
from day13 import extended_gcd

DAY = 14
RAW_INPUT = None
INPUT = None


def load_input(use_test_input=False):
    global RAW_INPUT, INPUT
    INPUT = [101, 103]
    path = f'inputs/actual/day{DAY:02}.txt'
    if use_test_input:
        INPUT = [11, 7]
        path = f'inputs/test/day{DAY:02}.txt'
    with open(path) as f:
        RAW_INPUT = f.read()


def parse_input():
    global INPUT
    robots = []
    velocities = []
    for line in RAW_INPUT.split('\n'):
        if line == '': continue
        px, py, vx, vy = tuple(map(int, re.findall(r'p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)', line)[0]))
        robots.append([px, py])
        velocities.append([vx, vy])
    INPUT.append(robots)
    INPUT.append(velocities)


def print_robots(robots):
    w, h, _, _ = INPUT
    s = ''
    for y in range(h):
        for x in range(w):
            robot_count = sum(1 for px, py in robots if px == x and py == y)
            if robot_count != 0:
                s += str(robot_count) + ' '
            else:
                s += '. '
        s += '\n'
    print(s, end='')
    print("Zoom out to see the tree!")


def move_robots_in_place(robots):
    w, h, _, velocities = INPUT
    for i, (px, py) in enumerate(robots):
        vx, vy = velocities[i]
        robots[i][0] = (px + vx) % w
        robots[i][1] = (py + vy) % h


def part1():
    w, h, robots, _ = INPUT
    robots = [robot[:] for robot in robots] # Copy so we don't mess up part 2
    for _ in range(100):
        move_robots_in_place(robots)
    
    half_w = w // 2
    half_h = h // 2
    quadrant_counts = [0, 0, 0, 0]
    for px, py in robots:
        if px < half_w:
            if py < half_h: quadrant_counts[0] += 1
            if py > half_h: quadrant_counts[1] += 1
        if px > half_w:
            if py < half_h: quadrant_counts[2] += 1
            if py > half_h: quadrant_counts[3] += 1
    
    return reduce(operator.mul, quadrant_counts, 1)


def variance(data):
    mean = sum(data)/len(data)
    return sum((d-mean)*(d-mean) for d in data)


def part2():
    w, h, robots, _ = INPUT
    best_x_variance = 99999999
    best_x_index = 0
    best_y_variance = 99999999
    best_y_index = 0

    for i in range(max(w, h)):
        move_robots_in_place(robots)
        if i < w and (x_variance := variance([robot[0] for robot in robots])) < best_x_variance:
            best_x_variance = x_variance
            best_x_index = i+1
        if i < h and (y_variance := variance([robot[1] for robot in robots])) < best_y_variance:
            best_y_variance = y_variance
            best_y_index = i+1
    
    # Chinese remainder theorem
    _, u, v = extended_gcd(w, h)
    picture_index = (best_x_index * v * h + best_y_index * u * w) % (w*h)
    for _ in range(picture_index - max(w, h)):
        move_robots_in_place(robots)
    print_robots(robots)
    return picture_index


def main():
    load_input(use_test_input=False)
    parse_input()
    print('PART 1:', part1())
    print('PART 2:', part2())


if __name__ == "__main__":
    main()

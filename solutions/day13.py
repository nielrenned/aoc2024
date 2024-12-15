import re
import math
from fractions import Fraction

DAY = 13
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
    for i in range(0, len(lines), 4):
        ax, ay = map(int, re.findall(r'Button A: X\+(\d+), Y\+(\d+)', lines[i])[0])
        bx, by = map(int, re.findall(r'Button B: X\+(\d+), Y\+(\d+)', lines[i+1])[0])
        x, y = map(int, re.findall(r'Prize: X=(\d+), Y=(\d+)', lines[i+2])[0])
        INPUT.append((ax, ay, bx, by, x, y))


def extended_gcd(a, b):
    old_r, r = a, b
    old_s, s = 1, 0
    old_t, t = 0, 1
    
    while r != 0:
        q = old_r // r
        old_r, r = r, old_r - q * r
        old_s, s = s, old_s - q * s
        old_t, t = t, old_t - q * t

    return old_r, old_s, old_t


def solve_simple_linear_diophantine(a, b, c):
    # Solves ax + by = c
    # Returns a0, a0_inc, b0, b0_inc where solutions are of the form
    #   a*(a0 + k*a0_inc) + b*(b0 + k*b0_inc) = c
    # for all integers k.
    g, g_a, g_b = extended_gcd(a, b)
    if c % g != 0: return None, None, None, None
    return g_a * (c // g), b // g, g_b * (c // g), -a // g


def find_non_negative_solution_set(a, b, c):
    # Solves ax + by = c
    # Returns a0, a0_inc, b0, b0_inc, k_bound where solutions are of the form
    #   a*(a0 + k*a0_inc) + b*(b0 + k*b0_inc) = c
    #   for 0 <= k <= k_bound
    # guaranteeing that a0 + k*a0_inc and b0 + k*b0_inc are both non-negative.
    a0, a0_inc, b0, b0_inc = solve_simple_linear_diophantine(a, b, c)
    if a0 is None: return None, None, None, None, None, None

    # When computing the bounds, we have to be careful about the division,
    # because dividing by a negative flips the inequality.
    lb = float('-inf')
    if a0_inc < 0: lb = max(lb, math.ceil(a0/a0_inc))
    if b0_inc < 0: lb = max(lb, math.ceil(b0/b0_inc))

    ub = float('inf')
    if a0_inc > 0: ub = min(ub, math.floor(a0/a0_inc))
    if b0_inc > 0: ub = min(ub, math.floor(b0/b0_inc))
                            
    if ub < lb: return None, None, None, None, None, None
    return a0, a0_inc, b0, b0_inc, lb, ub


def find_minimal_cost(ax, ay, bx, by, x, y):
    # Find combinations for x and y separately
    x_a0, x_a0_inc, x_b0, x_b0_inc, x_k_lb, x_k_ub = find_non_negative_solution_set(ax, bx, x)
    y_a0, y_a0_inc, y_b0, y_b0_inc, y_k_lb, y_k_ub = find_non_negative_solution_set(ay, by, y)
    if x_a0 is None or y_a0 is None: return 0

    # These are the expressions computed by hand to solve the following system.
    #     x_a0 + x_a0_inc*x_k == y_a0 + y_a0_inc*y_k
    #     x_b0 + x_b0_inc*x_k == y_b0 + y_b0_inc*y_k
    # We're using the Fraction class to avoid floating-point arithmetic.
    y_k = Fraction(((y_a0 - x_a0) + Fraction(x_a0_inc, x_b0_inc)*(x_b0 - y_b0)), (y_a0_inc - x_a0_inc*Fraction(y_b0_inc, x_b0_inc)))
    x_k = Fraction((y_a0_inc * y_k + x_a0 - y_a0), x_a0_inc)

    if not (y_k_lb <= y_k <= y_k_ub and x_k_lb <= x_k <= x_k_ub): return 0 # The solution to the system requires negative button presses
    if not (x_k.denominator == 1 and y_k.denominator == 1): return 0 # The solution to the system requires fractional button presses
    return -(3*x_a0_inc + x_b0_inc)*x_k + (3*x_a0 + x_b0)


def part1():
    return sum(find_minimal_cost(*machine) for machine in INPUT)


def part2():
    return sum(find_minimal_cost(ax, ay, bx, by, x + 10000000000000, y + 10000000000000) for ax, ay, bx, by, x, y in INPUT)


def main():
    load_input(use_test_input=False)
    parse_input()
    print('PART 1:', part1())
    print('PART 2:', part2())


if __name__ == "__main__":
    main()

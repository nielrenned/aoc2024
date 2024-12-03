# Advent of Code 2024

Solutions to the problems from [Advent of Code 2024](https://adventofcode.com/2024).

Welp, I didn't quite achieve my goal from [last year](https://github.com/nielrenned/aoc2023), but that's okay! It was lofty. We'll see how far I get this year.

|       S       |       M       |       T       |       W       |       T       |       F       |       S       |
|:-------------:|:-------------:|:-------------:|:-------------:|:-------------:|:-------------:|:-------------:|
|  [1](#day-1)  |  [2](#day-2)  |  [3](#day-3)  |   4           |   5           |   6           |   7           |
|   8           |   9           |  10           |  11           |  12           |  13           |  14           |
|  15           |  16           |  17           |  18           |  19           |  20           |  21           |
|  22           |  23           |  24           |  25           |               |               |               |

# Day 1

Python did most of the heavy lifting here. The list comprehensions make it short and sweet as well. Not much else to say really; we're starting off easy, as usual.

# Day 2

Factoring out the inner loops made Day 2's solution functions into one-liners, again using list comprehension. For Part 2, I was initially trying to think of some complicated solution to keep track of how many potential flaws there were. But computers are so fast and the input is relatively small, so I went with the brute force solution, which finished super quickly. A big lesson I've learned lately is to do the simplest thing first and then optimize later if necessary.

The simplicity of these first two days has me scared for the later days...

# Day 3

The wording in this problem kind of screamed "regular expression" to me, particularly "instructions like `mul(X,Y)`, where `X` and `Y` are each 1-3 digit numbers." This converts directly to the regex `mul\((\d{1,3}),(\d{1,3})\)`, which even has capture instructions to pick out `X` and `Y`. This makes Part 1 essentially a one-liner.

Part 2 required slightly more work, but we can add some or-statements to our regex to pickup the `do()` and `don't()` parts. Then we just iterate through all the matches and flip a flag that enables or disabled the sum.
# Advent of Code 2024

Solutions to the problems from [Advent of Code 2024](https://adventofcode.com/2024).

Welp, I didn't quite achieve my goal from [last year](https://github.com/nielrenned/aoc2023), but that's okay! It was lofty. We'll see how far I get this year.

|       S       |       M       |       T       |       W       |       T       |       F       |       S       |
|:-------------:|:-------------:|:-------------:|:-------------:|:-------------:|:-------------:|:-------------:|
|  [1](#day-1)  |  [2](#day-2)  |  [3](#day-3)  |  [4](#day-4)  |  [5](#day-5)  |  [6](#day-6)  |  [7](#day-7)  |
|  [8](#day-8)  |  [9](#day-9)  | [10](#day-10) | [11](#day-11) | [12](#day-12) | [13](#day-13) | [14](#day-14) |
|  15           |  16           |  17           |  18           |  19           |  20           |  21           |
|  22           |  23           |  24           |  25           |               |               |               |

# Day 1

Python did most of the heavy lifting here. The list comprehensions make it short and sweet as well. Not much else to say really; we're starting off easy, as usual.

# Day 2

Factoring out the inner loops made Day 2's solution functions into one-liners, again using list comprehension. For Part 2, I was initially trying to think of some complicated solution to keep track of how many potential flaws there were. But computers are so fast and the input is relatively small, so I went with the brute force solution, which finished super quickly. A big lesson I've learned lately is to do the simplest thing first and then optimize later if necessary.

The simplicity of these first two days has me scared for the later days...

# Day 3

The wording in this problem kind of screamed "regular expression" to me, particularly "instructions like `mul(X,Y)`, where `X` and `Y` are each 1-3 digit numbers. This converts directly to the regex `mul\((\d{1,3}),(\d{1,3})\)`, which even has capture instructions to pick out `X` and `Y`. This makes Part 1 essentially a one-liner.

Part 2 required slightly more work, but we can add some or-statements to our regex to pickup the `do()` and `don't()` parts. Then we just iterate through all the matches and flip a flag that enables or disabled the sum.

# Day 4

Today was word-search, for which I think the naive algorithm runs in $O(n m k)$ time (where the grid is $n\times m$ and the word is length $k$). That's, well, not _great_, but thankfully the puzzle input is small enough that it doesn't matter. 

I originally wrote the code for Part 1 more efficiently, but it was _four_ nested loops with an if-statement inside for a total of 5 indentations. Using `product.itertools` could get it down to 3 before getting too ugly, but I still didn't like it. So I decided to switch to something that is definitely less efficient, but reads much more nicely. For Part 2, I didn't bother trying to be efficient, and wrote legibly on the first go-round. I think this instinct has come from collaborating with people at work, where readability is king over slight efficiency gains.

# Day 5

Part 1 was pretty straightforward. Factoring out the check for one row made it essentially a one liner. Python list comprehensions are pretty neat, but I probably use them a little too liberally.

For Part 2, my initial solution was to just swap any pair of numbers that were out-of-order. Unfortunately, this doesn't quite work, even if you repeat the process. However, the problem implies that there is exactly _one_ correct ordering for each list, which means there must be a rule for every pair of numbers in the list. That means we can figure out the correct index for any number in the list by counting how many times it appears in the second position in a rule! 

For example, let's use the list `[61,13,29]`. The rules that apply are `61|29`, `61|13`, and `29|13`. In these three rules, `61` is second `0` times, `29` is second `1` times, and `13` is second `2` times. So the correct order must be `[61, 29, 13]`! I love the simplicity of this correction.

# Day 6

This is a classic Advent of Code-style problem: grid-walking! Part 1 was straightforward (_get it?_); it was just implementing the guard logic. There's the potential for a misstep that's a literal corner case:

```
.##
.^#
...
```

This guard needs to turn right _twice_ before taking another step.

Part 2 wasn't that much harder, but I thought I'd done something wrong at first. I implemented a brute-force solution and it was taking a while to run, so I thought I'd written an infinite loop somewhere. But it turns out that it was correct, but slow. It ran in a little under a minute on my machine. A few people on the subreddit pointed out that it only makes sense to put new obstacles on the path the guard walked, which in hindsight, should've been obvious. After adding this optimization in, the brute-force solution runs in about 10 seconds.

One other notable strategy: in part 2, you actually don't need to track all previous positions and orientations to know if the guard is looping. We can instead just count the steps and use the pigeonhole principle: if the guard has taken more than $4 \cdot width \cdot height$ steps without leaving the grid, she _must_ be looping (the 4 is there to account for the 4 possible directions). For me, this ended up being slower than just tracking all visited locations in a `set`, but it's interesting nonetheless.

# Day 7

Yet again, I was kind of worried that a brute-force approach wouldn't work here, but it's only Day 7, so we didn't need to do anything fancy. On my laptop (M3 MacBook Air), Part 1 finished almost instantly and Part 2 finished in less than 10 seconds. And Python's stdlib, as usual, did most of the heavy lifting for us. And once we factored out the common logic, the code for both parts is nearly identical! There are almost certainly optimizations that could be made here, but it finished so fast, it's not worth it.

# Day 8

I initially wrote this without writing a `Vector` class and just using tuples, but it looked so ugly I decided to rework it. The overall code is longer, but who knows, maybe this `Vector` class will come in handy on a later problem. You can see the before-and-after by picking out the commits from the log.

Outside of writing the `Vector` class (and remembering to give it a `__hash__` and `__eq__` method), today's problem was straightforward. We get to take advantage of my favorite class, `defaultdict`, to make parsing the input very straightforward. And we use a `dict` to separate out all the relevant points as we parse. Then we can use the great `itertools` hammer to get all possible pairs. I initially used `combinations`, but `permutations` actually simplifies the code, as we can just focus on moving in one direction. Then we can use a `set` to make sure we only capture each antinode once. Man! The Python standard library is so good.

# Day 9

For Part 1, I again just decided to try the brute-force method and it finished instantaneously, so I went with it. The only real trick here was using two pointers, `dest` and `index`, to keep track of the current destination and file blocks, respectively. One quirk here is that the order in which you move these pointers matters. Moving the `index` pointer first results in an off-by-one error.

~~For Part 2, I used a `namedtuple` to create a very simple class to keep track of spans of blocks rather than pieces of files. This preprocessing allows finding large enough empty spaces very quickly. This does seem inefficient though, as it takes a little over 10 seconds to compute on my laptop. But that's not _that_ long, so I don't feel like reworking it. I think the slowness is in the `find_with_predicate` calls.~~

~~For posterity's sake:~~ I think the fast solution would be to have two `dict`s. One that keeps the index and size of each file, keyed to its ID, and one keeps lists of empty block indices, keyed to their size. Then to find empty blocks, you can take the minimum index of the block sizes that are large enough, and then carefully move numbers around in the lists in the second `dict` to keep everything correct. Then "moving" a block would be very fast.

Okay, I ended up writing out the optimized solution the next day. It runs almost instantaneously on the actual puzzle input, and even finishes in less than a second with `/u/Standard_Bar8402`'s [pathologic inputs](https://www.reddit.com/r/adventofcode/comments/1haauty/2024_day_9_part_2_bonus_test_case_that_might_make/). I spent way too long debugging an issue where I was moving files to the "right" because I forgot to check that the new index was to the "left," but otherwise the solution worked flawlessly. My original solution is still in the commit labeled "Day 9 Finished," if you can be bothered to go digging for it.

# Day 10

Initially, I wrote two different functions to solve Part 1 and Part 2. But after solving Part 2, I realized we use its solution to compute Part 1 as well. So I rewrote the solutions to find all paths just once, and then use that solution to calculate the answers for Part 1 and Part 2. The only other interesting thing here is this is a breadth-first search, which means we can write a recursive function and it ends up being pretty clean.

# Day 11

Experience paid off here! Some people have said it reminds them of the [lanternfish](https://adventofcode.com/2021/day/6), but it reminded me more of the [polymers](https://adventofcode.com/2021/day/14) problem from the same year. He was also quite tricky with the red herring that their order is preserved! I realized that it didn't matter in Part 1, but I _was_ worried that it would matter in Part 2. Regardless, I decided to store the numbers in a `dict` from the get-go, because I knew that would be more efficient in Part 1. And it turned out to be the right idea! What a nice little throwback. (For completeness: since order doesn't matter, we can just keep track of how many of each stone exists between each blink, i.e. a `dict` of the form `{value: count, ...}`.)

Also, this has a super interesting math study [here](https://www.reddit.com/r/adventofcode/comments/1hbtz8w/2024_day_11_every_sequence_converges_to_3947/) claiming that every sequence eventually converges to a sequence of length 4219 (with some caveats)! That's wild!

# Day 12

This is the first day that was quite challenging for me! At least Part 2. In Part 1, we can use a simple flood-fill algorithm to find each region. While flood filling, any orthogonal neighbor that's not the same letter will be the location of a fence, and since we visit each "plot" only once, we can count the fence segments this way. That was my initial implementation for the `find_region` function. When I saw Part 2, I decided to change this function instead of redo-ing the work.

For Part 2, my initial thought was to count the number of corners that show up in each region. It turns out this is a valid approach, but I couldn't quite make it work. So my second approach was to actually combine the line segments to count to the number of sides. This was accomplished by looking for pairs of fence segments that were collinear and then combining them until no more pairs could be combined. I kept trying to find shortcuts in calculating this stuff, which led me astray for quite a while, but I ultimately got it working. The big trick here is that we need to make sure that in a situation like below, the middle horizontal and vertical lines don't get combined into one line, as specified in the problem.
```
+-----------+
|A A A A A A|
|     +---+ |
|A A A|B B|A|
|     |   | |
|A A A|B B|A|
| +---+---+ |
|A|B B|A A A|
| |   |     |
|A|B B|A A A|
| +---+     |
|A A A A A A|
+-----------+
```
We can use a nice little trick here: put each of the plots on integer coordinates. Then, whenever we find a spot where a fence should be, we shift the line segment over by only 0.25. For example, if we determine that there should be a fence west of `(3, 4)`, we add the segment `(2.75, 3.5)--(2.75, 4.5)`. This ensures that the middle segments in the diagram above won't be collinear! Once I worked out the kinks, this solution ended up working great for the input size. It runs in under 5 seconds, which is good enough for me.

# Day 13

This day absolutely destroyed me! I quickly identified that we are essentially given a pair of linear [Diophantine equations](https://en.wikipedia.org/wiki/Diophantine_equation#One_equation), (one for X and one for Y) which have a [relatively simple solution](https://cp-algorithms.com/algebra/linear-diophantine-equation.html) using the [extended Euclidean algorithm](https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm). So for Part 1, I computed all solutions with non-negative button presses for the X-coordinate and Y-coordinate separately, used `set` intersection to find common solutions, and computed the minimal cost among those solutions. Simple enough!

In Part 2, this becomes intractible because the number of possible solutions for each coordinate is in the billions. So I dove in with pen and paper to start trying to find a mathematical solution instead. I first thought that we could calculate the cost formulas for both sets of solutions and set them equal, which gives a third linear Diophantine equation to solve! Cool, we just find the minimal solution for that one, and we get the minimal cost right? Wrong. :( In a few cases, this doesn't give the correct minimal cost, because by simplifying the cost equations, we accidentally introduce extraneous solutions. I spent literal _hours_ trying to figure a way around this before having a [brain blast](https://www.youtube.com/watch?v=HcRyFCrW5EE) out of nowhere!

We solve for the X and Y coordinates separately to get solution sets that look like:

$$X = \{(a_0 + \hat{a_0}k_x, b_0 + \hat{b_0}k_x) : l_x \le k_x \le u_x] \}$$ 
$$Y = \{(a_0 + \hat{a_0}k_y, a_0 + \hat{a_0}k_y) : l_y \le k_y \le u_y \}$$

We're looking for the intersection of these sets, which gives a system of linear equations! DUH! This took me wayyyyy too long to notice. Rather than bringing in `numpy` or Sage, I decided to work out the formula by hand real quick and implement that. The only hiccup was that floating-point errors would sometimes throw off the solution, so I used Python's `Fraction` class to do the division. Then we just throw out solutions that are out of bounds or non-integral. 

Technically there is the chance of infinitely many solutions, but it looks like the problem-setters intentionally avoided this case (or I got lucky). So we get a unique solution in every case and that's also the minimal solution! Yeesh.

# Day 14

This was a fun day! Part 1 wasn't anything crazy, just simulating robots. My initial simulation code was super slow, but it still worked. Then for Part 2, I initially was going to just print all the robot states to the terminal and look, but it was too slow (and with what my answer ended up being, would've taken way too long). Then I tried to do something where I checked how close the robots were to other robots and looked for the frame that had the highest "neighbor value." For some reason this failed, although I didn't figure out why. Then I checked the subreddit and saw some people talking about variance and the Chinese Remainder Theorem and I smacked my forehead! Of course!

I threw together some code to compute the variance for the x-coordinates and y-coordinates separately and looked for the frames with the lowest variance. We can also do a neat trick here: the x-positions will repeat every 101 seconds and the y-positions will repeat every 103 seconds. So we check for the seconds with the lowest variance separately, then use the Chinese Remainder Theorem to solve for the second where the Christmas tree is! This ends up being relatively simple, as 101 and 103 are both prime, so the CRT applies directly. This also tells us that the robots will cycle every $101\times 103 = 10403$ seconds, so we know the second will be somewhere in that range. There are some super cool visualizations on the subreddit too! I'd highly recommend checking them out.s